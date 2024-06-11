import os
from dotenv import load_dotenv

def aws_credentials():
    # Carregar o arquivo .env
    load_dotenv()
    # Carregar as variáveis de ambiente
    ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    SESSION_TOKEN = os.getenv('AWS_SECRET_SESSION_TOKEN')

    # Certificar-se de que todas as variáveis estão sendo carregadas
    print(f"ACCESS_KEY: {ACCESS_KEY}, SECRET_KEY: {SECRET_KEY}")

    # Retornar as credenciais
    return ACCESS_KEY, SECRET_KEY, SESSION_TOKEN
