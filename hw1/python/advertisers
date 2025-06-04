import sys
import pandas as pd
import mysql.connector

df = pd.read_csv(sys.argv[1])
advertisers = df[['AdvertiserName']].drop_duplicates().reset_index(drop=True)
advertisers['id'] = advertisers['AdvertiserName'].str.extract(r'_(\d+)$').astype(int)

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpassword",
    database="assessment_db"
)
cursor = conn.cursor()

query = "INSERT INTO advertisers (id, name) VALUES (%s, %s)"
cursor.executemany(query, advertisers[['id', 'AdvertiserName']].values.tolist())
conn.commit()

cursor.close()
conn.close()
