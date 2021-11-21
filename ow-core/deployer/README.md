# OverWatch Deployer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What does the OverWatch Deployer do?

The deployer communicates with AWS Cloudwatch to create/modify Cloudwatch Alarms and Metrics.

## How does the OverWatch Deployer deploy rules?

Specifically, it works with the `put_metric_alarm` and `put_metric_filter` from `boto3` and translates fields from the rules into the Alarms and Metrics.

## Usage
Team 3 **does not** recommend you use the deployer alone and as such **will not** provide usage documentation to prevent any shortcuts that will undermine the security of OverWatch. 

The deployer is not meant to be run standalone as it does not offer any rule validation. It trusts that the rules have been validated by the validator before communicating with CloudWatch. However this does not mean the rules are blindly trusted, the input fields undergo another round of validation and checking by Cloudwatch upon script execution.

## Arguments

`--directory` 

Path to OverWatch Core Application. Default is "." or current directory

`--autofind`

Enables autofinding of <rules_folder_path> directory within project. If the autofind flag is set, then provide the directory name of the rules folder.

`rules_folder_path` 

Path to rules folder. By default the deployer will look for a 'rules' directory in the project.

## FAQ
### Can the deployer be used on its own? 
* Yes, however team 3 **strongly recommends** you use the provided installation guide as you lose many protective features when OverWatch is not used in it's intended form.
* You can find out how OverWatch is installed on the main project README [here](../../README.md) 

### The deployer gives something about Access Denied and Insufficient Permissions:
* Redeploy the [OverWatch Core CDK](../../ow-pipeline-cdk) as all permissions should be handled by the installation.

### The deployer gives something about AWS not found errors or similar:
* Ensure that the deployer is running on a deployment instance of an AWS system or has an AWS connection configured in the environment
* The deployer utilises boto3 which requires an AWS connection
