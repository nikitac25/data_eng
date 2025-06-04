import sys
import pandas as pd
import mysql.connector

df = pd.read_csv(sys.argv[1])

df['advertiser_id'] = df['AdvertiserName'].str.extract(r'_(\d+)').astype(int)

df[['TargetAgeRange', 'TargetInterest', 'TargetLocation']] = df['TargetingCriteria'].str.extract(r'(\d{2}-\d{2}),\s*(.*?),\s*(.*)')

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpassword",
    database="assessment_db"
)
cursor = conn.cursor()

query = """
    INSERT INTO campaigns (
        campaign_id, advertiser_id, campaign_name,
        campaign_start_date, campaign_end_date,
        target_age_range, target_interest, target_location,
        ad_slot_size, budget, remaining_budget
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = df[[
    'CampaignID',
    'advertiser_id',
    'CampaignName',
    'CampaignStartDate',
    'CampaignEndDate',
    'TargetAgeRange',
    'TargetInterest',
    'TargetLocation',
    'AdSlotSize',
    'Budget',
    'RemainingBudget'
]].values.tolist()

cursor.executemany(query, data)
conn.commit()

cursor.close()
conn.close()
