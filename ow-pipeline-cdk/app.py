#!/usr/bin/env python3

from aws_cdk.core import App, Construct, Stack
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_iam as iam

# S3 Access Policy
s3AccessPolicy = iam.PolicyStatement(
    actions=["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion", "s3:List*"],
    resources=["*"],
    sid="S3AccessPolicy",
)


# OW Validation Stack
class OverWatchValidateStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        validate = codebuild.PipelineProject(
            self,
            "ow-validate",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": 0.2,
                    "phases": {
                        "install": {
                            "on-failure": "ABORT",
                            "commands": [
                                "echo Entered OverWatch Validate Setup",
                                "pip install boto3",
                                "pip install json-schema==0.3 jsonschema==4.1.2 PyYAML==6.0",
                            ],
                            "finally": ["echo OverWatch Validate Setup Complete"],
                        },
                        "build": {
                            "on-failure": "ABORT",
                            "commands": [
                                "python demo/mylibrary/validator.py"  # TODO: Protect against fake file, perhaps do some temp directory trickery?
                            ],
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0
            ),
            # TODO: Potentially put overwatch logs into Cloudwatch?
        )

        # validate codebuild project has the permissions to get S3 objects (for codepipeline)
        # global s3 bucket access
        validate.add_to_role_policy(s3AccessPolicy)


# OW Deployment Stack
class OverWatchDeployStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        deploy = codebuild.PipelineProject(
            self,
            "ow-deploy",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": 0.2,
                    "phases": {
                        "install": {
                            "on-failure": "ABORT",
                            "commands": [
                                "echo Entered OverWatch Deployment Setup",
                                "pip install boto3",
                            ],
                            "finally": ["echo OverWatch Deployment Setup Complete"],
                        },
                        "build": {
                            "on-failure": "ABORT",
                            "commands": ["python -c 'print(\"hello world!\")'"],
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0
            ),
            # TODO: Potentially put overwatch logs into Cloudwatch?
        )

        # deploy codebuild project has the permissions to get S3 objects (for codepipeline)
        # global s3 bucket access
        deploy.add_to_role_policy(s3AccessPolicy)


# OW Application
class OverWatchService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        owValidateStack = OverWatchValidateStack(self, "ow-validate")
        owDeployStack = OverWatchDeployStack(self, "ow-deploy")

        owDeployStack.add_dependency(
            target=owValidateStack, reason="Require Validation for Deployment"
        )
        # TODO: Potentially put overwatch logs into Cloudwatch?


# Begin OverWatch Service deployment
app = App()
OverWatchService(app, "Overwatch-Service")
app.synth()
