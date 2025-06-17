import os
import mysql.connector
import pandas as pd
from config import DB_CONFIG

sql_dir = "../sql"
output_dir = "../output"

sql_files = [
    "campaign_performance.sql",
    "advertiser_spending.sql",
    "cost_efficiency.sql",
    "regional_analysis.sql",
    "user_engagement.sql",
    "budget_consumption.sql",
    "device_perfomance_comparison.sql"
]

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

os.makedirs(output_dir, exist_ok=True)

for file in sql_files:
    file_path = os.path.join(sql_dir, file)
    with open(file_path, 'r') as f:
        query = f.read()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=columns)
    csv_file = os.path.join(output_dir, file.replace(".sql", ".csv"))
    df.to_csv(csv_file, index=False)
    print(f"Written: {csv_file}")

cursor.close()
conn.close()
