import json
import os
from pathlib import Path

def read_json(cadastro, path):
    """Funcao responsavel por ler cadastro obtido da OXY"""
    
    path = path + cadastro + ".json"

    try:
        # Abrir o arquivo JSON existente
        with open(path, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados
    
    except FileNotFoundError:
        print(f"Arquivo {path} não encontrado.")
        return None
        
    except json.JSONDecodeError as json_error:
        print(
            f"Erro ao decodificar o JSON no arquivo {path}. Detalhes: {json_error}"
        )
        return None
        
    except Exception as e:
        print(f"Erro ao ler o arquivo {path}. Detalhes: {e}")
        return None


def write_json(json, cadastro, path):
    """Funcao responsavel apenas por salvar o json modificado em disco"""
    
    path = path + cadastro + ".json"
    
    try:
        # salva arquivo .tokenalterado
        with open(path, "w", encoding="utf-8") as arquivo:
            json.dump(json, arquivo, indent=2, ensure_ascii=False)
    
    except Exception as e:
        
        print(f"Erro ao salvar o arquivo {path}. Detalhes: {e}")
        return None


def extract_id_imovel(cadastro):
    """Função responsavel em extrair o Id do imovel"""

    file_path = Path(__file__).resolve()
    project_root = file_path.parents[2]  # .../cornelio
    json_path = (
        project_root / 'data' / 'json' / 'get_imovel' / f"{cadastro}.json"
    )

    try:
        with json_path.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        # Verificar se 'content' é uma lista não vazia
        if (
            'content' in dados
            and isinstance(dados['content'], list)
            and dados['content']
        ):
            # Acessar o primeiro elemento da lista 'content' e então o ID
            id_imovel = dados['content'][0]['id']
            return str(id_imovel)
        else:
            # Content vazio significa que o imóvel não existe na Betha
            return None

    except FileNotFoundError:
        print(f"Arquivo {json_path} não encontrado.")
        return None
    except json.JSONDecodeError as json_error:
        print(
            f"Erro ao decodificar o JSON no arquivo {json_path}. Detalhes: {json_error}"
        )
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo {json_path}. Detalhes: {e}")
        return None
    
    
def check_file_exists(identificacao, path):
    
    caminho_arquivo = os.path.join(path, identificacao)
    
    # Verificando se o arquivo existe
    if os.path.exists(caminho_arquivo):
        return True
    else:
        return False
