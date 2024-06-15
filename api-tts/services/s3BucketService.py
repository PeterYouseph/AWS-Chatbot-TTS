import boto3
import logging
from botocore.exceptions import ClientError

# Classe para manipular o S3 e fazer o upload dos arquivos de áudio gerados
class S3BucketClass:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
    
    # Método para criar o bucket no S3 caso ele não exista
    def create_s3_bucket(self):
        try: # Verifica se o bucket já existe, caso não exista, cria o bucket
            if self._bucket_exists(self.bucket_name):
                print(f"Bucket {self.bucket_name} já existe.")
                return True
            self.s3_client.create_bucket(Bucket=self.bucket_name)
        except ClientError as e: # Caso ocorra um erro, imprime a mensagem de erro
            logging.error(f"Erro ao criar o bucket: {e}")
            return False
        return True

    # Método para verificar se o bucket já existe no S3
    def _bucket_exists(self, bucket_name):
        try: # Verifica se o bucket já existe no S3 e retorna True, caso exista
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError: # Caso não exista, retorna False 
            return False 

    # Método para fazer o upload do arquivo no S3 e retornar a URL do arquivo
    def upload_s3_bucket(self, upload_file, filename):
        try: # Faz o upload do arquivo no S3 e retorna a URL do arquivo
            self.s3_client.upload_file(upload_file, self.bucket_name, filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
            return file_url
        except ClientError as e: # Caso ocorra um erro, imprime a mensagem de erro
            logging.error(f"Erro ao fazer upload do arquivo: {e}")
            return None
