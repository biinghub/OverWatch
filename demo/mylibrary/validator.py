import yaml
import os
from cerberus import Validator


#Refer to https://docs.python-cerberus.org/en/stable/customize.html#validator-schema
#Used this to create custom validator methods 
class overWatchValidator(Validator):
    def foo():
        return 0

#Taken from: https://stackoverflow.com/questions/1724693/find-a-file-in-python
#Used to find path of 'rules.yaml' file in the root of user's project directory. 
#Intelligently does this (no hardocded paths), thus, it does not matter whether user is on Windows or Linux
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def load_rules(): 
    with open(str(find('rules.yaml', os.path.abspath(os.curdir)))) as f:
        rules = yaml.load(f, Loader=yaml.FullLoader)
        return rules 

schema = eval(open('demo\mylibrary\schema.py', 'r').read()) 
v = Validator(schema)
rules = load_rules()
print(v.validate(rules, schema))
print(v.errors)

