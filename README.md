# Monitoring Data Ingestion Tasks With AWS CloudWatch Metrics and Alarms

This repository contains source code and supporting files for a serverless
application that you can deploy with the SAM CLI to create a
solution that monitors data ingestion tasks. It includes the following files
and folders:

- src/functions/ - Source code for the application's Lambda functions which
  generates data for Vendor A and Vendor B, processes the data, and creates
  metrics sent to Amazon CloudWatch
- tests/ - Unit tests for the Lambda functions' application code.
- template.yaml - A template that defines the application's AWS resources.

You can use this repository to create a solution which provides monitoring
and alerting on a data ingestion workload using Amazon CloudWatch Embedded Metric Format.
It also provides an approach to monitoring file ingestion activity within an
expected timeframe using Amazon CloudWatch Metrics and Alarms.

The application uses several AWS resources, including AWS Lambda functions,
Amazon S3 buckets, and various Amazon CloudWatch components. These resources
are defined in the `template.yaml` file in this project.

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda.

To use the SAM CLI, you need the following tools:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
src$ pip install -r tests/requirements.txt --user
# Unit Tests
src$ python -m pytest tests/unit -v
```

## Cleanup

To avoid incurring further charges, please use the following instructions to delete all the resources created from this solution.

Assuming you used your project name for the stack name, run the following
command to delete the resources with the SAM CLI:

```bash
sam delete --stack-name src
```

## Resources
For more information on CloudWatch Logs Embedded Metric Format, please visit
the [service documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html) and related [AWS blog post](https://aws.amazon.com/blogs/mt/enhancing-workload-observability-using-amazon-cloudwatch-embedded-metric-format/).

The [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
provides an introduction to SAM specification, the SAM CLI, and serverless
application concepts.

## Security
Please see [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
