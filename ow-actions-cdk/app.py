#!/usr/bin/env python3

from aws_cdk.core import App, Construct, Stack, CfnParameter
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as subscriptions

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class OverWatchEmailSNS(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(self, "OverWatch Email")
        notif_email = CfnParameter(self, "emailparam", allowed_pattern=EMAIL_REGEX, description="Email to be sent SNS notification")

        topic.add_subscription(subscriptions.EmailSubscription(notif_email.value_as_string))


app = App()
OverWatchEmailSNS(app, "OverWatch-Email-SNS")
app.synth()
