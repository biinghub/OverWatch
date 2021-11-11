import jsonschema
from jsonschema.validators import Draft4Validator
import yaml
import os
import json
from jsonschema import validate
import boto3

#Custom Exception Handling for smoother debugging
class DuplicateNameException(Exception):
    def __init__(self, message):
        super().__init__(message)
class OverwatchValidator():
    def __init__(self, rules='rules.yaml'):
        self.rules = rules
    #Helper Function to allow developers to choose rules filename 
    def set_rules(self, rules):
        self.rules = rules

    #Taken from: https://stackoverflow.com/questions/1724693/find-a-file-in-python
    #Used to find path of 'rules.yaml' file in the root of user's project directory. 
    #Intelligently does this (no hardocded paths), thus, it does not matter whether user is on Windows or Linux
    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def load_rules(self): 
        #TODO - Add in warning for developers that the default rules file is 'rules.yaml' - however they can change this with set_rules()
        with open(str(self.find(self.rules, os.path.abspath(os.curdir)))) as f:
            rules = yaml.load(f, Loader=yaml.FullLoader)
        return json.dumps(rules)

    def validate_rules_structure(self): 
        with open(str(self.find('schema.yaml', os.path.abspath(os.curdir)))) as f:
            schema = yaml.load(f, Loader=yaml.FullLoader)
            try:
                rules = self.load_rules()
                cleaned_rules = json.loads(rules)
                validate(instance=cleaned_rules[0], schema=schema)
            except jsonschema.ValidationError as error:
                print(error)
                err = "Invalid Rules File"
                return False, err
            message = "Valid Rules File"
            return True, message

    def validate_alarm_attributes(self):
        rules = self.load_rules()
        cleaned_rules = json.loads(rules)
        alarmNames = []
        for rule in cleaned_rules:
            if rule['Alarm']['AlarmName'] not in alarmNames:
                alarmNames.append(rule['Alarm']['AlarmName'])
            else:
                raise DuplicateNameException("AlarmName must be unique.")
            
    def validate_metric_attributes(self):
        rules = self.load_rules()
        cleaned_rules = json.loads(rules)
        metricNames = []
        for rule in cleaned_rules:
            if rule['Metric']['filterName'] not in metricNames:
                metricNames.append(rule['Metric']['filterName'])
            else:
                raise DuplicateNameException("filterName must be unique.") 
    ''' Attempt at using Boto3 to get all filterNames and AlarmNames currently in cloud and compare with local rules file to avoid conflict
    def get_local_alarm_names(self):
        result = []
        rules = self.load_rules()
        cleaned_rules = json.loads(rules)
        for rule in cleaned_rules:
            result.append(rule['Metric']['filterName'])
        return result

    def get_local_metric_names(self):
        result = []
        rules = self.load_rules()
        cleaned_rules = json.loads(rules)
        for rule in cleaned_rules:
            result.append(rule['Alarm']['AlarmName'])
        return result 

    def validate_boto3_resources(self):
        cloudwatch = boto3.client('cloudwatch')
        logs = boto3.client('logs')
        local_alarm_names = self.get_local_alarm_names()
        local_metric_names = self.get_local_metric_names()
    '''

    def validate(self):
        #Any other functions that are apart of the validation process add it here
        self.validate_alarm_attributes()  
        self.validate_metric_attributes()
        is_valid, msg = self.validate_rules_structure()
        print(msg)

ow_validate1 = OverwatchValidator()

