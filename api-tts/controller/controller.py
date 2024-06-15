import os
from dotenv import load_dotenv
from services.logsDynamoDBService import DynamoDBClass
from services.s3BucketService import S3BucketClass
from services.textToSpeechService import TTSClass

# Carrega os serviços do DynamoDB, S3 e Polly para serem utilizados
def load_services():
    load_dotenv()  # Carrega as variáveis de ambiente

    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE') # Nome da tabela no DynamoDB
    S3_BUCKET_NAME = os.getenv('BUCKET_NAME') # Nome do bucket no S3
    
    try:
        logDynamo = DynamoDBClass(DYNAMODB_TABLE_NAME) # Instancia a classe do DynamoDB
        logDynamo.create_table_dynamodb() # Cria a tabela no DynamoDB

        s3Bucket = S3BucketClass(S3_BUCKET_NAME) # Instancia a classe do S3
        s3Bucket.create_s3_bucket() # Cria o bucket no S3

        tts = TTSClass() # Instancia a classe do Polly
    except Exception as e:
        logging.error(f"Erro ao carregar os serviços: {e}") # Caso ocorra um erro, imprime a mensagem de erro e retorna None para os serviços
        return None, None, None

    return logDynamo, s3Bucket, tts

# Função para executar o Polly e salvar o arquivo de áudio
def run_tts(tts, phrase):
    tts.textToSpeech(phrase) # Converte o texto em áudio
    if not tts.saveMP3File(): # Salva o arquivo de áudio gerado caso não ocorra erro
        logging.error("Erro ao salvar o arquivo MP3.")
