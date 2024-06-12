import os
from dotenv import load_dotenv
from services.logsDynamoDBService import DynamoDBClass
from services.s3BucketService import S3BucketClass
from services.textToSpeechService import TTSClass

# Carrega os serviços do DynamoDB, S3 e Polly para serem utilizados
def load_services():
    load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE') # Obtém o nome da tabela do DynamoDB
    S3_BUCKET_NAME = os.getenv('BUCKET_NAME') # Obtém o nome do bucket do S3
 
    logDynamo = DynamoDBClass(DYNAMODB_TABLE_NAME) # Instancia a classe do DynamoDB
    logDynamo.create_table_dynamodb() # Cria a tabela no DynamoDB

    s3Bucket = S3BucketClass(S3_BUCKET_NAME) # Instancia a classe do S3
    s3Bucket.create_s3_bucket() # Cria o bucket no S3

    tts = TTSClass() # Instancia a classe do Polly

    return logDynamo, s3Bucket, tts # Retorna as instâncias dos serviços

# Função para executar o Polly e salvar o arquivo de áudio
def run_tts(tts, phrase):
    tts.textToSpeech(phrase)
    tts.saveMP3File()
