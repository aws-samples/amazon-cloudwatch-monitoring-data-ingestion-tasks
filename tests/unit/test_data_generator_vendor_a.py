import boto3
import os
import pytest
from moto import mock_s3
from unittest.mock import patch
from src.functions.data_generator_vendor_a import app

s3_bucket_name = "test-bucket"


@pytest.fixture(scope="function")
def s3_client():
    with mock_s3():
        client = boto3.client("s3")
        yield client


@pytest.fixture(scope="function")
def raw_bucket(s3_client):
    s3_client.create_bucket(Bucket=s3_bucket_name)
    return s3_bucket_name


@patch.dict(os.environ, {
    "RAW_BUCKET_NAME": s3_bucket_name
})
def test_data_generator_vendor_a(s3_client, raw_bucket):
    expected_s3_data = {
        "name": "ABC GOODS INC.",
        "status": "DELIVERED",
        "object_id": 12345
    }

    app.lambda_handler({}, "")

    response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
    contents = response["Contents"][0]
    s3_key = contents["Key"]
    result = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_key)
    data = eval(result["Body"].read().decode())

    assert data == expected_s3_data
