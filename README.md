# AWS Customer Agreement Update Checker

This repository contains a simple solution to check and notify when it detects a change to the AWS customer agreement posted at https://aws.amazon.com/agreement/


The solution uses an Amazon EventBridge rule which triggers a Lambda function daily. This function stores the "Last Updated" date specified on the agreement page in an SSM parameter and compares the date found with the stored parameter. When a new date is detected, an SNS notification is sent to the email addresses subscribed to the topic.

This sample can be modified with any additional requirements.

## Deployment

### Clone the repository
`git clone git@github.com:aws-samples/aws-customer-agreement-update-checker.git`

### Navigate to the cloned repository
`cd aws-customer-agreement-update-checker`

### Run the cloudformation package command
`aws cloudformation package --template-file cloudformation.yml --s3-bucket <bucket_name> --output-template-file packaged.yaml`
Replace the <bucket_name> with an existing bucket name in your account

### Deploy the CloudFormation stack
`aws cloudformation deploy --template-file packaged.yaml --stack-name aws-ca-update-checker-stack --parameter-overrides "NotificationEmailAddress=pat_candella@example.org" --capabilities CAPABILITY_IAM`

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

