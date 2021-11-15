import boto3
import yaml
import os
import argparse

cloudwatch=boto3.client('cloudwatch')
logs=boto3.client('logs')

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
SCHEMA_PATH = "ow-core/deployer/internal/schema.yaml"
# Path to Schema defaults
DEFAULT_PATH = "ow-core/deployer/internal/default.yaml"


class OverwatchDeployer:
    def __init__(self, rules_dir_path, autofind):
        self.rules_dir_path = str(self.find(rules_dir_path, os.path.abspath(os.curdir))) if autofind else rules_dir_path
        self.rules_dir_path += '/' # to make it proper filepath
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
                self.rules.append(filename)
        print(f"Loaded {', '.join(self.rules)}")

    def deploy_rules(self):
        for rule in self.rules:
            with open(self.rules_dir_path + rule, "r") as stream, open(DEFAULT_PATH, "r") as default:
                try:
                    current_rules = yaml.safe_load(stream)
                    default_rule = yaml.safe_load(default)
                except yaml.YAMLError as exc:
                    print(exc)
                except Exception as err:
                    exit(1)

                metric_fields={
                    "filterName":"",
                    "filterPattern":"",
                    "logGroupName":"",
                    "metricTransformations":"",
                }
                alarm_fields={
                    "ActionsEnabled":"",
                    "AlarmActions":"",
                    "AlarmDescription":"",
                    "AlarmName":"",
                    "ComparisonOperator":"",
                    "DatapointsToAlarm":"",
                    "Dimensions":"",
                    "EvaluateLowSampleCountPercentile":"",
                    "EvaluationPeriods":"",
                    "ExtendedStatistic":"",
                    "InsufficientDataActions":"",
                    "MetricName":"",
                    "Metrics":"",
                    "Namespace":"",
                    "OKActions":"",
                    "Period":"",
                    "Statistic":"",
                    "Tags":"",
                    "Threshold":"",
                    "ThresholdMetricId":"",
                    "TreatMissingData":"",
                    "Unit":"",
                }

                # print(default_rule['Metric'])
                # create metric filters for all alarms
                for current_rule in current_rules:
                    for field, value in list(metric_fields.items()):
                        if field in current_rule['Metric']:
                            metric_fields[field] = current_rule['Metric'][field]
                        else:
                            metric_fields[field] = default_rule['Metric'][field]
                            if metric_fields[field] == "" or metric_fields[field] == []:
                                del metric_fields[field]

                    # print(metric_fields)

                    try:
                        # Creating metric filter
                        logs.put_metric_filter(**metric_fields)
                    except Exception as err:
                        print("something went wrong creating metric filter")
                        exit(1)

                # deploy alarms
                for current_rule in current_rules:
                    for field, value in list(alarm_fields.items()):
                        if field in current_rule['Alarm']:
                            alarm_fields[field] = current_rule['Alarm'][field]
                        else:
                            alarm_fields[field] = default_rule['Alarm'][field]
                            if alarm_fields["MetricName"] == "":
                                alarm_fields["MetricName"] = metric_fields["metricTransformations"][0]["metricName"]
                            if alarm_fields["Namespace"] == "":
                                alarm_fields["Namespace"] = metric_fields["metricTransformations"][0]["metricNamespace"]
                            elif alarm_fields[field] == "" or alarm_fields[field] == []:
                                del alarm_fields[field]

                    # print(alarm_fields)

                    try:
                        # Creating CloudWatch Alarm
                        cloudwatch.put_metric_alarm(**alarm_fields)
                    except Exception as err:
                        print("something went wrong creating CloudWatch Alarm")
                        exit(1)

    def deploy(self):
        self.load_rules()
        self.deploy_rules()
    
if __name__ == "__main__":
    # parse the arguments
    args = parser.parse_args()

    # deployer class instance
    deployer = OverwatchDeployer(args.rules_folder_path, args.autofind)
    # if path given, attempt to deploy
    deployer.deploy()
