import boto3
import uuid
import boto3.dynamodb.conditions as conditions
from botocore.exceptions import ClientError
import datetime

def lambda_handler(event, context):
    # this will create dynamodb resource object and
    # here dynamodb is resource name
    client = boto3.resource('dynamodb')

    #generate UUID
    recordId = str(uuid.uuid4()).replace("-", "")
    # this will search for dynamoDB table
    # your table name may be different
    table = client.Table("events")
    userTable = client.Table("users")

    usersAttending = []
    usersMaybe = []

    if event['queryStringParameters']['RSVP'] == "Attending":
        usersAttending.append(event['queryStringParameters']['organizer'])
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['organizer'],
                },
                UpdateExpression="SET #o = list_append(#o, :eventID)",
                ExpressionAttributeNames={
                    "#o": "eventsAttending",
                },
                ExpressionAttributeValues={
                    ":eventID": [recordId]
                },
                ConditionExpression=conditions.Attr("userID").exists()

            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Update User Table (eventsAttending)"
            }
    elif event['queryStringParameters']['RSVP'] == "Maybe":
        usersMaybe.append(event['queryStringParameters']['organizer'])
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['organizer'],
                },
                UpdateExpression="SET #o = list_append(#o, :eventID)",
                ExpressionAttributeNames={
                    "#o": "eventsMaybe",
                },
                ExpressionAttributeValues={
                    ":eventID": [recordId]
                },
                ConditionExpression=conditions.Attr("userID").exists()

            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Update User Table (eventsMaybe)"
            }

    count = 0
    success = False

    while count<3:
        try:
            table.put_item(
                Item={
                    "eventID" : recordId,
                    "eventName" : event['queryStringParameters']['eventName'],
                    "organizer" : event['queryStringParameters']['organizer'],
                    "locationCords" : event['queryStringParameters']['locationCords'],
                    "city" : event['queryStringParameters']['city'],
                    "country" : event['queryStringParameters']['country'],
                    "entryFee" : event['queryStringParameters']['entryFee'],
                    "dressCode" : event['queryStringParameters']['dressCode'],
                    "description" : event['queryStringParameters']['description'],
                    "datetime" : str(datetime.datetime.utcnow()),
                    "iconPictureAddress" : "https://stumeetwebapp.s3.eu-central-1.amazonaws.com/event-profile-pics/" + recordId + ".jpg",
                    "usersAttending" : usersAttending,
                    "usersMaybe" : usersMaybe,
                    "postIDs" : []
                },
                ConditionExpression='attribute_not_exists(eventID)'
            )


            try:
                userTable.update_item(
                    Key={
                        "userID": event['queryStringParameters']['organizer'],
                    },
                    UpdateExpression="SET #o = list_append(#o, :eventID)",
                    ExpressionAttributeNames={
                        "#o": "eventsOrganized",
                    },
                    ExpressionAttributeValues={
                        ":eventID": [recordId]
                    },
                    ConditionExpression=conditions.Attr("userID").exists()

                )
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': "Server Failed to Update User Table (eventsOrganized)"
                }

            return {
                'statusCode': 200,
                'body': recordId
            }
        except ClientError as e:
            recordId = str(uuid.uuid4()).replace("-", "")
            count += 1

    return {
        'statusCode': 500,
        'body': "Server Failed to Generate Unique ID. Please Try Again."
    }
