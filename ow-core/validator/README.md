# OverWatch Validator

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What does the OverWatch Validator do?
The **OverWatch Validator** plays a crucial role in the **rules** deployment process. It provides a **secure interface** between **OverWatch Rules Deployment** and the user. 

## How does it do this? 
The robustly defined **YAML schema** is checked against user-defined rule configuration files, which are read by the **OverWatch Deployer**. You can place these configuration files in a folder named `rules` anywhere in your project directory. 

Otherwise, you can place the configuration files in a folder name of your choice - instructions on how to do this can be found [here](../../ow-pipeline-cdk/README.md#cdk-deploy-parameters)

## Usage
### Validator CLI
If you are using the validator standalone, and have imported the `ow-core/validator` folder to your project directory, you can use the following CLI arguments:
```
python3 project/validator.py --autofind
OR
python3 project/validator.py path/to/rules/folder
```
Otherwise, it is recommended the validator is used with OverWatch.

### Testing your rule configuration files 
If you need to test validation on your rule configurations, you are free to use any python testing frameworks. However, `pytest` is recommended. 

Import the validator into your testing script like so: 
```python
from validator import validator
from validator.validator import DuplicateNameException
from validator.validator import ValidationException
```

For each test, you may want to instatiate a validator object and check that your rules configuration files are valid like so: 
``` python
def test_validate():
    #Second arg is set to false since we do not want autofind - we are testing a specific rule files
    v = validator.OverwatchValidator('path/to/rules/folder', False)
    v.load_rules()
    #Provided your configuration files are correct
    assert v.validate() == (True, "All Rule Files Valid")
```

## FAQ
#### Can the validator be used on its own? 
* Yes. The validator can be treated as a standalone package if you are interested in a quick way to validate your YAML files. 
* Simply clone the `ow-core/validator` folder, and replace the `schema.yaml` file located in the `ow-core/validator/internal` folder with your own YAML schema. 

#### How do I enable autocomplete for my rules files in VSCode? 
* Install the YAML extension for VSCode which can be found [here](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
* Then, go to settings, and type in `Yaml: Schemas` and click on `"Edit in settings.json"`
* Then, provide the absolute path to the schema file in the extension settings. For example: 
```yaml
"yaml.schemas": {
  "/path/to/project/ow-core/validator/internal/schema.yaml",
}
```
* Save the file and reload VS Code. 
