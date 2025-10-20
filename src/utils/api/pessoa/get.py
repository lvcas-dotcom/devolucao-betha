from colorama import Style
import requests
import json
from pathlib import Path


def get_pessoa(cadastro):
    "Obtem cadastro completo da base BETHA."

    url = (
        'https://tributos.suite.betha.cloud/dados/v1/contribuintes?filter='
        'codigo=' + '"' + cadastro + '"'
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

        # Verificando se a solicitação foi bem-sucedida
        if response.status_code == 200:
            json_data = response.json()

            # Salvando os dados em um arquivo JSON com configurações p/ utf8
            out_dir = project_root / 'data' / 'json' / 'get_pessoa'
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{cadastro}.json"
            with out_file.open("w", encoding="utf-8") as arquivo:
                json.dump(json_data, arquivo, indent=2, ensure_ascii=False)

            # retorna os dados recebidos
            return json_data

    except (requests.RequestException, OSError, ValueError) as e:
        print(f"Erro ao baixar o cadastro {cadastro}. Detalhes: {e}")


def get_all_pessoa():
    "Obtem todos os cadastros de pessoas da base BETHA."

    offset = 0
    limit = 1000
    all_data = []  # Lista para armazenar todos os dados

    url_base = 'https://tributos.suite.betha.cloud/dados/v1/contribuintes?'

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
        hasNext = True
        while hasNext:
            url = f"{url_base}offset={offset}&limit={limit}"
            response = requests.get(url, headers=headers, timeout=60)

            # Verificando se a solicitação foi bem-sucedida
            if response.status_code == 200:
                json_data = response.json()

                # Adiciona os dados ao acumulador
                content = json_data.get('content', [])
                all_data.extend(content)

                # Verifica hasNext para determinar se deve continuar
                hasNext = json_data.get('hasNext', False)
                offset += limit
            else:
                # Em caso de erro na resposta, interrompe o loop e reporta
                print(
                    "Falha ao obter pessoas: status "
                    f"{response.status_code} - {response.text}"
                )
                break

            # Feedback visual durante a execução (sem importar CLI)
            print(f"{Style.RESET_ALL}|" + "=" * 73 + "|")
            print(
                "\nGERANDO ARQUIVO get_all_pessoas.json...  "
                "CADASTROS BAIXADOS: "
                f"{len(all_data)}\n\n"
            )

        # Salvando todos os dados em um único arquivo JSON
        out_dir = project_root / 'data' / 'json' / 'get_pessoa'
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / 'get_all_pessoas.json'
        with out_file.open("w", encoding="utf-8") as arquivo:
            json.dump(all_data, arquivo, indent=2, ensure_ascii=False)

        return all_data

    except (requests.RequestException, OSError, ValueError) as e:
        print(f"Erro ao baixar os cadastros de pessoas. Detalhes: {e}")
