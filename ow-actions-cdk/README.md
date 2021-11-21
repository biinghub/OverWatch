
# OverWatch Core CDK

This is the OverWatch Sample Actions CDK project which will deploy a sample email notification via AWS SNS.

Team 3 **strongly recommends** you utilise the AWS Console to create the SNS Topics and Lambda Functions as using an IaC solution is not very usable without significant investment in a creation script.
This is out of scope for OverWatch so please consider the above and proceed as necessary.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now deploy the OverWatch Sample Actions to your AWS account.

```
$ cdk deploy --all --parameters emailparam=<notif-email-here>
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## CDK Deploy Parameters

OverWatch Sample Actions also provides some parameters for you to change certain behaviour:

* `email-param`         email to receive the SNS notification | Required to give a valid email to deploy
```
$ cdk deploy --all --parameters emailparam=beffjezos9447@gmail.com
```

## Other Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## FAQ
### Deployment isn't working
* Ensure you are on an AWS shell environment and the user profile has sufficient permissions to deploy infrastructure to the account.
* Team 3 also recommends that you create a custom user on AWS to own/manage all OverWatch related infrastructure.

### Parameters do not seem to be resetting when redeploying
* Try adding in the following option to the deployment command:
```
$ cdk deploy --all --parameters emailparam=<notif-email-here> --no-previous-parameters
```
