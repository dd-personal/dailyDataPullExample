import os
import pandas as pd
from clickhouse_driver import Client
from io import StringIO
import boto3
from datetime import datetime

# Clickhouse connection details
clickhouse_host = 'gqfgpljyi1.us-central1.gcp.clickhouse.cloud'
clickhouse_secure = True
clickhouse_password = os.environ['CLICKHOUSE_PASSWORD']

# AWS S3 details
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
s3_bucket_name = 'crestahomework'
s3_folder = 'daily_exports'


# Connect to Clickhouse
client = Client(host=clickhouse_host, secure=clickhouse_secure, password=clickhouse_password)

# Query to fetch daily average and 90th percentile call length for each agent
query = """
SELECT
    agent_id,
    AVG(call_duration_sec) AS average_call_duration,
    quantileExact(0.9)(call_duration_sec) AS percentile_90_call_duration
FROM conversations
GROUP BY agent_id
ORDER BY agent_id
"""

# Execute the query
data = client.execute(query, with_column_types=True)

# The data for the DataFrame
data_for_df = data[0]

# Extracting the column names from the second element of the 'data' list.
column_names = []
for col in data[1]:
    column_name = col[0]
    column_names.append(column_name)

# Create a DataFrame with extracted data
df = pd.DataFrame(data_for_df, columns=column_names)

# Current date for file naming
current_date = datetime.now().strftime('%Y-%m-%d')

# Convert DataFrame to CSV format
csv_buffer = StringIO()  # Store csv data body in memory so we don't have to write it to a file

df.to_csv(csv_buffer, index=False)

# Upload CSV to S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
upload_path = os.path.join(s3_folder, f'agent_calls_{current_date}.csv')
s3_client.put_object(Bucket=s3_bucket_name, Key=upload_path, Body=csv_buffer.getvalue())

print(f"Data uploaded successfully to {upload_path} -- {current_date}")
