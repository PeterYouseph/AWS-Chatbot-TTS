import boto3
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError
from uuid import uuid4

# Classe para manipular o DynamoDB e inserir os logs de frases convertidas
class DynamoDBClass:
    def __init__(self, dynamodb_table_name):
        self.dynamodb_table_name = dynamodb_table_name
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
    
    # Método para criar a tabela no DynamoDB caso ela não exista
    def create_table_dynamodb(self):
        try: # Verifica se a tabela já existe, caso não exista, cria a tabela
            tables = self.dynamodb_client.list_tables()
            if self.dynamodb_table_name not in tables['TableNames']:
                table = self.dynamodb.create_table(
                    TableName=self.dynamodb_table_name,
                    KeySchema=[
                        {'AttributeName': 'id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'id', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                table.meta.client.get_waiter('table_exists').wait(TableName=self.dynamodb_table_name)
        except (BotoCoreError, ClientError) as e: # Caso ocorra um erro, imprime a mensagem de erro
            print(f'Error: {e}')

    # Método para inserir os logs no DynamoDB com os dados da frase convertida
    def log_register_dynamodb(self, unique_id, phrase, s3_url):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        log_item = {
            'id': unique_id,
            'timestamp': datetime.utcnow().isoformat(),
            'phrase': phrase,
            'url_to_audio': s3_url,
            'created_audio': datetime.utcnow().isoformat()
        }
        try:  # Insere os dados no DynamoDB
            table.put_item(Item=log_item)
        except ClientError as e:  # Caso ocorra um erro, imprime a mensagem de erro
            print(f"Erro ao inserir os dados do log no DynamoDB: {e}")


    # Método para verificar se a frase já foi convertida
    def repeated_value_dynamodb(self, unique_id):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        try:
            response = table.get_item(Key={'id': unique_id})
            return 'Item' in response
        except ClientError as e:
            print(f"Erro ao buscar a frase no DynamoDB: {e}")
            return None

    # Método para buscar o item no DynamoDB pelo ID
    def get_item(self, unique_id):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        try: # Busca o item no DynamoDB pelo ID
            response = table.get_item(Key={'id': unique_id})
            return response.get('Item', {})
        except ClientError as e: # Caso ocorra um erro, retorna None
            print(f"Erro ao buscar o item no DynamoDB: {e}")
            return None
