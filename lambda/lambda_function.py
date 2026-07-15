import json
import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

s3_client = boto3.client('s3')


def download_and_read_csv(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(response['Body'])
    return df


def transform_data(df):
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    df['symbol'] = 'GOOG'
    df['close_pct_change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df['Volume'] = df['Volume'].apply(lambda v: 'N/A' if v < 100000 else v)
    df['created_at'] = datetime.now().isoformat()

    return df


def upload_csv_to_s3(df, bucket, input_key):
    output_key = input_key.replace('input-data/', 'output-data/')

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_client.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=csv_buffer.getvalue()
    )

    return output_key


def lambda_handler(event, context):
    processed_files = []
    failed_files = []

    for record in event['Records']:
        try:
            s3_event = json.loads(record['body'])
            bucket_name = s3_event['Records'][0]['s3']['bucket']['name']
            object_key = s3_event['Records'][0]['s3']['object']['key']

            print(f"Processing file: {object_key} from bucket: {bucket_name}")

            df = download_and_read_csv(bucket_name, object_key)
            print(f"Downloaded CSV with shape: {df.shape}")

            transformed_df = transform_data(df)
            print(f"Transformation complete: {transformed_df.shape}")

            output_key = upload_csv_to_s3(transformed_df, bucket_name, object_key)
            print(f"Uploaded processed file to: {output_key}")

            processed_files.append(output_key)

        except Exception as e:
            print(f"ERROR processing record: {str(e)}")
            failed_files.append(str(e))

    return {
        "statusCode": 200 if not failed_files else 500,
        "body": json.dumps({
            "processed": processed_files,
            "failed": failed_files
        })
    }