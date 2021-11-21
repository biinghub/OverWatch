import boto3
import time
import enum

# Deployment Instance requires these AWS permissions:
# logs:DescribeLogStreams
# logs:PutLogEvents
# logs:CreateLogGroup
# logs:CreateLogStream

DEFAULT_LOG_GROUP = "/var/log/Overwatch"

# Currently supported priority levels (customisable to product needs)
class Priority(enum.Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"
    DEBUG = "DEBUG"


class OverWatch_Logger:
    def __init__(self, logGroup=DEFAULT_LOG_GROUP):
        self.logGroup = logGroup
        self.client = boto3.client("logs")

        # create log group if not already existing
        try:
            self.client.create_log_group(logGroupName=self.logGroup)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def __send_log(
        self, priority: Priority, application: str, eventPrefix: str, message: str
    ):
        # create log stream if not already existing
        logStream = f"{time.strftime('%Y-%m-%d')}-logstream"
        try:
            self.client.create_log_stream(
                logGroupName=self.logGroup, logStreamName=logStream
            )
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

        # https://stackoverflow.com/questions/30897897/python-boto-writing-to-aws-cloudwatch-logs-without-sequence-token/32947579
        # Not going to reinvent the wheel here
        log_stream_description = self.client.describe_log_streams(
            logGroupName=self.logGroup, logStreamNamePrefix=logStream
        )

        # generate event log
        event_log = {
            "logGroupName": self.logGroup,
            "logStreamName": logStream,
            "logEvents": [
                {
                    "timestamp": int(round(time.time() * 1000)),
                    "message": f"{priority} - {application} - {eventPrefix} : {message}",
                }
            ],
        }

        # upload log (cursed sequence log bs done as well)
        if "uploadSequenceToken" in log_stream_description["logStreams"][0]:
            event_log.update(
                {
                    "sequenceToken": log_stream_description["logStreams"][0][
                        "uploadeSequenceToken"
                    ]
                }
            )

        # actually upload to Cloudwatch
        res = None
        try:
            res = self.client.put_log_events(**event_log)
        except Exception as err:
            print(err)

    def monitor_event(
        self, priority: Priority, application: str, eventPrefix: str, message: str
    ):
        """
        Send Activity Log to OverWatch

        priority: Priority - priority of event (enum from SDK)
        application: str - application name
        eventPrefix: str - unique prefix to identify specific event type
        message: str - message for log
        """
        self.__send_log(priority, application, eventPrefix, message)
