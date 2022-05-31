import os
from unittest.mock import patch

from src.functions.data_generator_vendor_a import app


@patch.dict(os.environ, {
    "RAW_BUCKET_NAME": 'mock-raw-bucket'
})
def test_data_generator_vendor_a(mock_s3_client, mock_raw_bucket):
    expected_s3_data = {
        "name": "ABC GOODS INC.",
        "status": "DELIVERED",
        "object_id": 12345
    }

    app.lambda_handler({}, "")

    response = mock_s3_client.list_objects_v2(Bucket=mock_raw_bucket)
    contents = response["Contents"][0]
    s3_key = contents["Key"]
    result = mock_s3_client.get_object(Bucket=mock_raw_bucket, Key=s3_key)
    data = eval(result["Body"].read().decode())

    assert data == expected_s3_data
