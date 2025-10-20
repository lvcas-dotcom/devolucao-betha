from assets.sql import *
from utils.database.conn import *
from utils.files import read_json
from colorama import Fore, Style


# NOVAS CADASTRADAS TERA PROBLEMA NO ID POIS NAO TEMOS ACESSO AO ULTIMO VALOR,
# FICANDO ASSIM COM TESTES PARA MANDAR SEM O ID E O MESMO SER DEFINIDO PELA API (TOMARA)


def lote(json_oxy, cadastro):
    """Responsável por atualizar BIC`s do LOTE (TERRENO/IMOVEL) """

    # Moldes SQL p/ BIC
    bic_lote = [sql_bic_meiofio]
    
    print(f'{Style.RESET_ALL}\n==================== Lote Cadastro: {cadastro} ====================')
    
    for bic in bic_lote:
        
        existe = False
        
        result_select = exec_select(bic + cadastro)
        
        # percorre o array de bics (json) até encontrar o compativel com loop acima (sql)
        for item in json_oxy['imobiliario']['boletim']:
            
            # verifica se está no campo correto para substituicao
            if result_select[0][4] == item['resposta']['campo']['id'] and result_select[0][5] == item['resposta']['campo']['codigo']:
                
                existe = True
                
                print(f'{Fore.GREEN}+ {result_select[0][6]}')
                        
                # verifica o tipo de resposta de bic de acordo com o select feito
                if result_select[0][7] == 'T':  # TEXTO
                
                    item['descricao'] = result_select[0][0]

                else:
                    
                    item['descricao'] = result_select[0][0]
                    item['resposta']['id'] = int(result_select[0][1])
                    item['resposta']['codigo'] = int(result_select[0][2])
                    item['resposta']['descricao'] = result_select[0][3]
                    
            
        # se não existe, adiciona o bic ao JSON
        if existe is False:
            
            print(f'{Fore.YELLOW}+ {result_select[0][6]}')
            
            # verifica o tipo de resposta de bic de acordo com o select feito
            if result_select[0][8] == "T":    
                
                json_moldebic = {
                                    "descricao": result_select[0][0],
                                    "resposta": {
                                        "campo": {
                                            "id": result_select[0][4],
                                            "codigo": result_select[0][5],
                                            "descricao": result_select[0][6],
                                            "multiResposta": result_select[0][7],
                                            "tipo": result_select[0][8],
                                            "grupo": {
                                                "id": result_select[0][9],
                                                "grupo": result_select[0][10],
                                                "descricao": result_select[0][11],
                                                "segmento": result_select[0][12]
                                            }
                                        }
                                    }
                                }
                
            else:
                
                json_moldebic = {
                                    "descricao": result_select[0][0],
                                    "resposta": {
                                        "id": int(result_select[0][1]),
                                        "codigo": result_select[0][2],
                                        "descricao": result_select[0][3],
                                        "campo": {
                                            "id": result_select[0][4],
                                            "codigo": result_select[0][5],
                                            "descricao": result_select[0][6],
                                            "multiResposta": result_select[0][7],
                                            "tipo": result_select[0][8],
                                            "grupo": {
                                                "id": result_select[0][9],
                                                "grupo": result_select[0][10],
                                                "descricao": result_select[0][11],
                                                "segmento": result_select[0][12]
                                            }
                                        }
                                    }
                                }   
                
            # Adicionando o JSON do BIC à lista de características da Edificação
            json_oxy['imobiliario']['boletim'].append(json_moldebic)

    return json_oxy

#==========================================================================================================================

