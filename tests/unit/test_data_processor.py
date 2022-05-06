import boto3
import pytest
from moto import mock_s3
from src.functions.data_processor.app import (
    validate_data_fields,
    validate_data_types,
    write_processed_file
)

s3_raw_bucket_name = "test-raw-bucket"
s3_processed_bucket_name = "test-processed-bucket"


@pytest.fixture(scope="function")
def s3_client():
    with mock_s3():
        client = boto3.client("s3")
        yield client


@pytest.fixture(scope="function")
def raw_bucket(s3_client):
    s3_client.create_bucket(Bucket=s3_raw_bucket_name)

    return s3_raw_bucket_name


@pytest.fixture(scope="function")
def processed_bucket(s3_client):
    s3_client.create_bucket(Bucket=s3_processed_bucket_name)
    return s3_processed_bucket_name


def test_validate_data_fields_successful():
    test_data = {
        "name": "vendor-name", "status": "SUCCESSFUL", "object_id": 123
    }
    try:
        validate_data_fields(test_data)
    except KeyError:
        assert False


def test_validate_data_fields_exception():
    test_data = {
        "bad_key": "vendor-name", "status": "UNSUCCESSFUL", "object_id": 123
    }
    with pytest.raises(KeyError):
        validate_data_fields(test_data)


def test_validate_data_types_successful():
    test_data = {
        "name": "vendor-name", "status": "SUCCESSFUL", "object_id": 123
    }
    try:
        validate_data_types(test_data)
    except TypeError:
        assert False


def test_validate_data_types_exception():
    test_data = {
        "name": 123, "status": "UNSUCCESSFUL", "object_id": "wrong_dtype"
    }
    with pytest.raises(TypeError):
        validate_data_types(test_data)


def test_write_processed_file(s3_client, processed_bucket):
    test_source = "test-vendor"
    test_data = {
        "name": "vendor-name", "status": "SUCCESSFUL", "object_id": 123
    }
    write_processed_file(
        s3_client,
        s3_processed_bucket_name,
        test_source,
        test_data
    )

    response = s3_client.list_objects_v2(Bucket=s3_processed_bucket_name)
    contents = response["Contents"][0]
    s3_key = contents["Key"]
    result = s3_client.get_object(Bucket=s3_processed_bucket_name, Key=s3_key)
    data = eval(result["Body"].read().decode())

    assert data == test_data
