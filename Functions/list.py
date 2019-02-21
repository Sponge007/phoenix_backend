import json
import os

from Functions.utils import DecimalEncoder
import boto3
from lambda_decorators import cors_headers
import datetime

dynamodb = boto3.resource('dynamodb')


@cors_headers
def list(event, context):
    table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }

    return response



@cors_headers
def connector(event,context):
	table = dynamodb.Table(os.environ['PHOENIX_TABLE'])

    # fetch all todos from the database
	result = table.scan()
	data = []

	for i in result["Items"]:
		real_create_date = str(i["createdAt"])[:10]
		real_update_date = str(i["updatedAt"])[:10]
		# print(real_date)
		updated_time = str(datetime.datetime.fromtimestamp(int(real_update_date)).date())
		created_time = str(datetime.datetime.fromtimestamp(int(real_create_date)).date())
		amount = i.get("amount")
		name = i.get("name")
		phone = i.get("phone number")
		fromFacebook = i.get("fromFacebook")
		havePVC = i.get("havePVC")
		problemToSolve = i.get("problemToSolve")
		localGovernment = i.get("localGovernment")
		votedBefore = i.get("votedBefore")

		print(type(amount),amount)
		print(type(havePVC),havePVC)



		if amount==None:
			if i.get("subTotal")==None:
				amount="default"
			else:
				amount=str(i.get("subTotal"))
		elif amount==True:
			amount= "test_amount"
		else:
			amount = str(float(amount)/100)

		if name == None:
			name = "default"
		if phone == None:
			phone = "default"

		if fromFacebook == None:
			fromFacebook = "default"
		elif fromFacebook == False:
			fromFacebook = "No"
		else:
			fromFacebook = "Yes"

		if havePVC == None:
			havePVC = "default"
		if problemToSolve == None:
			problemToSolve = "default"
		if votedBefore == None:
			votedBefore = "default"
		if localGovernment == None:
			localGovernment = "default"
		x = {
				"name": name,
				"phone": phone,
				"amount": amount,
				"updated_at": updated_time,
				"created_at": created_time,
				"fromFacebook": fromFacebook,
				"havePVC": havePVC,
				"problemToSolve": problemToSolve,
				"localGovernment": localGovernment,
				"votedBefore": votedBefore
			}
		data.append(x)
	print(data)

    # create a response
	response = {
		"statusCode": 200,
		"body": json.dumps(data, cls=DecimalEncoder)
	}

	return response

