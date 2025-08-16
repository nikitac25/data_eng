import os
from datetime import timedelta
import pandas as pd
from pymongo import MongoClient, InsertOne

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/assessment_db")
MONGO_DB = os.getenv("MONGO_DB", "assessment_db")
CSV_DIR = os.getenv("CSV_DIR", "/datasources")
SESSION_GAP_MINUTES = int(os.getenv("SESSION_GAP_MINUTES", "30"))

AD_EVENTS = os.path.join(CSV_DIR, "ad_events.csv")

IMP_COLS = [
    "EventID","AdvertiserName","CampaignName",
    "CampaignStartDate","CampaignEndDate",
    "CampaignTargetingCriteria","CampaignTargetingInterest","CampaignTargetingCountry",
    "AdSlotSize","UserID","Device","Location","Timestamp",
    "BidAmount","AdCost","AdRevenue","Budget","RemainingBudget",
]

ae = pd.read_csv(AD_EVENTS)

for c in ["Timestamp","ClickTimestamp","CampaignStartDate","CampaignEndDate"]:
    if c in ae.columns:
        ae[c] = pd.to_datetime(ae[c], errors="coerce", utc=True)
for c in ["BidAmount","AdCost","AdRevenue","Budget","RemainingBudget"]:
    if c in ae.columns:
        ae[c] = pd.to_numeric(ae[c], errors="coerce")

if "UserID" in ae.columns:
    ae["UserID"] = ae["UserID"].astype(str)

for req in ["UserID","Device","Timestamp"]:
    if req not in ae.columns:
        raise SystemExit(f"missing required column in ad_events.csv: {req}")

ae = ae.sort_values(["UserID","Device","Timestamp"])
gap = timedelta(minutes=SESSION_GAP_MINUTES)
sessions = []

def flush(bucket, user, device):
    if not bucket:
        return
    ts = [x.get("Timestamp") for x in bucket if x.get("Timestamp") is not None]
    s_start = min(ts) if ts else pd.Timestamp.utcnow().to_pydatetime()
    s_end   = max(ts) if ts else s_start
    sessions.append({
        "UserID": str(user),
        "Device": str(device),
        "SessionStart": s_start,
        "SessionEnd": s_end,
        "Impressions": bucket
    })

for (user, device), g in ae.groupby(["UserID","Device"], dropna=False):
    g = g.reset_index(drop=True)
    bucket = []
    last_ts = None
    for _, r in g.iterrows():
        ts = r["Timestamp"]
        if last_ts is not None and pd.notna(ts) and pd.notna(last_ts) and (ts - last_ts) > gap:
            flush(bucket, user, device)
            bucket = []

        imp = {k: r[k] for k in IMP_COLS if k in r and pd.notna(r[k])}

        for dtc in ["Timestamp","CampaignStartDate","CampaignEndDate"]:
            if dtc in imp:
                imp[dtc] = pd.to_datetime(imp[dtc], utc=True).to_pydatetime()

        clicks = []
        wc = r.get("WasClicked", None)
        ct = r.get("ClickTimestamp", None)
        if (wc is not None and not pd.isna(wc)) or (ct is not None and not pd.isna(ct)):
            entry = {}
            if wc is not None and not pd.isna(wc):
                if isinstance(wc, str):
                    entry["WasClicked"] = (wc.strip().lower() in ("1","true","t","yes","y"))
                else:
                    entry["WasClicked"] = bool(wc)
            if ct is not None and not pd.isna(ct):
                entry["ClickTimestamp"] = pd.to_datetime(ct, utc=True).to_pydatetime()
            clicks.append(entry)
        if clicks:
            imp["Clicks"] = clicks

        if "WasClicked" in imp: del imp["WasClicked"]
        if "ClickTimestamp" in imp: del imp["ClickTimestamp"]

        bucket.append(imp)
        last_ts = ts if pd.notna(ts) else last_ts

    flush(bucket, user, device)

cli = MongoClient(MONGO_URI)
db = cli[MONGO_DB]
coll = db["sessions"]

if sessions:
    ops = [InsertOne(doc) for doc in sessions]
    res = coll.bulk_write(ops, ordered=False)
    print(f"Inserted {len(sessions)} session documents into {MONGO_DB}.sessions")
else:
    print("No sessions to write.")
