import json

# Função para verificar a saúde da API TTS ( Se está funcionando corretamente )
def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!", # Mensagem de sucesso da requisição teste
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)} # Resposta da requisição

    return response