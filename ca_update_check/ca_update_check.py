#This lambda function will download an HTML page and parse the page looking for the string "Last Updated" and date in the string
#It will check against an SSM parameter store to see if the date is the same as the last time the function was run
#If the date is different, it will update the SSM parameter store with the new date and send an SNS notification
#If the date is the same, it will do nothing and return a success message
#The SNS notification will be sent to a SNS topic that is subscribed to the lambda function
#The SNS topic will be used to send an email to the user with the new date



import json
import urllib.request
import re
import boto3
import os
from urllib.parse import urlparse


def lambda_handler(event, context):
    
    url = "https://aws.amazon.com/agreement/"
    parsed_url = urlparse(url)

    if parsed_url.scheme in ["http", "https"]:
        html = urllib.request.urlopen(url).read() #nosec
        html = html.decode('utf-8')
    else:
        raise ValueError("Invalid URL scheme. Only HTTP and HTTPS are allowed.")
    pattern = r"Last Updated\s*:\s*(\w+ \d{1,2}, \d{4})"
    
    # Search for the pattern in the HTML content
    match = re.search(pattern, html)
    
    # If a match is found, extract the date
    if match:
        last_updated_date = match.group(1)

        # Connect to SSM parameter
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(Name='/customer_agreement_last_updated_date')
        last_updated_date_from_ssm = response['Parameter']['Value']
        
        if last_updated_date_from_ssm == last_updated_date:
            print("Date in SSM parameter matches the date in the HTML content")

        else:
            print("Date in SSM does not match the date in the HTML content")
            ssm.put_parameter(Name='/customer_agreement_last_updated_date', Value=last_updated_date, Type='String',Overwrite=True)

            # Connect to SNS
            sns = boto3.client('sns')
            sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
            sns.publish(TopicArn=sns_topic_arn, Message="New AWS customer agreement posted. See https://aws.amazon.com/agreement/recent-changes/")

    return {
            'statusCode': 200
    }
