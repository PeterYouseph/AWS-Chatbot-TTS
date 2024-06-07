import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os


# Classe para configuração e manipulação do AWS DynamoDB no projeto
# Para salvar referências dos áudios sintetizados no DynamoDB e evitar duplicidade de audios no S3 bucket

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

# Função para verificar se a chave existe no DynamoDB e retornar o item correspondente
def get_item(phrase_hash):
    # Tenta buscar o item no DynamoDB e retorna o item se encontrado ou None se não encontrado
    try:
        response = table.get_item(Key={'phraseHash': phrase_hash})
        return response.get('Item', None)
    # Caso ocorra um erro, imprime a mensagem de erro e retorna None
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

# Função para salvar o item no DynamoDB e retorna True se bem sucedido
def put_item(item):
    # Tenta salvar o item no DynamoDB e retorna True se bem sucedido
    try:
        table.put_item(Item=item)
        return True
    # Caso ocorra um erro, imprime a mensagem de erro e retorna False
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
