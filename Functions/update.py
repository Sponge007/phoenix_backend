import json
import time
import logging
import os

from Functions.utils import DecimalEncoder
import boto3
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')

@cors_headers
def update(event, context):
    data = json.loads(event['body'])

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    # update the todo in the database
    result = table.update_item(
        Key={
            'phoenix_id': data['id']
        },
        ExpressionAttributeNames={
          '#reference': 'reference',
        },
        ExpressionAttributeValues={
          ':reference': data['reference'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #reference = :reference, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=DecimalEncoder)
    }

    return response
