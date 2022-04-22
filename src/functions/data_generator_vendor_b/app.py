import json
import os
from datetime import datetime

import boto3


def lambda_handler(event, context) -> None:
    """
    This Lambda function is scheduled to run every day and uploads a JSON
    file to the Raw S3 bucket with the following prefix: 
        vendor_b/<date in yyyy-mm-dd>

    The following shows the file structure with sample data:
    {
        "name": "XYZ MATERIALS CO.",
        "status": "DELIVERED",
        "object_id": 12345
    }

    name: str
    status: str
    object_id: int

    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        None
    """
    # Read in environment variable
    raw_s3_bucket = os.environ["RAW_BUCKET_NAME"]

    # Create the s3 client
    s3_client = boto3.client("s3")

    # Create variables
    current_date = datetime.today().strftime("%Y-%m-%d")
    vendor_data = {
        "name": "XYZ MATERIALS CO.",
        "status": "DELAYED",
        "object_id": 54321
    }

    # Create JSON object
    vendor_json = json.dumps(vendor_data)

    # Create S3 prefix
    s3_key = f"vendor_b/{current_date}/{current_date}-raw-file.json"

    # Upload data into JSON file in Raw S3 bucket
    s3_client.put_object(
        Body=vendor_json,
        Bucket=raw_s3_bucket,
        Key=s3_key
    )

    return
