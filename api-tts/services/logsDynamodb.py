import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import BotoCoreError, ClientError
from services.importAWSCredentials import aws_credentials
from uuid import uuid4

# Classe para manipular o DynamoDB e salvar os logs
class DynamoDBClass: 
    # Construtor da classe que recebe o nome da tabela do DynamoDB
    def __init__(self, dynamodb_table_name):
        self.dynamodb_table_name = dynamodb_table_name
        self.session = self.create_session()
        print(f"AWS Session: {self.session}")
        self.dynamodb = self.session.resource('dynamodb', region_name='us-east-1')
        self.dynamodb_client = self.session.client('dynamodb', region_name='us-east-1')
    # Método para criar a sessão do DynamoDB
    def create_session(self):
        ACCESS_KEY, SECRET_KEY = aws_credentials()
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY, 
            aws_secret_access_key=SECRET_KEY,
            # aws_session_token=SESSION_TOKEN
        )
        return session
    # Método para criar a tabela no DynamoDB
    def create_table_dynamodb(self):
        try:
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
        except (BotoCoreError, ClientError) as e:
            print(f'Error: {e}')
    # Método para salvar o log no DynamoDB com o id, a frase e a url do audio
    def log_register_dynamodb(self, unique_id, phrase, s3_url):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        log_item = {
            'id': unique_id,
            'timestamp': datetime.utcnow().isoformat(),
            'phrase': phrase,
            'url_to_audio': s3_url
        }
        try:
            table.put_item(Item=log_item)
        except ClientError as e:
            print(f"Erro ao inserir os dados do log no DynamoDB: {e}")
    # Método para verificar se a frase já foi salva no DynamoDB
    def repeated_value_dynamodb(self, unique_id):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        try:
            response = table.get_item(Key={'id': unique_id})
            return 'Item' in response
        except ClientError as e:
            print(f"Erro ao buscar a frase no DynamoDB: {e}")
            return None
    # Método para buscar o item no DynamoDB
    def get_item(self, unique_id):
        table = self.dynamodb.Table(self.dynamodb_table_name)
        try:
            response = table.get_item(Key={'id': unique_id})
            return response.get('Item', {})
        except ClientError as e:
            print(f"Erro ao buscar o item no DynamoDB: {e}")
            return None