def edificacoes(json_oxy, cadastro):
    """Responsável por atualizar BIC / Area da Edificacao """
    
    ## ATUALIZAR AREAS 
    
    # 2 - Área Unid. Construída | Regular
    # 3 - Área Geometria        | Irregular
    # 4 - Área Coberta          | Nova Cadastrada
    # 6 - Área Unid. Construída | Sobrado Regular
    # 7 - Área Descoberta       | Sobrado Irregular
    #     REGULAR               # NAO ALTERAR!

    bic_edificacao = [  sql_bic_tipoimovel,
                        sql_bic_alinhamento,
                        sql_bic_localizacao,
                        sql_bic_posicao,
                        sql_bic_estrutura,
                        sql_bic_cobertura,
                        sql_bic_vedacao,
                        sql_bic_forro,
                        sql_bic_revestimentoext,
                        sql_bic_sanitarios,
                        sql_bic_insteletrica,
                        sql_bic_piso,
                        sql_bic_conservacao,
                        sql_bic_utilizacao_edif]
    
    # BIC DAS EDIFICAÇÕES (JÁ PRESENTES AISE/GEON)
    
    # Adiciona uma lista para armazenar as sequências presentes(edificacoes) no JSON OXY
    sequencias_edificacoes = []  
    
    # percorre todas edificacoes já cadastradas do lote
    for edificacao in json_oxy['imobiliario']['segmentos']:
        
        edif_demolida =  exec_select(sql_edif_demolida.format(cadastro=cadastro, sequencia=edificacao['sequencia']))
        # VERIFICA SE A EDIFICACAO ESTÁ DEMOLIDA
        if edif_demolida:
            
            # remove a edificação demolida do JSON
            json_oxy['imobiliario']['segmentos'].remove(edificacao) 
                        
            print(f'{Style.RESET_ALL}==================== {Fore.RED}Edificação Demolida Unidade:{Style.RESET_ALL} {edificacao["sequencia"]} ====================')
            break


        print(f'{Style.RESET_ALL}==================== Unidade: {edificacao["sequencia"]} ====================')        

        sequencias_edificacoes.append(edificacao['sequencia'])  # Adiciona a sequência à lista
        
        
        # ATUALIZA AREA DA EDIFICACAO
        area_numeric = exec_select(sql_areaunid_edificacao.format(cadastro=cadastro, sequencia=edificacao['sequencia']))[0][0]
        if area_numeric:        
            area_float = float(area_numeric)
            edificacao['area'] = area_float
            print(f"ÁREA alterada!")
        else: 
            print(f"ÁREA não alterada! Cadastro: {cadastro} Sequencia:{edificacao['sequencia']}")
        
        
        #$=================================================================================
        # para cada molde de bic
        for bic in bic_edificacao:
            
            existe = False
            
            result_select = exec_select(bic.format(cadastro=cadastro, sequencia=edificacao['sequencia']))
            if result_select: 
                
                #$=================================================================================
                # percorre todos os bics da edificacao a fim de substituir 
                for item in edificacao['caracteristicas']:
                    
                    # confere se o BIC do select é o mesmo que o JSON 
                    if result_select[0][4] == item['resposta']['campo']['id'] and result_select[0][5] == item['resposta']['campo']['codigo']:
                    
                        existe = True
                        
                        print(f'{Fore.GREEN}+ {result_select[0][6]}')
                        
                        if result_select[0][8] == "T":
                        
                            item['descricao'] = result_select[0][0]
                            
                        else:
                            
                            item['descricao'] = result_select[0][0]
                            item['resposta']['id'] = int(result_select[0][1])
                            item['resposta']['codigo'] = int(result_select[0][2])
                            item['resposta']['descricao'] = result_select[0][3]
                            
                # se não existe, adiciona o bic ao JSON
                if existe is False:
                    
                    print(f'{Fore.YELLOW}+ {result_select[0][6]}')
                    
                    # verifica o tipo de resposta de bic de acordo com o select feito
                    if result_select[0][8] == "T":    
                        
                        json_moldebic = {
                                            "descricao": result_select[0][0],
                                            "resposta": {
                                                "campo": {
                                                    "id": result_select[0][4],
                                                    "codigo": result_select[0][5],
                                                    "descricao": result_select[0][6],
                                                    "multiResposta": result_select[0][7],
                                                    "tipo": result_select[0][8],
                                                    "grupo": {
                                                        "id": result_select[0][9],
                                                        "grupo": result_select[0][10],
                                                        "descricao": result_select[0][11],
                                                        "segmento": result_select[0][12]
                                                    }
                                                }
                                            }
                                        }
                        
                    else:
                        
                        json_moldebic = {
                                            "descricao": result_select[0][0],
                                            "resposta": {
                                                "id": int(result_select[0][1]),
                                                "codigo": result_select[0][2],
                                                "descricao": result_select[0][3],
                                                "campo": {
                                                    "id": result_select[0][4],
                                                    "codigo": result_select[0][5],
                                                    "descricao": result_select[0][6],
                                                    "multiResposta": result_select[0][7],
                                                    "tipo": result_select[0][8],
                                                    "grupo": {
                                                        "id": result_select[0][9],
                                                        "grupo": result_select[0][10],
                                                        "descricao": result_select[0][11],
                                                        "segmento": result_select[0][12]
                                                    }
                                                }
                                            }
                                        }   
                        
                    # Adicionando o JSON do BIC à lista de características da Edificação
                    edificacao["caracteristicas"].append(json_moldebic)
                    
