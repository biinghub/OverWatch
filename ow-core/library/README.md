# OverWatch SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What does the OverWatch SDK do?
The **OverWatch SDK** plays a crucial role in the functionality of OverWatch.

In essence, the SDK provides a **simple interface** between **OverWatch** and the application utilising OverWatch. 

## Docs
[Link to API Docs](actions.md)

## FAQ
### Can the SDK be used on its own? 
* Unfortunately, the SDK **cannot** be used without OverWatch core installed and has no functionality without the relevant rules set.
* You can find out how OverWatch is installed on the main project README [here](../../README.md) 

### The SDK gives something about Access Denied and Insufficient Permissions:
* Ensure that you have the following AWS IAM permissions for your deployment instance or AWS environment profile:
    * logs:DescribeLogStreams
    * logs:PutLogEvents
    * logs:CreateLogGroup
    * logs:CreateLogStream

### The SDK gives something about AWS not found errors or similar:
* Ensure that the SDK is running on a deployment instance of an AWS system or has an AWS connection configured in the environment
* The SDK utilises boto3 and CloudWatch which require an AWS connection
