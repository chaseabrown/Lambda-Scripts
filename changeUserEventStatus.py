import boto3
import uuid
import boto3.dynamodb.conditions as conditions
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # this will create dynamodb resource object and
    # here dynamodb is resource name
    client = boto3.resource('dynamodb')

    # this will search for dynamoDB table
    # your table name may be different
    eventTable = client.Table("events")
    userTable = client.Table("users")

    if event['queryStringParameters']['RSVP'] == "Attending":
        #Update User
        #   Add EventID to table=users attribute=eventsAttending
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression="SET #o = list_append(#o, :eventID)",
                ExpressionAttributeNames={
                    "#o": "eventsAttending",
                },
                ExpressionAttributeValues={
                    ":eventID": [event['queryStringParameters']['eventID']]
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Add EventID to table=users attribute=eventsAttending (Error = " + str(e) + ")"
            }

        #   Remove EventID from table=users attribute=eventsMaybe
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression="REMOVE #o[{" + event['queryStringParameters']['eventID'] + "}]",
                ExpressionAttributeNames={
                    "#o": "eventsMaybe",
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove EventID from table=users attribute=eventsMaybe (Error = " + str(e) + ")"
            }

        #Update Event
        #   Add UserID to table=events attribute=usersAttending
        try:
            eventTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression="SET #o = list_append(#o, :userID)",
                ExpressionAttributeNames={
                    "#o": "usersAttending",
                },
                ExpressionAttributeValues={
                    ":userID": event['queryStringParameters']['userID']
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Add UserID to table=events attribute=usersAttending (Error = " + str(e) + ")"
            }

        #   Remove UserID from table=events attribute=usersMaybe
        try:
            userTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['userID']}]",
                ExpressionAttributeNames={
                    "#o": "usersMaybe",
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove UserID from table=events attribute=usersMaybe (Error = " + str(e) + ")"
            }

    elif event['queryStringParameters']['RSVP'] == "Maybe":
        #Update User
        #   Add EventID to table=users attribute=eventsMaybe
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression="SET #o = list_append(#o, :eventID)",
                ExpressionAttributeNames={
                    "#o": "eventsMaybe",
                },
                ExpressionAttributeValues={
                    ":eventID": [event['queryStringParameters']['eventID']]
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Add EventID to table=users attribute=eventsMaybe (Error = " + str(e) + ")"
            }
        #   Remove EventID from table=users attribute=eventsAttending
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['eventID']}]",
                ExpressionAttributeNames={
                    "#o": "eventsAttending",
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove EventID from table=users attribute=eventsAttending (Error = " + str(e) + ")"
            }

        #Update Event
        #   Add UserID to table=events attribute=usersMaybe
        try:
            eventTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression="SET #o = list_append(#o, :userID)",
                ExpressionAttributeNames={
                    "#o": "usersMaybe",
                },
                ExpressionAttributeValues={
                    ":userID": event['queryStringParameters']['userID']
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Add UserID to table=events attribute=usersMaybe (Error = " + str(e) + ")"
            }

        #   Remove UserID from table=events attribute=usersAttending
        try:
            userTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['userID']}]",
                ExpressionAttributeNames={
                    "#o": "usersAttending",
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove UserID from table=events attribute=usersAttending (Error = " + str(e) + ")"
            }

    elif event['queryStringParameters']['RSVP'] == "None":
        #Update User
        #   Remove EventID from table=users attribute=eventsAttending
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['eventID']}]",
                ExpressionAttributeNames={
                    "#o": "eventsAttending",
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove EventID from table=users attribute=eventsAttending (Error = " + str(e) + ")"
            }
        #   Remove EventID from table=users attribute=eventsMaybe
        try:
            userTable.update_item(
                Key={
                    "userID": event['queryStringParameters']['userID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['eventID']}]",
                ExpressionAttributeNames={
                    "#o": "eventsMaybe",
                },
                ConditionExpression=conditions.Attr("userID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove EventID from table=users attribute=eventsMaybe (Error = " + str(e) + ")"
            }

        #Update Event
        #   Remove UserID from table=events attribute=usersAttending
        try:
            userTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['userID']}]",
                ExpressionAttributeNames={
                    "#o": "usersAttending",
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove UserID from table=events attribute=usersAttending (Error = " + str(e) + ")"
            }
        #   Remove UserID from table=events attribute=usersMaybe
        try:
            userTable.update_item(
                Key={
                    "eventID": event['queryStringParameters']['eventID'],
                },
                UpdateExpression=f"REMOVE #o[{event['queryStringParameters']['userID']}]",
                ExpressionAttributeNames={
                    "#o": "usersMaybe",
                },
                ConditionExpression=conditions.Attr("eventID").exists()
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': "Server Failed to Remove UserID from table=events attribute=usersMaybe (Error = " + str(e) + ")"
            }


    return {
        'statusCode': 200,
        'body': "Updated User='" + event['queryStringParameters']['userID'] + "' to Status'" + event['queryStringParameters']['RSVP'] + "' for Event='" + event['queryStringParameters']['eventID'] + "'"
    }
