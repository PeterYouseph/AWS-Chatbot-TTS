import json
import hashlib
from datetime import datetime
from services.logsDynamodb import DynamoDBClass
from services.s3BucketService import S3BucketClass
from services.textToSpeech import TTSClass
from controller.controller import load_services, run_tts

def health(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Go Serverless v3.0! Your function executed successfully!",
            "input": event,
        }),
    }

def v1_description(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "TTS api version 1.",
        }),
    }

def tts(event, context):
    print("Event received:", event)  # Print the event to debug the structure
    try:
        body = json.loads(event['body'])
        phrase = body['phrase']
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid input, 'body' key not found in the event."
            }),
        }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid JSON format in the body."
            }),
        }

    # Generate a unique ID for the phrase using a hash
    unique_id = hashlib.md5(phrase.encode()).hexdigest()

    logDynamo, s3Bucket, tts = load_services()

    # Check if the phrase already exists in DynamoDB
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

    # Run TTS to generate the audio
    run_tts(tts, phrase)

    # Upload the audio file to S3
    audio_file = tts.output_file
    audio_filename = f"{unique_id}.mp3"
    s3_url = s3Bucket.upload_s3_bucket(audio_file, audio_filename)

    # Register the log in DynamoDB
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
