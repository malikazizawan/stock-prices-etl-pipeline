# Serverless Stock Price ETL Pipeline

An automated, event-driven ETL pipeline built on AWS that detects stock price CSV uploads to S3, processes and transforms the data via Lambda, stores the output back to S3, and logs execution in CloudWatch — with zero manual intervention.

## Architecture

![Architecture Diagram](architecture/architecture-diagram.png)

S3 (input-data/) → S3 Event Notification → SQS → Lambda Trigger → Lambda → S3 (output-data/) → CloudWatch Logs

## Problem Statement

Manually processing stock price CSV files is time-consuming and error-prone. This project automates the entire flow — from file upload to processed output — using a fully serverless, event-driven architecture.

## Tech Stack

- Amazon S3
- Amazon SQS (Standard Queue)
- AWS Lambda (Python 3.11)
- AWS Lambda Layer (AWSSDKPandas)
- Amazon CloudWatch
- AWS IAM
- Python (pandas, boto3, json)

## How It Works

1. A CSV file is uploaded to the S3 bucket under the `input-data/` prefix.
2. S3 Event Notification sends a message to an SQS queue.
3. SQS triggers the Lambda function.
4. Lambda downloads the CSV, transforms it (adds `symbol`, `close_pct_change`, `created_at` columns), and uploads the processed file to `output-data/`.
5. Execution logs are recorded in CloudWatch.

## Security

IAM role follows the least privilege principle:
- `s3:GetObject` scoped to `input-data/*`
- `s3:PutObject` scoped to `output-data/*`
- `sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:GetQueueAttributes` scoped to the specific queue
- CloudWatch Logs permissions for logging

## Project Structure
lambda/lambda_function.py    - Lambda function code
sample-data/                 - Sample CSV file
architecture/                - Architecture diagram
screenshots/                 - AWS console screenshots

## Author

Aziz Awan

