import json
import os
from datetime import datetime
from urllib.parse import unquote_plus

import boto3
import botocore
from aws_embedded_metrics import metric_scope


def validate_data_fields(data: dict) -> None:
    """
    This function checks if there are only three keys in the raw data and
    that the keys only include 'name', 'status', and 'object_id'

    Parameters
    ----------
    data: dict, required
        Dictionary containing the data from the vendor JSON file

    Returns
    ------
        None
    """
    valid_fields = {"name", "status", "object_id"}

    # Check if there are only three keys and that keys are valid
    if (len(data) == 3) and (all(key in data for key in valid_fields)):
        return
    else:
        raise KeyError(f"Invalid key field found in the data: {data}"
                       f"Key fields must contain: 'name', 'status', 'object_id'")


def validate_data_types(data: dict) -> None:
    """
    This function checks whether the data types of the values are valid. The
    following needs to be true:
        name: str
        status: str
        object_id: int

    Parameters
    ----------
    data: dict, required
        Dictionary containing the data from the vendor JSON file

    Returns
    ------
        None
    """
    # Check data types for the values in the data
    if (
            isinstance(data["name"], str) and
            isinstance(data["status"], str) and
            isinstance(data["object_id"], int)
    ):
        return
    else:
        raise TypeError(f"Invalid data type(s) for value(s) in the data: "
                        f" {data}")


def write_processed_file(s3_client: botocore.client.BaseClient,
                         processed_s3_bucket: str,
                         source: str,
                         data: dict) -> None:
    """
    This Lambda function is invoked once a new file is uploaded to the Raw
    S3. The Lambda function reads in the

    Parameters
    ----------
    s3_client: botocore.client.BaseClient, required
        S3 client used to put file into Processed S3 bucket

    processed_s3_bucket: str, required
        Name of the Processed S3 bucket

    source: str, required
        The source of the raw data which is either Vendor A or B

    data: dict, required
        The content of the raw data

    Returns
    ------
        None
    """
    # Create date variable
    current_date = datetime.today().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")

    # Create S3 prefix
    s3_key = f"{source}/{current_date}/{current_datetime}-processed-file.json"

    # Create JSON object
    processed_json_obj = json.dumps(data)

    # Upload data into JSON file in Raw S3 bucket
    s3_client.put_object(
        Body=processed_json_obj,
        Bucket=processed_s3_bucket,
        Key=s3_key
    )


@metric_scope
def lambda_handler(event, context, metrics) -> None:
    """
    This Lambda function is invoked once a new file is uploaded to the Raw 
    S3. The Lambda function reads in the  
    
    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    metrics: MetricsLogger, required
        Object which uploads the metrics in the CloudWatch Embedded Metric
        Format

    Returns
    ------
        None
    """
    # Read in environment variables
    processed_s3_bucket = os.environ["PROCESSED_BUCKET_NAME"]

    # Create the s3 client
    s3_client = boto3.client("s3")

    # Read bucket and key from event
    record = event["Records"][0]
    raw_s3_bucket = record["s3"]["bucket"]["name"]
    s3_object_key = unquote_plus(record["s3"]["object"]["key"])

    # Parse source name
    source = s3_object_key.split("/")[0]

    # Read in the vendor JSON file
    result = s3_client.get_object(Bucket=raw_s3_bucket, Key=s3_object_key)
    data = eval(result["Body"].read().decode())

    # Check if data fields are valid
    validate_data_fields(data)

    # Check if data types are valid
    validate_data_types(data)

    # Write data to appropriate partition in the Processed S3 bucket
    write_processed_file(s3_client, processed_s3_bucket, source, data)

    # Emit CloudWatch metric for successful data processing
    metrics.set_dimensions({"Ingestion": source})
    metrics.put_metric("Success", 1, "Count")

    return
