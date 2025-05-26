import json
import requests
import boto3
import logging
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
NEWSAPI_KEY = "67c1f11c5a014e87910655670ea6961e"
NEWSAPI_URL = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=100&apiKey={NEWSAPI_KEY}"
S3_BUCKET = "news-raw-data"  # Ensure this is correctly named in your S3 console

def lambda_handler(event, context):
    logger.info("Starting news ingestion Lambda")

    try:
        response = requests.get(NEWSAPI_URL)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            logger.warning("No articles found in response.")
            return {
                "statusCode": 204,
                "body": "No articles found."
            }

        # Timestamped key: e.g., news-raw-data/2025/07/25/14-30.json
        timestamp = datetime.utcnow()
        s3_key = f"{timestamp.strftime('%Y/%m/%d/%H-%M')}.json"

        # Upload to S3
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(articles),
            ContentType='application/json'
        )

        logger.info(f"Successfully saved {len(articles)} articles to S3 at {s3_key}")
        return {
            "statusCode": 200,
            "body": f"Successfully ingested {len(articles)} articles at {s3_key}"
        }

    except requests.RequestException as e:
        logger.error(f"NewsAPI request failed: {e}")
        return {
            "statusCode": 502,
            "body": f"Error fetching news: {str(e)}"
        }

    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 upload failed: {e}")
        return {
            "statusCode": 500,
            "body": f"Error saving to S3: {str(e)}"
        }

    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return {
            "statusCode": 500,
            "body": f"Unexpected error: {str(e)}"
        }
