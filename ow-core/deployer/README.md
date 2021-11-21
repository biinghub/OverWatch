# OverWatch Deployer WIP

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage
### Video Guide and Demonstration
[![OverWatch Video Guide and Demonstration](https://img.youtube.com/vi/iumwHlVJtLE/0.jpg)](https://www.youtube.com/watch?v=iumwHlVJtLE)

## Arguments

`rules_folder_path` 

Path to rules folder.

If the autofind flag is set, then provide the directory name of the rules folder.

By default the deployer will look for a 'rules' directory in the project.

`--directory` 

Path to OverWatch Core Application | Default "." or Current Directory

`--autofind` 

Enables autofinding of <rules_folder_path> directory within project

## Example
`./deployer example`

`cdk deploy --all --parameters rulesDirPath=example --parameters enableAutofind=True --no-previous-parameters`

`cdk deploy --all --parameters rulesDirPath=ow-core/example --no-previous-parameters`
