import sys
import pandas as pd
import mysql.connector

df = pd.read_csv(sys.argv[1])

df = df[df['WasClicked'] == 1]

df = df.rename(columns={'EventID': 'campaign_id'})
df['campaign_id'] = df['campaign_id'].str.extract(r'_(\d+)').astype(int)

df = df.reset_index(drop=True)
df['impression_id'] = df.index + 1 

df['click_timestamp'] = pd.to_datetime(df['Timestamp'])

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpassword",
    database="assessment_db"
)
cursor = conn.cursor()

query = """
    INSERT INTO clicks (
        click_id, impression_id, click_timestamp
    )
    VALUES (%s, %s, %s)
"""

df['click_id'] = range(1, len(df) + 1)

data = df[['click_id', 'impression_id', 'click_timestamp']].values.tolist()

cursor.executemany(query, data)
conn.commit()
cursor.close()
conn.close()
