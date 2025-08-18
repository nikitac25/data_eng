from fastapi import FastAPI, HTTPException, Query
from typing import Any, Dict, Optional
from datetime import datetime
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import json
import redis

DB_NAME = os.getenv("MYSQL_DATABASE")
DB_USER = os.getenv("ADMIN_USER")
DB_PASSWORD = os.getenv("ADMIN_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = int(os.getenv("MYSQL_PORT"))

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB   = int(os.getenv("REDIS_DB", "0"))

# Single shared Redis client
_redis = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)

TTL_CAMPAIGN_PERF = 30
TTL_ADVERTISER_SPEND = 300

def _cache_get(key: str):
    try:
        v = _redis.get(key)
        return None if v is None else json.loads(v)
    except Exception:
        # Fail open if Redis is unavailable
        return None

def _cache_set(key: str, value, ttl_seconds: int):
    try:
        _redis.set(key, json.dumps(value), ex=ttl_seconds)
    except Exception:
        # Fail open if Redis is unavailable
        pass

missing = [k for k, v in {
    "MYSQL_DATABASE": DB_NAME,
    "ADMIN_USER|MYSQL_USER": DB_USER,
    "ADMIN_PASSWORD|MYSQL_PASSWORD": DB_PASSWORD,
    "MYSQL_HOST": DB_HOST
}.items() if not v]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

def get_engine() -> Engine:
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)

engine = get_engine()
app = FastAPI(title="Ad Analytics API (MySQL)", version="1.0.0")

