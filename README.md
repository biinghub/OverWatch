# OverWatch

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is OverWatch?
**OverWatch** is a cloud-based rules creation and enforcement engine designed to incorporate security rules and actions with minimal intervention on your existing applications on AWS whilst accelerating the secure development of your new ones.

## What is the aim of OverWatch?
**OverWatch** aims to provide a low-code, simple and efficient solution to connecting the dots between **AWS CloudWatch** and **security driven application logic**.
**OverWatch** 

## Installation
### Video Guide and Demonstration
[![OverWatch Video Guide and Demonstration](https://img.youtube.com/vi/iumwHlVJtLE/0.jpg)](https://www.youtube.com/watch?v=iumwHlVJtLE)
### OverWatch Core (AWS Deployment)
The easiest way to install the OverWatch Core software into your AWS account is to naviagte on an AWS shell environment to the `ow-pipeline-cdk` folder, then type in the following command:
```
cdk deploy --all
```


## example
`./validator example`

`cdk deploy --all --parameters rulesDirPath=example --parameters enableAutofind=True --no-previous-parameters`

`cdk deploy --all --parameters rulesDirPath=ow-core/example --no-previous-parameters`
