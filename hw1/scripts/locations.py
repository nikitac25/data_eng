import sys
import pandas as pd
import mysql.connector
from config import DB_CONFIG

users_df = pd.read_csv(sys.argv[1])
campaigns_df = pd.read_csv(sys.argv[2])
ad_events_df = pd.read_csv(sys.argv[3])

user_locations = users_df['Location']
campaign_locations = campaigns_df['TargetingCriteria'].dropna().apply(lambda x: x.split(',')[-1].strip())
ad_event_locations = ad_events_df['Location']

all_locations = pd.concat([user_locations, campaign_locations, ad_event_locations])
unique_locations = all_locations.dropna().drop_duplicates().reset_index(drop=True)
location_data = [(loc,) for loc in unique_locations]

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

query = "INSERT INTO locations (name) VALUES (%s)"
cursor.executemany(query, location_data)

conn.commit()
cursor.close()
conn.close()
