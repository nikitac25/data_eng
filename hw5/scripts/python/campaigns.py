import sys
import pandas as pd
import mysql.connector
from config import DB_CONFIG

df = pd.read_csv(sys.argv[1])

df['advertiser_id'] = df['AdvertiserName'].str.extract(r'_(\d+)').astype(int)

df[['TargetAgeRange', 'TargetInterest', 'TargetLocation']] = df['TargetingCriteria'].str.extract(r'(\d{2}-\d{2}),\s*(.*?),\s*(.*)')

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM locations")
location_map = {name: loc_id for loc_id, name in cursor.fetchall()}
df['target_location_id'] = df['TargetLocation'].map(location_map)

data = df[[
    'CampaignID',
    'advertiser_id',
    'CampaignName',
    'CampaignStartDate',
    'CampaignEndDate',
    'TargetAgeRange',
    'TargetInterest',
    'target_location_id',
    'AdSlotSize',
    'Budget',
    'RemainingBudget'
]].values.tolist()

query = """
    INSERT INTO campaigns (
        campaign_id, advertiser_id, campaign_name,
        campaign_start_date, campaign_end_date,
        target_age_range, target_interest, target_location_id,
        ad_slot_size, budget, remaining_budget
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query, data)
conn.commit()

cursor.close()
conn.close()
