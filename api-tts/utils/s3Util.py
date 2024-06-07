import boto3
from botocore.exceptions import ClientError

# Classe para configuração e manipulação do AWS S3 no projeto

# Deverá possibilitar o salvamento dos áudios sintetizados no S3 bucket da AWS.


# Função para salvar o áudio no S3 bucket a partir de um stream de áudio do AWS Polly
def save_to_s3(bucket_name, audio_filename, audio_stream):
    s3 = boto3.client('s3')
    # Tenta salvar o áudio no S3 bucket e retorna True se bem sucedido
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=audio_filename,
            Body=audio_stream.read()
        )
        return True
    # Caso ocorra um erro, imprime a mensagem de erro e retorna False
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
