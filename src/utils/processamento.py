from utils.api import *
from utils.files import *
from utils.json  import *
    
def processamento(cadastro):
    """Função principal para atualizacao dos dados (responsavel por baixar, ler, alterar todo cadastro de entrada, salvar e enviar)"""
    try:
        
        # Verificar se o arquivo JSON existe
        if check_file_exists(cadastro, 'data/json/get_imovel/') is not True:
            get_imovel(cadastro)
        
        # Json GEON mesclado
        dados_alterados = json_merge(cadastro)
        # Json GEON mesclado -> salvo
        write_json(dados_alterados, cadastro)
                
        # PUT // Json GEON -> Atualizacao enviada
        # put_cadastro(dados_alterados, cadastro)
        
        print(f'CADASTRO: {cadastro} atualizado em Homologação.')
    except Exception as e:
        print(f"Erro ao atualizar o cadastro {cadastro}. Detalhes: {e}")
        
        



