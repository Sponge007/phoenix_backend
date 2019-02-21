import json
import logging
import os
import time
import datetime
import uuid

import boto3
from lambda_decorators import cors_headers

from Functions.utils import sendSMS

dynamodb = boto3.resource('dynamodb')

@cors_headers
def create(event, context):
    data = json.loads(event['body'])
    print(data)
    # if 'name' not in data or 'phone' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't create the phoenix profile item.")
    #     return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    item = {
        'phoenix_id': str(uuid.uuid1()),
        'name': data['name'],
        'phone number': data['mobile'],
        'havePVC': data['havePVC'],
        'votedBefore': data['voteLast'],
        'localGovernment': data['localGovernment'],
        'amount': data['amount'],
        'problemToSolve': data['problem'],
        'fromFacebook': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
        'friend name': data['friend_name'],
        'friend phone': data['friend_phone'],
        'reference': data['reference']
    }
    print("saving ............")
    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    print("done saving.......")
    print("sending SMS to user.......")
    sendSMS(data['mobile'],data['name'],data['friend_phone'],data['friend_name'])
    # print("sending SMS to friend.......")
    # sendSMS(data['friend_phone'],data['name'])
    print("done sending sms.....")
    return response

@cors_headers
def create_from_facebook(event, context):
    data = json.loads(event['body'])
    print(data)
    # if 'name' not in data or 'phone' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't create the phoenix profile item.")
    #     return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    item = {
        'phoenix_id': str(uuid.uuid1()),
        'name': data['name'],
        'phone number': data['mobile'],
        'amount': data['amount'],
        "reference": data["reference"],
        "localGovernment": data['localGovernment'],
        "fromFacebook": True,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    print("saving ............")
    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    print("done saving.......")
    print("sending SMS.......")
    sendSMS(data['mobile'],data['name'],None,None)
    print("done sending sms.....")
    return response