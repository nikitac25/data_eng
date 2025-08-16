import sys
import pandas as pd
import mysql.connector
from config import DB_CONFIG

df = pd.read_csv(sys.argv[1])

df['Campaign_id'] = df['CampaignName'].str.extract(r'_(\d+)').astype(int)
df = df.rename(columns={'Location': 'location'})
df['timestamp'] = pd.to_datetime(df['Timestamp'])

df = df.reset_index(drop=True)
df = df.rename(columns={'EventID': 'id'})

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM locations")
location_map = {name: loc_id for loc_id, name in cursor.fetchall()}
df['location_id'] = df['location'].map(location_map)

data = df[[
    'id',
    'Campaign_id',
    'UserID',
    'Device',
    'location_id',
    'timestamp',
    'BidAmount',
    'AdCost',
    'AdRevenue'
]].values.tolist()

query = """
    INSERT INTO impressions (
        id, campaign_id, user_id, device, location_id, timestamp,
        bid_amount, ad_cost, ad_revenue
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

batch_size = 2000
for start in range(0, len(data), batch_size):
    end = start + batch_size
    batch = data[start:end]
    cursor.executemany(query, batch)
    conn.commit()

cursor.close()
conn.close()
