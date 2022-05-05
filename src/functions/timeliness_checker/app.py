import os
from datetime import datetime, timedelta

import boto3
from aws_embedded_metrics import metric_scope
from aws_embedded_metrics.logger.metrics_logger import MetricsLogger


@metric_scope
def emit_timeliness_metric(source: str,
                           timeframe_hours: int,
                           timeliness_metric_value: int,
                           metrics: MetricsLogger) -> None:
    """
    This function is invoked once a new file is uploaded to the Raw
    S3. The Lambda function reads in the

    Parameters
    ----------
    source: str, required
        Name of the data source i.e. Vendor A

    timeframe_hours: int, required
        Expected timeframe of the file ingestion in hours i.e. 24

    timeliness_metric_value: int, required
        Binary flag of whether file was ingested in timeframe. 1 for present
        and 0 for missing

    metrics: MetricsLogger, required
        Object which uploads the metrics in the CloudWatch Embedded Metric
        Format

    Returns
    ------
        None
    """
    metrics.set_dimensions({"Ingestion": source})
    metrics.set_property("TimeframeHours", timeframe_hours)
    metrics.put_metric("Timeliness", timeliness_metric_value, "None")

    return


def lambda_handler(event, context) -> None:
    """
    This Lambda function checks the metric statistics from CloudWatch for the
    successful ingestion of files from both Vendor A and B. If at least one
    file was ingested during the expected timeframe, the function uploads a
    timeliness metric of 1. If no files were ingested during the expected
    timeframe, then a timeliness metric of 0 is uploaded.

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
    # Read in vendor expected timeframes from environment variables
    expected_timeframes = {
        "vendor_a": int(os.environ["VENDOR_A_EXPECTED_TIMEFRAME_HOURS"]),
        "vendor_b": int(os.environ["VENDOR_B_EXPECTED_TIMEFRAME_HOURS"]),
    }

    # Create the CloudWatch client
    cloudwatch = boto3.client("cloudwatch")

    # Create variables for the current and end time
    current_time = datetime.now().replace(microsecond=0, second=0)
    end_time = current_time.isoformat()

    # Iterate through vendors, get ingestion statistics, and create
    # timeliness metric
    for source, timeframe_hours in expected_timeframes.items():
        start_time = (
                current_time - timedelta(hours=timeframe_hours + 1)).isoformat()

        response = cloudwatch.get_metric_statistics(
            Namespace="MonitoringTasksEMF",
            MetricName="Success",
            Dimensions=[{"Name": "Ingestion", "Value": source}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Sum"],
            Unit="Count",
        )

        if len(response["Datapoints"]) > 0:
            # at least 1 source data file has been successfully
            # ingested within the expected timeframe
            timeliness_metric_value = 1
        else:
            # no source data files have been successfully
            # ingested within the expected timeframe
            timeliness_metric_value = 0

        emit_timeliness_metric(source, timeframe_hours, timeliness_metric_value)

    return
