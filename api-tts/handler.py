import json
import hashlib
from datetime import datetime
from services.logsDynamoDBService import DynamoDBClass
from services.s3BucketService import S3BucketClass
from services.textToSpeechService import TTSClass
from controller.controller import load_services, run_tts
from dotenv import load_dotenv

# Function responsável por verificar a saúde da API
def health(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Go Serverless v3.0! Your function executed successfully!",
            "input": event,
        }),
    }

# Function responsável por retornar a descrição da API na versão 1
def v1_description(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "TTS api version 1.",
        }),
    }

# Function responsável por receber a frase e retornar o áudio gerado pelo Polly e salvo no S3
def tts(event, context):
    print("Event received:", event)  # Evento recebido pelo Lambda
    try: # Tenta obter a frase do corpo do evento recebido
        body = json.loads(event['body'])
        phrase = body['phrase']
    except KeyError: # Caso a chave 'body' não seja encontrada no evento, retorna um erro
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid input, 'body' key not found in the event."
            }),
        }
    except json.JSONDecodeError: # Caso o JSON esteja em um formato inválido, retorna um erro
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid JSON format in the body."
            }),
        }

    # Gerar um ID único para a frase recebida e o arquivo de áudio gerado
    unique_id = hashlib.md5(phrase.encode()).hexdigest()

    logDynamo, s3Bucket, tts = load_services()

    # Certifica-se de que a frase não foi convertida anteriormente e retorna o áudio gerado caso já tenha sido convertida
    if logDynamo.repeated_value_dynamodb(unique_id):
        item = logDynamo.get_item(unique_id)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "received_phrase": phrase,
                "url_to_audio": item['url_to_audio'],
                "created_audio": item['created_audio'],
                "unique_id": unique_id
            }),
        }

    # Converte a frase em áudio
    run_tts(tts, phrase)

    # Realiza o upload do arquivo de áudio gerado no S3
    audio_file = tts.output_file
    audio_filename = f"{unique_id}.mp3"
    s3_url = s3Bucket.upload_s3_bucket(audio_file, audio_filename)

    # Registra a conversão da frase no DynamoDB
    logDynamo.log_register_dynamodb(unique_id, phrase, s3_url)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "received_phrase": phrase,
            "url_to_audio": s3_url,
            "created_audio": datetime.utcnow().isoformat(),
            "unique_id": unique_id
        }),
    }
