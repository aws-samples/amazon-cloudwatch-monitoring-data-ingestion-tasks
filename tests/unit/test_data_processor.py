import pytest

from src.functions.data_processor.app import (
    validate_data_fields,
    validate_data_types,
    write_processed_file
)


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


def test_write_processed_file(mock_s3_client, mock_processed_bucket):
    test_source = "test-vendor"
    test_data = {
        "name": "vendor-name", "status": "SUCCESSFUL", "object_id": 123
    }
    write_processed_file(
        mock_s3_client,
        mock_processed_bucket,
        test_source,
        test_data
    )

    response = mock_s3_client.list_objects_v2(Bucket=mock_processed_bucket)
    contents = response["Contents"][0]
    s3_key = contents["Key"]
    result = mock_s3_client.get_object(Bucket=mock_processed_bucket, Key=s3_key)
    data = eval(result["Body"].read().decode())

    assert data == test_data
