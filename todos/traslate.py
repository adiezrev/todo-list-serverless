import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Obtenemos la tarea de la base de datos
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    # Obtenemos el lenguage al cual queremos traducir
    target = event['pathParameters']['lang']

    # texto a traducir e idioma en que esta el texto
    task = result['Item']['text']
    source_result = comprehend.detect_dominant_language(task)
    source = source_result['Languages'][0]['LanguageCode']

    # se traduce el texto de la tarea
    task_translated = translate.translate_text(task,source,target)        
    result['Item']['text'] = task_translated['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response