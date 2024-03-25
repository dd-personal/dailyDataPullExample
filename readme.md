# dataPull python script walkthrough

This Python script automates the process of fetching daily call data metrics from a ClickHouse database and then exporting these metrics as a CSV file to an AWS S3 bucket. 

## Features

- **ClickHouse Database Integration**: Connects securely to a ClickHouse database hosted on `gqfgpljyi1.us-central1.gcp.clickhouse.cloud` to fetch call data.
- **Data Aggregation**: Executes a SQL query to calculate the daily average call duration and the 90th percentile call duration for each agent.
- **Data Transformation**: Transforms the fetched data into a pandas DataFrame for easy manipulation and export.
- **CSV Export**: Converts the DataFrame to a CSV format, which includes metrics for each agent.
- **AWS S3 Upload**: Securely uploads the generated CSV file to an AWS S3 bucket named `crestahomework` under the `daily_exports/` folder, using AWS credentials stored in environment variables.
- **Environment Variable Configuration**: Utilizes environment variables for ClickHouse password (`CLICKHOUSE_PASSWORD`), AWS access key ID (`AWS_ACCESS_KEY_ID`), and AWS secret access key (`AWS_SECRET_ACCESS_KEY`) to secure sensitive information.
- **Dynamic File Naming**: Names the output CSV file based on the current date, facilitating easy tracking and organization of exported files.

## Dependencies

- `pandas`: For data manipulation and CSV file creation.
- `clickhouse_driver`: For connecting to and querying data from ClickHouse.
- `boto3`: For AWS services integration, specifically for uploading files to S3.
- `os`: For retrieving environment variables.
- `io.StringIO`: For creating an in-memory text stream, which is used to hold the CSV content before uploading to S3.
- `datetime`: For fetching the current date to dynamically name the output file.

## Workflow

1. Connect to ClickHouse using the credentials and host details specified.
2. Fetch the daily metrics (average and 90th percentile call durations) for each agent from the `conversations` table.
3. Transform the query results into a pandas DataFrame.
4. Convert the DataFrame into a CSV string.
5. Upload the CSV string to a specified AWS S3 bucket using boto3, with the file named to include the current date.

## Security and Configuration

- The script relies on environment variables for sensitive information to enhance security by storing these in the Git action crediential storage.


