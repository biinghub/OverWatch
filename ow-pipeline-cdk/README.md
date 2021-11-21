
# OverWatch Core CDK

This is the OverWatch Core CDK project which will deploy the necessary infrastructure and projects to be able to utilise OverWatch on your AWS account.

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

At this point you can now synthesize the CloudFormation template for OverWatch Core.

```
$ cdk synth
```

Alternatively, you can deploy the OverWatch Core to your AWS account.

```
$ cdk deploy --all
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## CDK Deploy Parameters

OverWatch Core also provides some parameters for you to change certain aspects of the core behaviour:

* `autofind`         enables autofind of rules yaml file for OverWatch if parameter is present (and not 'False')
```
$ cdk deploy --all --parameters enableAutofind=True
```

* `rulesDirPath`     specify the path to the rules directory | specify the directory name if autofind is enabled
```
# autofind disabled
$ cdk deploy --all --parameters rulesDirPath=this-dir-is-on-top-level/rules

# autofind enabled
$ cdk deploy --all --parameters rulesDirPath=example --parameters enableAutofind=True
```

* `overWatchBucket`  specify the s3 bucket name from which OverWatch core scripts will be synced from if hosting OverWatch core scripts locally | defaults to 'overwatchglobal' maintained by dev
```
$ cdk deploy --all --parameters overWatchBucket=<bucket-name-here>
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
$ cdk deploy --all --no-previous-parameters
```
