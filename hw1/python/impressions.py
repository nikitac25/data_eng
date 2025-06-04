import sys
import pandas as pd
import mysql.connector

df = pd.read_csv(sys.argv[1])

df = df.rename(columns={'EventID': 'campaign_id'})
df['campaign_id'] = df['campaign_id'].str.extract(r'_(\d+)').astype(int)

df = df.rename(columns={'Location': 'user_location'})

df['timestamp'] = pd.to_datetime(df['Timestamp'])

df = df.reset_index(drop=True)
df['id'] = df.index + 1 

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpassword",
    database="assessment_db"
)
cursor = conn.cursor()

query = """
    INSERT INTO impressions (
        id, campaign_id, user_id, device, user_location, timestamp,
        bid_amount, ad_cost, ad_revenue
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = df[[
    'id',
    'campaign_id',
    'UserID',
    'Device',
    'user_location',
    'timestamp',
    'BidAmount',
    'AdCost',
    'AdRevenue'
]].values.tolist()

cursor.executemany(query, data)
conn.commit()
cursor.close()
conn.close()
