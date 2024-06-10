import os
from dotenv import load_dotenv
from services.logsDynamodb import DynamoDBClass
from services.s3BucketService import S3BucketClass
from services.textToSpeech import TTSClass

def load_services():
    load_dotenv()

    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE')
    S3_BUCKET_NAME = os.getenv('BUCKET_NAME')

    logDynamo = DynamoDBClass(DYNAMODB_TABLE_NAME)
    logDynamo.create_table_dynamodb()

    s3Bucket = S3BucketClass(S3_BUCKET_NAME)
    s3Bucket.create_s3_bucket()

    tts = TTSClass()

    return logDynamo, s3Bucket, tts

def run_tts(tts, phrase):
    tts.textToSpeech(phrase)
    tts.saveMP3File()
