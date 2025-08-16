
import os
import re
from datetime import datetime, timezone
import pandas as pd
from pymongo import MongoClient, UpdateOne

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/assessment_db")
MONGO_DB  = os.getenv("MONGO_DB",  "assessment_db")
CSV_DIR   = os.getenv("CSV_DIR",   "/datasources")

AD_EVENTS = os.path.join(CSV_DIR, "ad_events.csv")

ENG_COLS = [
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

if "UserID" not in ae.columns:
    raise SystemExit("missing required column in ad_events.csv: UserID")

if "Timestamp" in ae.columns:
    ae = ae.sort_values(["UserID","Timestamp"])

AGE_RE_RANGE  = re.compile(r"(\d{1,3})\s*-\s*(\d{1,3})")
AGE_RE_SINGLE = re.compile(r"(\d{1,3})\+?")

def to_py_dt(val):
    if pd.isna(val): return None
    dt = pd.to_datetime(val, utc=True, errors="coerce")
    if pd.isna(dt): return None
    return dt.to_pydatetime()

def derive_age(criteria: str) -> int:
    if not isinstance(criteria, str) or "Age" not in criteria:
        return 0
    m = AGE_RE_RANGE.search(criteria)
    if m:
        return int(m.group(1))
    m2 = AGE_RE_SINGLE.search(criteria)
    if m2:
        return int(m2.group(1))
    return 0

users = {}

for _, r in ae.iterrows():
    uid = str(r.get("UserID")) if pd.notna(r.get("UserID")) else ""
    if not uid:
        continue

    eng = {k: r[k] for k in ENG_COLS if k in r and pd.notna(r[k])}

    for dtc in ["Timestamp","CampaignStartDate","CampaignEndDate"]:
        if dtc in eng:
            eng[dtc] = to_py_dt(eng[dtc])

    for numc in ["BidAmount","AdCost","AdRevenue","Budget","RemainingBudget"]:
        if numc in eng and pd.isna(eng[numc]):
            eng[numc] = None

    for sc in ["EventID","AdvertiserName","CampaignName",
               "CampaignTargetingCriteria","CampaignTargetingInterest",
               "CampaignTargetingCountry","AdSlotSize","UserID","Device","Location"]:
        if sc in eng:
            eng[sc] = str(eng[sc])

    clicks = []
    wc = r.get("WasClicked", None)
    ct = r.get("ClickTimestamp", None)
    if (wc is not None and not pd.isna(wc)) or (ct is not None and not pd.isna(ct)):
        entry = {}
        if wc is not None and not pd.isna(wc):
            entry["WasClicked"] = (str(wc).strip().lower() in ("1","true","t","yes","y")) if isinstance(wc,str) else bool(wc)
        if ct is not None and not pd.isna(ct):
            entry["ClickTimestamp"] = to_py_dt(ct)
        if entry:
            clicks.append(entry)
    if clicks:
        eng["Clicks"] = clicks

    if uid not in users:
        crit = eng.get("CampaignTargetingCriteria","")
        age  = derive_age(crit)
        loc  = eng.get("Location","") or "Unknown"
        intr = eng.get("CampaignTargetingInterest","") or ""
        sgn  = eng.get("Timestamp") or datetime.now(timezone.utc)

        users[uid] = {
            "UserID": uid,
            "demographics": {
                "Age": int(age),
                "Gender": "Unknown",
                "Location": loc,
                "Interests": intr,
                "SignupDate": sgn
            },
            "engagements": []
        }

    if eng.get("Timestamp") and eng["Timestamp"] < users[uid]["demographics"]["SignupDate"]:
        users[uid]["demographics"]["SignupDate"] = eng["Timestamp"]

    if eng.get("Location") and users[uid]["demographics"]["Location"] in ("","Unknown"):
        users[uid]["demographics"]["Location"] = eng["Location"]

    if eng.get("CampaignTargetingInterest"):
        users[uid]["demographics"]["Interests"] = eng["CampaignTargetingInterest"]

    users[uid]["engagements"].append(eng)

cli = MongoClient(MONGO_URI)
db = cli[MONGO_DB]
coll = db["user_stats"]

ops = [UpdateOne({"UserID": d["UserID"]}, {"$set": d}, upsert=True) for d in users.values()]
if ops:
    res = coll.bulk_write(ops, ordered=False)
    print(f"Inserted/updated user_stats: upserted={getattr(res,'upserted_count',0)} modified={getattr(res,'modified_count',0)} matched={getattr(res,'matched_count',0)}")
else:
    print("Nothing to write into user_stats.")