#===============================================================================================================
    # NOVAS CADASTRADAS
    # precisa do id do campo pra poder popular corretamente 


    # extrai todas edificacoes presente no lote á serem comparadas
    qt_edificacoes = exec_select(sql_qt_edificacoes.format(cadastro=cadastro))
    # armazena lista com edificações (cadastros ativos e novas cadastradas)
    todas_edificacoes = [item[0] for item in qt_edificacoes]


    # Identifica edificações que não está no JSON (elotech)
    sequencia_novacadastrada = set(todas_edificacoes) - set(sequencias_edificacoes) 

    #$=================================================================================
    for sequencia in sequencia_novacadastrada:
        
        # trazer dados referente a edificacao a ser inserida.
        edificacao = exec_select(sql_edificacao.format(cadastro=cadastro, sequencia=sequencia))

        if edificacao:

            # Dados da Edificação
            json_moldeedif = {"id": int(edificacao[0][0]),
                                "sequencia": edificacao[0][1],
                                "principal": edificacao[0][2],
                                "area": float(edificacao[0][3]),
                                "tipo": {
                                    "id": edificacao[0][4],
                                    "descricao": edificacao[0][5]
                                    },
                                "caracteristicas": []
                            }
            
            print(f'{Style.RESET_ALL}==================== {Fore.GREEN}Nova Cadastrada Unidade:{Style.RESET_ALL} {sequencia} ====================')


            #$=================================================================================
            # para cada select de bic
            for bic in bic_edificacao:
                
                result_select = exec_select(bic.format(cadastro=cadastro, sequencia=sequencia))
                
                if result_select:
                    
                    print(f'{Fore.GREEN}+ {result_select[0][6]}')
                    
                    # verifica o tipo de resposta de bic de acordo com o select feito
                    if  result_select[0][8] == "T":    
                        
                        json_moldebic = {
                                            "descricao": result_select[0][0],
                                            "resposta": {
                                                "campo": {
                                                    "id": result_select[0][4],
                                                    "codigo": result_select[0][5],
                                                    "descricao": result_select[0][6],
                                                    "multiResposta": result_select[0][7],
                                                    "tipo": result_select[0][8],
                                                    "grupo": {
                                                        "id": result_select[0][9],
                                                        "grupo": result_select[0][10],
                                                        "descricao": result_select[0][11],
                                                        "segmento": result_select[0][12]
                                                    }
                                                }
                                            }
                                        }
                        
                    else:
                        
                        json_moldebic = {
                                            "descricao": result_select[0][0],
                                            "resposta": {
                                                "id": int(result_select[0][1]),
                                                "codigo": result_select[0][2],
                                                "descricao": result_select[0][3],
                                                "campo": {
                                                    "id": result_select[0][4],
                                                    "codigo": result_select[0][5],
                                                    "descricao": result_select[0][6],
                                                    "multiResposta": result_select[0][7],
                                                    "tipo": result_select[0][8],
                                                    "grupo": {
                                                        "id": result_select[0][9],
                                                        "grupo": result_select[0][10],
                                                        "descricao": result_select[0][11],
                                                        "segmento": result_select[0][12]
                                                    }
                                                }
                                            }
                                        }   
                        
                    # Adicionando o JSON do BIC à lista de características da Edificação
                    json_moldeedif["caracteristicas"].append(json_moldebic)
                    
        # Adicionando o JSON da NOVA CADASTRADA ao JSON
        json_oxy['imobiliario']['segmentos'].append(json_moldeedif)

                
    return json_oxy


def json_merge(cadastro):
    """Responsável por atualizar json BETHA - Elotech com informações GEON - Tributech"""
    
    # certifica que o objeto recebido esteja no formato de string para evitar erros de concatenacao
    cadastro = str(cadastro)
    
    # abre o arquivo json
    json_oxy = read_json(cadastro)
    
    # atualiza lotes (bic e tipo imovel)
    json_oxy = lote(json_oxy, cadastro)
    
    # atualiza/adiciona edificacoes (bic e area)
    json_oxy = edificacoes(json_oxy, cadastro)
    
    return json_oxy