import boto3
from botocore.exceptions import ClientError

# Classe para configuração e manipulação do AWS Polly no projeto
# Para sintetizar uma fala em audio MP3 com a voz da AWS Polly e salvar no S3 bucket

# Função para sintetizar a fala em audio MP3 com a voz da AWS Polly
def synthesize_speech(phrase):
    polly = boto3.client('polly')
    # Tenta sintetizar a fala em audio MP3 com a voz da AWS Polly e retorna o stream de audio
    try:
        response = polly.synthesize_speech(
            Text=phrase,
            OutputFormat='mp3', # Formato de saída do áudio
            VoiceId='Joanna' # Seleciona a voz feminina Joanna
        )
        return response.get('AudioStream', None) # Retorna o stream de audio
    # Caso ocorra um erro, imprime a mensagem de erro e retorna None
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
