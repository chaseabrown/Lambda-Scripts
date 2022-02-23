import boto3
import uuid
import botocore
import re

def cleanNumber(number):
    allNumber = re.sub("[^0-9]", "", number)
    return (allNumber[:3] + "-" + allNumber[3:6] + "-" + allNumber[6:])

def lambda_handler(event, context):
    # this will create dynamodb resource object and
    # here dynamodb is resource name
    client = boto3.resource('dynamodb')

    #generate UUID
    recordId = str(uuid.uuid4()).replace("-", "")
    # this will search for dynamoDB table
    # your table name may be different
    table = client.Table("users")

    count = 0
    success = False
    while count<3:
        try:
            table.put_item(
                Item={
                    'userID' : recordId,
                    'username' : event['queryStringParameters']['username'],
                    #This was before adding Cognito to the application. This is not how I would add passwords on a real project. This was just to fill a temporary database for other features
                    'password' : event['queryStringParameters']['password'],
                    'email' : event['queryStringParameters']['email'],
                    'phone' : cleanNumber(event['queryStringParameters']['phone']),
                    'age' : event['queryStringParameters']['age'],
                    'universityID' : event['queryStringParameters']['email'].split("@")[1].split(".")[0],
                    'profilePictureAddress' : "https://stumeetwebapp.s3.eu-central-1.amazonaws.com/user-profile-pics/" + event['queryStringParameters']['username'] + ".jpg",
                    'eventsOrganized' : [],
                    'eventsAttending' : [],
                    'eventsMaybe' : []
                },
                ConditionExpression='attribute_not_exists(userID)'
            )
            return {
                'statusCode': 200,
                'body': recordId
            }
        except botocore.exceptions.ClientError as e:
            recordId = str(uuid.uuid4()).replace("-", "")
            count += 1

    return {
        'statusCode': 500,
        'body': "Server Failed to Generate Unique ID. Please Try Again."
    }
