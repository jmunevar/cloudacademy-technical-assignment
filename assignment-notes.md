# Cloud Academy - Lab Operations Specialist Assignment

[TOC]

## Create CloudFormation Stack A

### Task 1: Resolve CloudFormation Stack Deployment Errors

#### Resolve IAM User Creation Errors

Initially, CloudFormation template `cloudformationA.yaml` failed due to
providing a password in the "UserConfig.Login" mapping not meeting the minimum
IAM user password requirements [^1] [^2] including having at least one upper case
letter, one number, and having a minimum length of 12 characters:

```text
Password should have at least one uppercase letter (Service: AmazonIdentityManagement;
Status Code: 400; Error Code: PasswordPolicyViolation;
Request ID: <redacted>; Proxy: null)
```

```text
Password should have at least one number (Service: AmazonIdentityManagement;
Status Code: 400; Error Code: PasswordPolicyViolation;
Request ID: <redacted>; Proxy: null)
```

```text
Password should have a minimum length of 12 (Service: AmazonIdentityManagement;
Status Code: 400; Error Code: PasswordPolicyViolation;
Request ID: <redacted>; Proxy: null)
```

In order to resolve the relevant errors, I generated a random password using
the AWS CLI and AWS Secrets Manager's "get-random-password" API [^3]; I provided
a Bash script, `aws_sm_get_random_password.sh` as an example using both tools.
I also provided a sample Python script, `generate_random_password.py`, to
generate a random alphanumeric password without a AWS managed service.


#### Resolve Lambda function creation errors

Next, CloudFormation template `cloudformationA.yaml` failed due to using a
deprecated version of the Node.js runtime for AWS Lambda, "nodejs6.10". The
error message recommended using the newest Node.js runtime, "nodejs14.x" [^4],
when creating or updating Lambda functions:

```text
Resource handler returned message: "The runtime parameter of nodejs6.10 is no
longer supported for creating or updating AWS Lambda functions. We recommend
you use the new runtime (nodejs14.x) while creating or updating functions.
(Service: Lambda, Status Code: 400, Request ID: <redacted>, Extended Request
ID: null)" (RequestToken: <redacted>, HandlerErrorCode: InvalidRequest)
```

After trying the oldest supported runtime for Node.js ("nodejs10.x") and
observing the same error, I tried "nodejs12.x", which allowed the Lambda
function creation to complete successfully. [^5]


### Task 2: Add missing IAM permissions for read-only access on DynamoDB items

The next issue of DynamoDB access for the student user was resolved by
adding the minimal IAM permissions to the relevant IAM group used for managing
access for viewing and querying/scanning through DynamoDB items. [^6] [^7] I
logged into the student account in the AWS Management Console and verified
access to the relevant DynamoDB table and its items that were added separately
by an admin user account.


## Create CloudFormation Stack B

### Task 3: Resolve Jenkins' SNS & Git plugin errors

#### Update CloudFormation template's user data script

For CloudFormation template `cloudformationB.yaml`, the Jenkins web application
 hosted on the deployed EC2 instance displayed several errors related to its
installed AWS SNS and Git plugins:

```text
Some plugins could not be loaded due to unsatisfied dependencies.
Fix these issues and restart Jenkins to re-enable these plugins.

Dependency errors:

Amazon SNS Build Notifier (2.0)
    Jenkins (2.263.1) or higher required

Jenkins Git plugin (4.8.3)
    Jenkins (2.263.1) or higher required

Jenkins Git client plugin (3.9.0)
    Jenkins (2.263.1) or higher required

Some of the above failures also result in additional indirectly dependent
plugins not being able to load.

Indirectly dependent plugins:

Git plugin (4.8.3)
    Failed to load: Jenkins Git client plugin (3.9.0)
```

After reviewing the relevant error message and version of Jenkins installed
through a deb package installer, I replaced the deprecated version,
"jenkins_2.249.3_all.deb", with a more recent Jenkins version,
"jenkins_2.303.2_all.deb", available from the relevant S3 bucket into
the user data script section of the CloudFormation template. I ran the
following AWS CLI command to get a list of available Jenkins deb package
installers from the relevant S3 bucket:

```shell
aws s3api list-objects --bucket clouda-labs-assets | grep 'jenkins'
```

After deploying the relevant CloudFormation template again, the previous
errors were nonexistent in the Jenkins web app, in addition to several
security vulnerabilities listed for that older version of Jenkins.

#### Alternative resolution through downgrading any incompatible plugins based on the initial Jenkins version

1. For example, download an older Git plugin version [^8]
based on initial Jenkins version "2.249.3" and the most recent version of the
Git plugin [^9] that supports that Jenkins version.
2. Install the the older plugin version manually. [^10]

Note: This alternative method is not recommended as staying on the older
version of Jenkins is not recommended from a security perspective. There were
several known security vulnerabilities listed on the Jenkins web app itself,
and that older version may be vulnerable to the recent log4j2 vulnerability,
"Log4Shell", affecting Java based software including Jenkins plugins. [^11]

#### Suggestions to improve the relevant CloudFormation template

- Perhaps substituting the configured AZ, 'us-west-2a', with a dynamic parameter
like 'AWS::REGION' [^12] to generate a valid AZ for that AWS Region at stack
deployment.


## Python Comprehension

### Task 4: Evaluate and summarize Python code using Azure SDK

- From the "handler" function name, the code seems to be a Azure function,
which, like AWS Lambda or Google Cloud Functions, accept an "event" and
"context" object in the function signature from the current function execution
environment.
- The "event" object in the sample code is used to extract "credentials",
"subscription_id", and "resource_group" objects used to generate client objects
and interact with the Azure Recovery Services API and Azure Recovery Services
Backup API.
- The main part of the code involves getting a list of Azure Recovery Services
vaults by resource group, iterating for backup jobs on each vault and
resource group, and then returning a "True" boolean object if a back job's
operation type is a restore operation.


## References

[^1]: [AWS Documentation - IAM > API Reference > CreateLoginProfile](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateLoginProfile.html)

[^2]: [AWS Documentation - IAM > CLI Reference > CreateLoginProfile](https://docs.aws.amazon.com/cli/latest/reference/iam/create-login-profile.html)

[^3]: [AWS Documentation - SecretsManager > API Reference > GetRandomPassword](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/secretsmanager/get-random-password.html)

[^4]: [AWS Blog - Node.js 14.x Runtime Now Available in AWS Lambda](https://aws.amazon.com/blogs/compute/node-js-14-x-runtime-now-available-in-aws-lambda/)

[^5]: [AWS Documentation - AWS Lambda > Developer Guide > Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)

[^6]: [AWS Documentation - AWS DynamoDB > Developer Guide > Read-Only Access on Items](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-only-permissions-on-table-items.html)

[^7]: [AWS Documentation - Service Authorization Reference > DynamoDB](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazondynamodb.html)

[^8]: [Jenkins Project - Downloads > Plugins > Git](https://updates.jenkins.io/download/plugins/git/)

[^9]: [GitHub - "jenkinsci/git-plugin" repo > Releases](https://github.com/jenkinsci/git-plugin/releases)

[^10]: [Jenkins Project - Documentation > Managing Plugins > Advanced Installation](https://www.jenkins.io/doc/book/managing/plugins/#advanced-installation)

[^11]: [VentureBeat - Major attacks using Log4j vulnerability ‘lower than expected’](https://venturebeat.com/2022/01/24/major-attacks-using-log4j-vulnerability-lower-than-expected/)

[^12]: [AWS Documentation - User Guide > CloudFormation > Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
