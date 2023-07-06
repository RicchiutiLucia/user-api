import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def create_user(event, context):
    data = json.loads(event['body'])
    user_id = str(uuid.uuid4())
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Name and email are required fields"})
        }
        return response

    table.put_item(Item={
        'id': user_id,
        'name': name,
        'email': email
    })

    response = {
        "statusCode": 201,
        "body": json.dumps({"id": user_id, "name": name, "email": email})
    }
    return response

def get_user_by_id(event, context):
    user_id = event['pathParameters']['id']
    response = table.get_item(Key={'id': user_id})

    if 'Item' not in response:
        response = {
            "statusCode": 404,
            "body": json.dumps({"message": "User not found"})
        }
    else:
        user = response['Item']
        response = {
            "statusCode": 200,
            "body": json.dumps({"id": user['id'], "name": user['name'], "email": user['email']})
        }
    
    return response