def parse_date(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise HTTPException(
        status_code=400,
        detail=f"Invalid date format '{s}'. Use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'."
    )

@app.get("/campaign/{campaign_id}/performance")
def campaign_performance(
    campaign_id: int,
    start: Optional[str] = Query(None, description="Start datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    end: Optional[str] = Query(None, description="End datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
) -> Dict[str, Any]:

    start_dt = parse_date(start)
    end_dt = parse_date(end)

    # Read-through cache (30s)
    _ckey = f"campaign:{campaign_id}:performance:{start_dt.isoformat() if start_dt else 'None'}:{end_dt.isoformat() if end_dt else 'None'}"
    _cached = _cache_get(_ckey)
    if _cached is not None:
        return _cached

    with engine.begin() as conn:
        camp = conn.execute(text("""
            SELECT c.campaign_id, c.campaign_name, a.name AS advertiser_name
            FROM campaigns c
            JOIN advertisers a ON a.id = c.advertiser_id
            WHERE c.campaign_id = :cid
        """), {"cid": campaign_id}).mappings().first()

        if not camp:
            raise HTTPException(status_code=404, detail=f"CampaignID {campaign_id} not found.")

        imp_where = "campaign_id = :cid"
        clk_where = "campaign_id = :cid"
        params = {"cid": campaign_id}
        if start_dt:
            imp_where += " AND timestamp >= :start"
            clk_where += " AND click_timestamp >= :start"
            params["start"] = start_dt
        if end_dt:
            imp_where += " AND timestamp < :end"
            clk_where += " AND click_timestamp < :end"
            params["end"] = end_dt

        impressions = conn.execute(
            text(f"SELECT COUNT(*) FROM impressions WHERE {imp_where}"), params
        ).scalar_one()

        clicks = conn.execute(
            text(f"SELECT COUNT(*) FROM clicks WHERE {clk_where}"), params
        ).scalar_one()

        spend = conn.execute(
            text(f"SELECT COALESCE(SUM(ad_cost), 0) FROM impressions WHERE {imp_where}"), params
        ).scalar_one()

    ctr = float(clicks) / float(impressions) if impressions else 0.0

    result = {
        "campaign_id": camp["campaign_id"],
        "campaign_name": camp["campaign_name"],
        "advertiser_name": camp["advertiser_name"],
        "impressions": int(impressions),
        "clicks": int(clicks),
        "ctr": ctr,
        "ad_spend": float(spend),
        "filters": {
            "start": start_dt.isoformat() if start_dt else None,
            "end": end_dt.isoformat() if end_dt else None
        }
    }

    _cache_set(_ckey, result, TTL_CAMPAIGN_PERF)
    return result

@app.get("/advertiser/{advertiser_id}/spending")
def advertiser_spending(
    advertiser_id: int,
    start: Optional[str] = Query(None, description="Start datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    end: Optional[str] = Query(None, description="End datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
) -> Dict[str, Any]:

    start_dt = parse_date(start)
    end_dt = parse_date(end)

    # Read-through cache (5 minutes)
    _ckey = f"advertiser:{advertiser_id}:spending:{start_dt.isoformat() if start_dt else 'None'}:{end_dt.isoformat() if end_dt else 'None'}"
    _cached = _cache_get(_ckey)
    if _cached is not None:
        return _cached

    with engine.begin() as conn:
        adv = conn.execute(
            text("SELECT id, name FROM advertisers WHERE id = :aid"),
            {"aid": advertiser_id}
        ).mappings().first()

        if not adv:
            raise HTTPException(status_code=404, detail=f"Advertiser {advertiser_id} not found.")

        where = "imp.timestamp IS NOT NULL AND camp.advertiser_id = :aid"
        params = {"aid": advertiser_id}
        if start_dt:
            where += " AND imp.timestamp >= :start"
            params["start"] = start_dt
        if end_dt:
            where += " AND imp.timestamp < :end"
            params["end"] = end_dt

        spend = conn.execute(text(f"""
            SELECT COALESCE(SUM(imp.ad_cost), 0)
            FROM campaigns camp
            JOIN impressions imp ON camp.campaign_id = imp.campaign_id
            WHERE {where}
        """), params).scalar_one()

        campaign_count = conn.execute(text("""
            SELECT COUNT(DISTINCT campaign_id) FROM campaigns WHERE advertiser_id = :aid
        """), {"aid": advertiser_id}).scalar_one()

    result = {
        "advertiser_id": int(adv["id"]),
        "advertiser_name": adv["name"],
        "campaign_count": int(campaign_count or 0),
        "total_ad_spend": float(spend),
        "filters": {
            "start": start_dt.isoformat() if start_dt else None,
            "end": end_dt.isoformat() if end_dt else None
        }
    }

    _cache_set(_ckey, result, TTL_ADVERTISER_SPEND)
    return result

@app.get("/user/{user_id}/engagements")
def user_engagements(
    user_id: int,
    start: Optional[str] = Query(None, description="Start datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    end: Optional[str] = Query(None, description="End datetime (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
) -> Dict[str, Any]:
    """
    Returns ads a user engaged with (rows in clicks) along with campaign and advertiser info.
    Optional date range filters apply to clicks.click_timestamp.
    """
    start_dt = parse_date(start)
    end_dt = parse_date(end)

    with engine.begin() as conn:
        user_exists = conn.execute(
            text("SELECT 1 FROM users WHERE user_id = :uid"), {"uid": user_id}
        ).first()
        if not user_exists:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found.")

        where = "clk.user_id = :uid"
        params = {"uid": user_id}
        if start_dt:
            where += " AND clk.click_timestamp >= :start"
            params["start"] = start_dt
        if end_dt:
            where += " AND clk.click_timestamp < :end"
            params["end"] = end_dt

        rows = conn.execute(text(f"""
            SELECT
                clk.click_id,
                clk.impression_id,
                clk.click_timestamp,
                camp.campaign_id,
                camp.campaign_name,
                adv.name AS advertiser_name
            FROM clicks clk
            JOIN campaigns camp ON camp.campaign_id = clk.campaign_id
            JOIN advertisers adv ON adv.id = camp.advertiser_id
            WHERE {where}
            ORDER BY clk.click_timestamp DESC
            LIMIT 1000
        """), params).mappings().all()

    engagements = [dict(r) for r in rows]
    return {
        "user_id": int(user_id),
        "engagement_count": len(engagements),
        "engagements": engagements,
        "filters": {
            "start": start_dt.isoformat() if start_dt else None,
            "end": end_dt.isoformat() if end_dt else None
        }
    }
