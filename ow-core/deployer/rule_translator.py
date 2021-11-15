import boto3
import yaml
import os

cloudwatch=boto3.client('cloudwatch')
logs=boto3.client('logs')

rules=[]

for filename in os.listdir("rules"):
    if filename.endswith(".yaml") and filename != "default.yaml" and filename != "schema.yaml":
        rules.append(filename)
    else:
        continue


for rule in rules:
    with open("rules/"+rule, "r") as stream, open("rules/default.yaml", "r") as default:
        try:
            current_rule = yaml.safe_load(stream)
            default_rule = yaml.safe_load(default)
        except yaml.YAMLError as exc:
            print(exc)

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

        for field, value in list(metric_fields.items()):
            if field in current_rule['Metric']:
                metric_fields[field] = current_rule['Metric'][field]
            else:
                metric_fields[field] = default_rule['Metric'][field]
                if metric_fields[field] == "" or metric_fields[field] == []:
                    del metric_fields[field]

        print(metric_fields)

        try:
            # Creating metric filter
            logs.put_metric_filter(**metric_fields)
        except ValueError:
            print("something went wrong creating metric filter")

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

        print(alarm_fields)

        try:
            # Creating CloudWatch Alarm
            cloudwatch.put_metric_alarm(**alarm_fields)
        except ValueError:
            print("something went wrong creating CloudWatch Alarm")
