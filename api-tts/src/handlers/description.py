import json

# Função para retornar uma breve descrição da API TTS
def v1_description(event, context): 
    body = {
        "message": "TTS api version 1." # Descrição da API TTS
    }

    response = {"statusCode": 200, "body": json.dumps(body)} # Resposta da requisição
 
    return response 