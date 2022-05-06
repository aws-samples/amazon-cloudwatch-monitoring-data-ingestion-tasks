import boto3
import os
import pytest
from moto import mock_cloudwatch
from unittest.mock import patch
from src.functions.timeliness_checker.app import lambda_handler


@pytest.fixture(scope="function")
def cloudwatch_client():
    with mock_cloudwatch():
        client = boto3.client("cloudwatch", region_name="us-east-1")
        yield client


@patch("src.functions.timeliness_checker.app.emit_timeliness_metric")
@patch.dict(os.environ, {
    "VENDOR_A_EXPECTED_TIMEFRAME_HOURS": "1",
    "VENDOR_B_EXPECTED_TIMEFRAME_HOURS": "24"

})
def test_timeliness_checker(mock_emit_timeliness_metric, cloudwatch_client):
    expected_vendor_a_timeframe_hours = 1
    expected_vendor_a_timeliness_metric = 0
    expected_vendor_b_timeframe_hours = 24
    expected_vendor_b_timeliness_metric = 0

    lambda_handler({}, "")
    for call in mock_emit_timeliness_metric.call_args_list:
        args, kwarg = call
        if args[0] == "vendor_a":
            assert args[1] == expected_vendor_a_timeframe_hours
            assert args[2] == expected_vendor_a_timeliness_metric
        elif args[0] == "vendor_b":
            assert args[1] == expected_vendor_b_timeframe_hours
            assert args[2] == expected_vendor_b_timeliness_metric
    assert mock_emit_timeliness_metric.call_count == 2


