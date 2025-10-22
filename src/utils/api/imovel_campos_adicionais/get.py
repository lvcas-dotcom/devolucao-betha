import requests
import json
from pathlib import Path
from utils.files import extract_id_imovel
from utils.api import get_imovel

 
def get_imovel_campos_adicinais(cadastro):
    "Obtem informações adicionais de um cadastro da base BETHA."
    
    id_imovel = extract_id_imovel(cadastro)

    if not id_imovel:
        # Tenta baixar o imóvel e extrair novamente
        print(f"\n⚠️  Arquivo local não encontrado. Buscando cadastro {cadastro} na API Betha...")
        get_imovel(cadastro)
        id_imovel = extract_id_imovel(cadastro)
        if not id_imovel:
            print(
                f"\n❌ Cadastro {cadastro} NÃO existe na base Betha."
                f"\n   O imóvel precisa ser enviado primeiro usando a opção 4 (Gerar JSON)."
            )
            return None

    # api para receber dados
    url = (
        'https://tributos.suite.betha.cloud/geoprocessamento/v1/imoveis/'
        + id_imovel
        + '/campos-adicionais'
    )

    file_path = Path(__file__).resolve()
    src_dir = file_path.parents[3]
    project_root = file_path.parents[4]

    token_path = src_dir / 'assets' / 'token_betha.json'
    with token_path.open() as f:
        config_data = json.load(f)

    token = config_data['token']
    user_access = config_data['user_access']

    headers = {
        "Content-Type": 'application/json',
        "Authorization": "Bearer " + token,
        "User-Access": user_access
    }

    try:
        # requisição GET
        response = requests.get(url, headers=headers, timeout=30)
        
        # Verificando se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            
            json_data = response.json()

            # Salvando os dados em um arquivo JSON com configurações p/ utf8
            out_dir = (
                project_root / 'data' / 'json' / 'get_imovelcamposadicionais'
            )
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{cadastro}.json"
            with out_file.open("w", encoding="utf-8") as arquivo:
                json.dump(json_data, arquivo, indent=2, ensure_ascii=False)
            
            # retorna os dados recebidos
            return json_data

    except (requests.RequestException, OSError) as e:
        print(f"Erro ao baixar o cadastro {cadastro}. Detalhes: {e}")
            