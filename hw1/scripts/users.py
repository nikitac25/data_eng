import sys
import pandas as pd
import mysql.connector
from config import DB_CONFIG

df = pd.read_csv(sys.argv[1])

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM locations")
location_map = {name: loc_id for loc_id, name in cursor.fetchall()}
df['location_id'] = df['Location'].map(location_map)

query = """
INSERT INTO users (user_id, age, gender, location_id, interests, signup_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""
data = df[['UserID', 'Age', 'Gender', 'location_id', 'Interests', 'SignupDate']].values.tolist()
cursor.executemany(query, data)
conn.commit()

cursor.close()
conn
