# OverWatch Deployer WIP

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What does the OverWatch Deployer do?

The deployer communicates with AWS Cloudwatch to create/modify Cloudwatch Alarms and Metrics. Specifically, it works with the put_metric_alarm() and put_metric_filter() from boto3 and translates fields from the rules into the Alarms and Metrics.

The deployer is not meant to be run standalone as it does not contain any rule validation. It trusts that the rules have been validated by the validator before communicating with CloudWatch. However this does not mean the rules are blindly trusted, the input fields undergo another round of validation and checking by Cloudwatch upon script execution.

## Arguments

`--directory` 

Path to OverWatch Core Application. Default is "." or current directory

`--autofind`

Enables autofinding of <rules_folder_path> directory within project. If the autofind flag is set, then provide the directory name of the rules folder.

`rules_folder_path` 

Path to rules folder. By default the deployer will look for a 'rules' directory in the project.
