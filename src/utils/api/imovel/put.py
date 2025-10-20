import requests
import json 
from utils.processamento import *


def put_imovel(dados_atualizados, cadastro):
    """Atualiza o cadastro em BETHA"""
    
    # api para receber dados (incompleta)
    url = '' + cadastro

    with open('src/assets/token_betha.json') as f:
        config_data = json.load(f)

    # Acessar os valores do JSON como você faria com qualquer dicionário Python
    token = config_data['token']
    user_access = config_data['user_access']

    headers = {
        "Content-Type" : 'application/json',
        "Authorization": "Bearer " + token,
        "User-Access": user_access
    }
    
    try: 
        # requisição PUT
        response = requests.put(url, headers=headers, json=dados_atualizados)

        # Verificando se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            
            print("Ok.")
            
        print(response.text)
    
    except Exception as e:
    
        print(f"Erro ao atualizar o cadastro {cadastro}. Detalhes: {e}")
        
