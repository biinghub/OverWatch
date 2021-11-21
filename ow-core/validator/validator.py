import jsonschema
import yaml
import json
import os
import argparse

SCHEMA_PATH = f"ow-core/validator/internal/schema.yaml"

"""
Arguments Engine - defining CLI parameters for customisability with validator script 
i.e. python validator.py --autofind
"""
parser = argparse.ArgumentParser(description="OverWatch Rules Validator")
parser.add_argument(
    "rules_folder_path",
    metavar="path",
    type=str,
    nargs="?",
    default="rules",
    help='Path to rules folder | dirName of rules folder if autofind flag is set | Default: "rules"',
)
parser.add_argument(
    "--directory",
    type=str,
    nargs="?",
    default=".",
    help='Path to OverWatch Core Application | Default "." or Current Directory',
)
parser.add_argument(
    "--autofind",
    dest="autofind",
    action="store_true",
    help="Enables autofinding of <rules_folder_path> directory within project",
)


class DuplicateNameException(Exception):
    """
    DuplicateNameException - is raised when there are duplicate AlarmNames or filterNames in rules folder
    """

    def __init__(self, message):
        super().__init__(message)


class ValidationException(Exception):
    """
    ValidationException - is raised when there is a syntax or type issue with configurations in rules folder
    """

    def __init__(self, message):
        super().__init__(message)


class OverwatchValidator:
    """
    OverWatch Valitor Class - defined to make use of the validator more extensible and essentially be used as a 'microservice',
    so people can use it in code and test scripts easily
    """

    def __init__(self, rules_dir_path, autofind):
        """
        Constructor - by default will the rules directory should be specified, otherwise the --autofind tag will search for a 'rules' folder and
        assign it to attributes of Overwatch Validator class
        """
        self.rules_dir_path = (
            str(self.find(rules_dir_path, os.path.abspath(os.curdir)))
            if autofind
            else rules_dir_path
        )
        self.rules_dir_path += "/"
        self.rules = []

    def find(self, name, path):
        """
        Taken from: https://stackoverflow.com/questions/1724693/find-a-file-in-python
        Finds rules folder depending on folder name provided - utilizing os module to do this regardless of user's OS i.e. no hardcoding
        Returns a reference to file
        """
        for root, dirs, files in os.walk(path):
            if name in dirs:
                return os.path.join(root, name)

    def load_rules(self):
        """
        Using the find() function, will use yaml parser and json.dumps to convert into readable python data structure
        Returns all rules files in rules folder and assigns them to class rules attribute
        """
        for filename in os.listdir(self.rules_dir_path):
            if filename.endswith(".yaml"):
                with open(self.rules_dir_path + filename) as f:
                    self.rules.append(
                        (filename, json.dumps(yaml.load(f, Loader=yaml.FullLoader)))
                    )
        print(f"Loaded {', '.join(n[0] for n in self.rules)}")

    def validate_rules_structure(self):
        """
        Uses jsonschema pypi package to validate structure of schema.
        The schema was defined with jsonschema.net, however modified quite a lot to add in
        required fields and enums
        Returns tuple - (True, "All Rules Files Valid") if the structure is OK, otherwise wil throw validation error and message
        """
        with open(SCHEMA_PATH) as f:
            schema = yaml.load(f, Loader=yaml.FullLoader)
            for filename, rule_bundle in self.rules:
                try:
                    cleaned_rules = json.loads(rule_bundle)
                    for cleaned_rule in cleaned_rules:
                        jsonschema.validate(instance=cleaned_rule, schema=schema)
                except (jsonschema.ValidationError, KeyError) as error:
                    print(error)
                    return False, f"Invalid Rules File - {filename} - Schema Error"
            return True, "All Rules Files Valid"

    def validate_alarm_attributes(self):
        """
        Similar to validate_rules_structure, however checks for duplicate AlarmNames in rules folder
        Returns list of all AlarmName in rules folder
        """
        alarmNames = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                try:
                    if clean_rule["Alarm"]["AlarmName"] not in alarmNames:
                        alarmNames.append(clean_rule["Alarm"]["AlarmName"])
                    else:
                        raise DuplicateNameException(
                            f"AlarmName must be unique. Conflict with '{clean_rule['Alarm']['AlarmName']}' in '{filename}'"
                        )
                except Exception as err:
                    raise ValidationException(
                        f"'{filename}' is an Invalid Rules File - err: {err}"
                    )

        return alarmNames

    def validate_metric_attributes(self):
        """
        Similar to validate_rules_structure, however checks for duplicate filterName in rules folder
        Returns list of all filterNames in rules folder
        """
        metricNames = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                try:
                    if clean_rule["Metric"]["filterName"] not in metricNames:
                        metricNames.append(clean_rule["Metric"]["filterName"])
                    else:
                        raise DuplicateNameException(
                            f"filterName must be unique. Conflict with '{clean_rule['Metric']['filterName']}' in '{filename}'"
                        )
                except Exception as err:
                    raise ValidationException(
                        f"'{filename}' is an Invalid Rules File - err: {err}"
                    )
        return metricNames

    def get_local_alarm_names(self):
        """
        Helper function for developer testing
        Returns list of all filterNames defined in rules
        """
        result = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                result.append(clean_rule["Metric"]["filterName"])
        return result

    def get_local_metric_names(self):
        """
        Helper function for developer testing
        Returns list of all AlarmNames
        """
        result = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                result.append(clean_rule["Alarm"]["AlarmName"])
        return result

    def validate(self):
        """
        For customisability, any extra measures to the validation build, add underneath self.load_rules()
        Function executes all relevant steps in the OverwatchValidator class to ensure the rules folder contains valid rule configurations
        """
        self.load_rules()
        self.validate_alarm_attributes()
        self.validate_metric_attributes()
        is_valid, msg = self.validate_rules_structure()
        print(msg)
        if not is_valid:
            exit(1)
        exit(0)


if __name__ == "__main__":
    """
    Parses arguments, instantiates OverwatchValidator class depending on arguments, and runs validate() step
    This is mainly for integration within Overwatch CDK.
    """
    args = parser.parse_args()

    # Path to Schema
    SCHEMA_PATH = f"{args.directory}/ow-core/validator/internal/schema.yaml"

    # validator class instance
    validator = OverwatchValidator(args.rules_folder_path, args.autofind)
    # if path given, attempt to validate
    validator.validate()
