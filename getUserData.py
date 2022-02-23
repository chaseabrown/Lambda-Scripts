import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):

    table = dynamodb.Table('users')
    body = table.query(KeyConditionExpression=Key('user-ID').eq(event["queryStringParameters"]['userID']))
    items = body['Items']

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items, cls=DecimalEncoder)
    }
