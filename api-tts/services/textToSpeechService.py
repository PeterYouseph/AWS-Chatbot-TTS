import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Classe para manipular o Polly e converter o texto em áudio
class TTSClass:
    def __init__(self):
        self.polly_client = boto3.client('polly')
        self.output_file = "/tmp/output.mp3"
    
    # Método para converter o texto em áudio e salvar o arquivo
    def textToSpeech(self, text):
        try: # Converte o texto em áudio e salva o arquivo no diretório /tmp
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Joanna'
            )
            with open(self.output_file, 'wb') as file: # Salva o arquivo no diretório /tmp
                file.write(response['AudioStream'].read())
        except (BotoCoreError, ClientError) as error: # Caso ocorra um erro, imprime a mensagem de erro do Polly
            print(f"Error: {error}")
            
    # Método para retornar o arquivo de áudio gerado
    def saveMP3File(self):
        return self.output_file
