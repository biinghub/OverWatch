import jsonschema
import yaml
import json
import os
import argparse

# Arguments Engine
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
    "--autofind",
    dest="autofind",
    action="store_true",
    help="Enables autofinding of <rules_folder_path> directory within project",
)

# Path to Schema
SCHEMA_PATH = "ow-core/validator/internal/schema.yaml"

# Custom Exception Handling for smoother debugging
class DuplicateNameException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class OverwatchValidator:
    def __init__(self, rules_dir_path, autofind):
        self.rules_dir_path = (
            str(self.find(rules_dir_path, os.path.abspath(os.curdir)))
            if autofind
            else rules_dir_path
        )
        self.rules_dir_path += "/"  # to make it proper filepath
        self.rules = []

    # Taken from: https://stackoverflow.com/questions/1724693/find-a-file-in-python
    # Finds rules folder depending on folder name provided
    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in dirs:
                return os.path.join(root, name)

    def load_rules(self):
        for filename in os.listdir(self.rules_dir_path):
            if filename.endswith(".yaml"):
                with open(self.rules_dir_path + filename) as f:
                    self.rules.append(
                        (filename, json.dumps(yaml.load(f, Loader=yaml.FullLoader)))
                    )
        print(f"Loaded {', '.join(n[0] for n in self.rules)}")

    def validate_rules_structure(self):
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

    # get_local_alarm_names and get_local_metric_names are simply helper functions for developers
    # these two functions are NOT used in validation step
    def get_local_alarm_names(self):
        result = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                result.append(clean_rule["Metric"]["filterName"])
        return result

    def get_local_metric_names(self):
        result = []
        for filename, rule in self.rules:
            cleaned_rules = json.loads(rule)
            for clean_rule in cleaned_rules:
                result.append(clean_rule["Alarm"]["AlarmName"])
        return result

    def validate(self):
        # Any other functions that are apart of the validation process add it here
        self.load_rules()
        self.validate_alarm_attributes()
        self.validate_metric_attributes()
        is_valid, msg = self.validate_rules_structure()
        # TODO: perhaps actual and real error messaging?
        print(msg)
        if not is_valid:
            exit(1)
        exit(0)


if __name__ == "__main__":
    # parse the arguments
    args = parser.parse_args()

    # validator class instance
    validator = OverwatchValidator(args.rules_folder_path, args.autofind)
    # if path given, attempt to validate
    validator.validate()
