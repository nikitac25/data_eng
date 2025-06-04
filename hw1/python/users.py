import sys
import pandas as pd
import mysql.connector

df = pd.read_csv(sys.argv[1])

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpassword",
    database="assessment_db"
)
cursor = conn.cursor()

query = """
INSERT INTO users (user_id, age, gender, location, interests, signup_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""
data = df[['UserID', 'Age', 'Gender', 'Location', 'Interests', 'SignupDate']].values.tolist()
cursor.executemany(query, data)
conn.commit()

cursor.close()
conn.close()
