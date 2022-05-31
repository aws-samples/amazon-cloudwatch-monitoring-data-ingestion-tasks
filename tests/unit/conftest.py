import boto3
import pytest
from moto import mock_cloudwatch, mock_s3


@pytest.fixture(scope="function")
def mock_s3_client():
    with mock_s3():
        client = boto3.client("s3")
        yield client


@pytest.fixture(scope="function")
def mock_raw_bucket(mock_s3_client):
    s3_raw_bucket_name = "mock-raw-bucket"
    mock_s3_client.create_bucket(Bucket=s3_raw_bucket_name)
    yield s3_raw_bucket_name


@pytest.fixture(scope="function")
def mock_processed_bucket(mock_s3_client):
    s3_processed_bucket_name = "mock-processed-bucket"
    mock_s3_client.create_bucket(Bucket=s3_processed_bucket_name)
    yield s3_processed_bucket_name


@pytest.fixture(scope="function")
def mock_cloudwatch_client():
    with mock_cloudwatch():
        client = boto3.client("cloudwatch", region_name="us-east-1")
        yield client
