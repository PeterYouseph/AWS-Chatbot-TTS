import boto3
from services.importAWSCredentials import aws_credentials
from botocore.exceptions import BotoCoreError, ClientError

# Classe para manipular o Polly (Text-to-Speech) e salvar o arquivo mp3
class TTSClass:
    # Construtor da classe que recebe o nome da tabela do DynamoDB
    def __init__(self):
        self.session = self.create_session()
        self.polly_client = self.session.client('polly')
        self.output_file = "output.mp3"
    # Método para criar a sessão do Polly (Text-to-Speech)
    def create_session(self):
        ACCESS_KEY, SECRET_KEY = aws_credentials()
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY, 
            aws_secret_access_key=SECRET_KEY,
            # aws_session_token=SESSION_TOKEN
        )
        return session
    # Método para converter o texto em fala e salvar o arquivo mp3
    def textToSpeech(self, text):
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Joanna'
            )
            with open(self.output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
        except (BotoCoreError, ClientError) as error:
            print(f"Error: {error}")

    def saveMP3File(self):
        pass  # Método para salvar o arquivo mp3 no S3