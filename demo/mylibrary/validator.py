import jsonschema
from jsonschema.validators import Draft4Validator
import yaml
import os
import json
from jsonschema import validate

#Taken from: https://stackoverflow.com/questions/1724693/find-a-file-in-python
#Used to find path of 'rules.yaml' file in the root of user's project directory. 
#Intelligently does this (no hardocded paths), thus, it does not matter whether user is on Windows or Linux
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def load_rules(): 
    with open(str(find('simple_rules_example.yaml', os.path.abspath(os.curdir)))) as f:
        rules = yaml.load(f, Loader=yaml.FullLoader)
    return json.dumps(rules)

def validate_rules_structure(): 
    with open(str(find('schema.yaml', os.path.abspath(os.curdir)))) as f:
        schema = yaml.load(f, Loader=yaml.FullLoader)
        try:
            rules = load_rules()
            cleaned_rules = json.loads(rules)
            validate(instance=cleaned_rules[0], schema=schema)
        except jsonschema.ValidationError as err:
            print(err)
            err = "Invalid Rules File"
            return False, err
        message = "Valid Rules File"
        return True, message

def validate_alarm_attributes():
    rules = load_rules()
    cleaned_rules = json.loads(rules)
    alarmNames = []
    for rule in cleaned_rules:
        if rule['Alarm']['AlarmName'] not in alarmNames:
            alarmNames.append(rule['Alarm']['AlarmName'])
        else:
            print("not unique")
        #Add in uniqeness checks here

def validate_metric_attributes():
    rules = load_rules()
    cleaned_rules = json.loads(rules)
    metricNames = []
    for rule in cleaned_rules:
        if rule['Metric']['filterName'] not in metricNames:
            metricNames.append(rule['Metric']['filterName'])
        else:
            print("not unique")
validate_alarm_attributes()  
validate_metric_attributes()
is_vald, msg = validate_rules_structure()
print(msg)



