import sys
import pandas as pd
import mysql.connector
from config import DB_CONFIG


df = pd.read_csv(sys.argv[1])
df = df[df['WasClicked'] == 1]

df['campaign_id'] = df['CampaignName'].str.extract(r'_(\d+)').astype(int)
df['click_timestamp'] = pd.to_datetime(df['Timestamp'])


click_data = df[['UserID', 'campaign_id', 'click_timestamp']].values.tolist()

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

insert_rows = []
click_id = 1

for user_id, campaign_id, click_ts in click_data:
    cursor.execute("""
        SELECT id FROM impressions
        WHERE user_id = %s AND campaign_id = %s AND timestamp = %s
        LIMIT 1
    """, (user_id, campaign_id, click_ts))
    
    result = cursor.fetchone()
    if result:
        impression_id = result[0]
        insert_rows.append((click_id, campaign_id, user_id, impression_id, click_ts))
        click_id += 1

cursor.executemany("""
    INSERT INTO clicks (click_id, campaign_id, user_id, impression_id, click_timestamp)
    VALUES (%s, %s, %s, %s, %s)
""", insert_rows)

conn.commit()
cursor.close()
conn.close()
