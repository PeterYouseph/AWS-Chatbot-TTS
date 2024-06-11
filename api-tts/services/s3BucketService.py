import os
import boto3
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from services.importAWSCredentials import aws_credentials

class S3BucketClass: 
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.session = self.create_session()
        self.s3_client = self.session.client('s3')
         
    def create_session(self):
        ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = aws_credentials()
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY, 
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN
        )
        return session

    def create_s3_bucket(self):
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_s3_bucket(self, upload_file, filename):
        try:
            self.s3_client.upload_file(upload_file, self.bucket_name, filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
            return file_url
        except ClientError as e:
            logging.error(e)
            return None