# OverWatch Validator

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What does the OverWatch Validator do?
The **OverWatch Validator** plays a crucial role in the **rules** deployment process. It provides a **secure interface** between **OverWatch Rules Deployment** and the user. 

## How does it do this? 
The robustly defined **YAML schema** is checked against user-defined rule configuration files, which are read by the **OverWatch Deployer**. You can place these configuration files in a folder named `rules` anywhere in your project directory. Otherwise, you can place the configuration files in a folder name of your choice - instructions on how to do this can be found [here](ow-pipeline-cdk#cdk-deploy-parameters)

## Usage
### Validator CLI
insert usage by itself (not in cdk)

### Testing your rule configuration files 
insert usage of validator as a library 

### OverWatch Sample Rule Configurations 
insert some sample rules 

## FAQ
#### Can this replace my existing security controls?
* OverWatch is designed to supplement existing security controls and should not be substituted for any baseline policies.
* OverWatch increases the security coverage of application layer business and security behaviours/state.
