import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')
# Funzione per la Creazione di un utente con name ed email
def create_user(event, context):
    data = json.loads(event['body'])#estrae i dati dal corpo (body) di un evento in formato JSON e li converte in un oggetto Python.
    user_id = str(uuid.uuid4()) #genere un identificatore univoco e lo converte in una stringa
    name = data.get('name')
    email = data.get('email')
    #if che mostra un messaggio di errore nel caso in cui name ed email sono richiesti e non vengono assegnati
    if not name or not email:
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Name and email are required fields"})
        }
        return response
    #inserisce un nuovo elemento (item) nella tabella DynamoDB.
    table.put_item(Item={
        'id': user_id,
        'name': name,
        'email': email
    })

    response = {
        "statusCode": 201,
        "body": json.dumps({"id": user_id, "name": name, "email": email}) #json.dumps() è una funzione che converte un oggetto Python in una stringa JSON.
    }
    return response
# Funzione per ricercare un utente tramite il proprio id
def get_user_by_id(event, context):
    user_id = event['pathParameters']['id']
    response = table.get_item(Key={'id': user_id})
    #if che mostra un messaggio di errore nel caso in cui un utente non dovrebbe essere presente
    if 'Item' not in response:
        response = {
            "statusCode": 404,
            "body": json.dumps({"message": "User not found"})
        }
    else: #else che mostra l'avvenuto successo nella ricerca dell'utente con id, name ed email
        user = response['Item']
        response = {
            "statusCode": 200,
            "body": json.dumps({"id": user['id'], "name": user['name'], "email": user['email']})
        }
    
    return response
