#!/usr/bin/env python3

from aws_cdk.core import App, Construct, Stack, RemovalPolicy, CfnParameter
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3


# OW Infrastructure Stack
class OverWatchInfraStack(Stack):
    artifactBucket = None  # Artifact Store S3 bucket
    artifactBucketAccessPolicy = None  # Artifact Store S3 Policy

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # parse any arguments
        rulesDirPath = CfnParameter(
            self,
            "rulesDirPath",
            default="rules",
            description="Path to rules folder | dirName of rules folder if autofind flag is set | Default: 'rules'",
        ).value_as_string
        autofind = CfnParameter(
            self,
            "enableAutofind",
            default="False",
            description="Enables autofind of rules yaml file for OverWatch if parameter is present (and not 'False')",
        ).value_as_string
        s3bucket = CfnParameter(
            self,
            "overWatchBucket",
            default="overwatchglobal",
            description="Bucket ARN of OverWatch source s3 bucket | Default: 'overwatchglobal' - maintained by dev team",
        ).value_as_string

        self.artifactBucket = s3.Bucket(
            self,
            "OverwatchArtifactBucket",
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        self.artifactBucketAccessPolicy = iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion", "s3:List*"],
            resources=[
                self.artifactBucket.bucket_arn + "*"
            ],  # need the "*" to be able get the source artis properly
            sid="overwatchArtifactBucketAccessPolicy",
        )


# OW Validation Stack
class OverWatchValidateStack(Stack):
    def __init__(
        self, scope: Construct, id: str, artifactStack: OverWatchInfraStack, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # parse any arguments
        rulesDirPath = CfnParameter(
            self,
            "rulesDirPath",
            default="rules",
            description="Path to rules folder | dirName of rules folder if autofind flag is set | Default: 'rules'",
        ).value_as_string
        autofind = CfnParameter(
            self,
            "enableAutofind",
            default="False",
            description="Enables autofind of rules yaml file for OverWatch if parameter is present (and not 'False')",
        ).value_as_string
        s3bucket = CfnParameter(
            self,
            "overWatchBucket",
            default="overwatchglobal",
            description="Bucket ARN of OverWatch source s3 bucket | Default: 'overwatchglobal' - maintained by dev team",
        ).value_as_string

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
                                "TMPDIR=$(mktemp -d)",
                                'echo "Syncing from OverWatch Bucket at $BUCKET to $TMPDIR"',
                                "aws s3 sync s3://$BUCKET $TMPDIR",
                                "pip install -r $TMPDIR/ow-core/validator/requirements.txt",
                            ],
                            "finally": ["echo OverWatch Validate Setup Complete"],
                        },
                        "build": {
                            "on-failure": "ABORT",
                            "commands": [
                                "echo Entered OverWatch Validate",
                                "chmod +x $TMPDIR/ow-core/validator/validator.py",
                                'python3 $TMPDIR/ow-core/validator/validator.py "$RULEPATH" "$AUTOFIND"',
                            ],
                            "finally": ["echo OverWatch Validate Complete"],
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            environment_variables={
                "RULEPATH": {"value": rulesDirPath},
                "AUTOFIND": {"value": "--autofind" if autofind != "False" else ""},
                "BUCKET": {"value": s3bucket},
            },
        )

        # validate codebuild project has the permissions to get S3 objects (for codepipeline)
        # artifact store s3 bucket access
        validate.add_to_role_policy(artifactStack.artifactBucketAccessPolicy)


# OW Deployment Stack
class OverWatchDeployStack(Stack):
    def __init__(
        self, scope: Construct, id: str, artifactStack: OverWatchInfraStack, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # parse any arguments
        rulesDirPath = CfnParameter(
            self,
            "rulesDirPath",
            default="rules",
            description="Path to rules folder | dirName of rules folder if autofind flag is set | Default: 'rules'",
        ).value_as_string
        autofind = CfnParameter(
            self,
            "enableAutofind",
            default="False",
            description="Enables autofind of rules yaml file for OverWatch if parameter is present (and not 'False')",
        ).value_as_string
        s3bucket = CfnParameter(
            self,
            "overWatchBucket",
            default="overwatchglobal",
            description="Bucket ARN of OverWatch source s3 bucket | Default: 'overwatchglobal' - maintained by dev team",
        ).value_as_string

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
                                "TMPDIR=$(mktemp -d)",
                                'echo "Syncing from OverWatch Bucket at $BUCKET to $TMPDIR"',
                                "aws s3 sync s3://$BUCKET $TMPDIR",
                                "pip install -r $TMPDIR/ow-core/deployer/requirements.txt",
                            ],
                            "finally": ["echo OverWatch Deployment Setup Complete"],
                        },
                        "build": {
                            "on-failure": "ABORT",
                            "commands": [
                                "echo Entered OverWatch Deploy",
                                "chmod +x $TMPDIR/ow-core/deployer/deployer.py",
                                'python3 $TMPDIR/ow-core/deployer/deployer.py "$RULEPATH" "$AUTOFIND"',
                            ],
                            "finally": ["echo OverWatch Deploy Complete"],
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            environment_variables={
                "RULEPATH": {"value": rulesDirPath},
                "AUTOFIND": {"value": "--autofind" if autofind != "False" else ""},
                "BUCKET": {"value": s3bucket},
            },
        )

        # deploy codebuild project has the permissions to get S3 objects (for codepipeline)
        # artifact store s3 bucket access
        deploy.add_to_role_policy(artifactStack.artifactBucketAccessPolicy)

        # deploy also needs access to create, delete and modify metric filters and alarms
        # Needs accesss to all resources since it's impossible to limit to very specific ARNS (not yet created)
        deployRulesAccessPolicy = iam.PolicyStatement(
            actions=["cloudwatch:*"],
            resources=[
                "*"
            ],  # need the "*" to be able get the source artis properly
            sid="overwatchDeployRulesCloudWatchAccessPolicy",
        )
        deploy.add_to_role_policy(deployRulesAccessPolicy)


# OW Application
class OverWatchService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        owInfraStack = OverWatchInfraStack(self, "ow-infra")
        owValidateStack = OverWatchValidateStack(self, "ow-validate", owInfraStack)

        owValidateStack.add_dependency(
            target=owInfraStack, reason="Require Infrastructure for OverWatch"
        )

        owDeployStack = OverWatchDeployStack(self, "ow-deploy", owInfraStack)

        owDeployStack.add_dependency(
            target=owValidateStack, reason="Require Validation for Deployment"
        )


# Begin OverWatch Service deployment
app = App()

# Filepaths
VALIDATOR_PATH = "./validator"
DEPLOYER_PATH = "./deployer"

# deploy the service
OverWatchService(app, "Overwatch-Service")
app.synth()
