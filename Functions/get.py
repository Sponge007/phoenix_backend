import os
import json

from Functions.utils import DecimalEncoder
import boto3
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')

@cors_headers
def get(event, context):
    table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=DecimalEncoder)
    }

    return response
