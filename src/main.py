from utils.api import *
from utils.api.pessoa import *
from utils.processamento import *
from cli.console import * 
from utils.transformers.imovel_builder import (
    build_imovel_payload,
    write_imovel_payload,
)
import os
import sys
from colorama import Fore, Style

# Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


def main():
    while True:
        exibir_menu()
        
        opcao = input(f"|{Fore.LIGHTCYAN_EX} Escolha uma opção: {Fore.GREEN}")
        print(f"{Style.RESET_ALL}|=========================================================================|")

        # Opções de menu
        
        if opcao == "1":    
            
            imovel_cadastro = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))

            get_imovel(imovel_cadastro)
            
            input("\nVerifique a pasta de downloads (data/get_imovel)\n\n Pressione Enter para continuar...")
            
        elif opcao == "2":
            
            imovel_cadastro = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))
            
            get_imovel_campos_adicinais(imovel_cadastro)
            
            input("\nVerifique a pasta de downloads (data/get_imovelcamposadicionais)\n\n Pressione Enter para continuar...")
            
        elif opcao == "3":
            
            cadastro_atualizar = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))
        
            processamento(cadastro_atualizar)
            
            input("\nPressione Enter para continuar...")
            
        elif opcao == "4":
            cadastro = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))
            print(f"{Style.RESET_ALL}|=========================================================================|")
            
            try:
                # Gerar payload
                payload = build_imovel_payload(cadastro)
                
                # Salvar JSON
                out_file = write_imovel_payload(cadastro, payload)
                
                # Estatísticas do JSON gerado
                total_campos = len(payload.get('camposAdicionais', []))
                
                # Contar áreas
                areas = [c for c in payload.get('camposAdicionais', []) 
                         if 'área' in c['campoAdicional']['titulo'].lower()]
                
                # BICs de lote
                bics_lote_esperadas = ['Meio Fio', 'Pavimentacao', 'Ocupacao', 
                                       'Utilizacao', 'Situacao', 'Cerca/Muro']
                bics_lote = [c for c in payload.get('camposAdicionais', []) 
                             if c['campoAdicional']['titulo'] in bics_lote_esperadas]
                
                # BICs de edificação
                bics_edif_esperadas = ['Tipo', 'Alinhamento', 'Localizacao', 'Posicao', 
                                       'Estrutura', 'Cobertura', 'Vedacao', 'Forro',
                                       'Revest Externo', 'Sanitarios', 'Acabam. Interno',
                                       'Piso', 'Conservacao']
                bics_edif = [c for c in payload.get('camposAdicionais', []) 
                             if c['campoAdicional']['titulo'] in bics_edif_esperadas]
                
                # Exibir resultado
                print(f"\n{Fore.GREEN}✅ JSON gerado com sucesso!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}📁 Arquivo:{Style.RESET_ALL} {out_file}")
                print(f"\n{Fore.YELLOW}📊 Estatísticas:{Style.RESET_ALL}")
                print(f"   • Cadastro: {payload.get('idImovel', cadastro)}")
                print(f"   • Inscrição: {payload.get('inscricaoImobiliaria', 'N/A')}")
                print(f"   • Tipo: {payload.get('tipoImovel', 'N/A')}")
                print(f"   • Total de campos adicionais: {total_campos}")
                print(f"   • Áreas: {len(areas)}")
                print(f"   • BICs do Lote: {len(bics_lote)}")
                print(f"   • BICs da Edificação: {len(bics_edif)}")
                
            except Exception as e:
                print(f"\n{Fore.RED}❌ Erro ao gerar JSON do cadastro {cadastro}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Detalhes: {e}{Style.RESET_ALL}")

            input(f"\n{Style.RESET_ALL}Pressione Enter para continuar...") 
        
        elif opcao == "5":

            pessoa = "true"

            while pessoa != "false":

                exibir_menu_pessoa()

                opcao_pessoa = input(f"|{Fore.LIGHTCYAN_EX} Escolha uma opção: {Fore.GREEN}")
                print(f"{Style.RESET_ALL}|=========================================================================|")

                if opcao_pessoa == "1":

                    pessoa_cadastro = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))

                    get_pessoa(pessoa_cadastro)
            
                    input("\nVerifique a pasta de downloads (data/get_pessoa)\n\n Pressione Enter para continuar...")

                elif opcao_pessoa == "2":

                    get_all_pessoa()
                    
                    input("\nVerifique a pasta de downloads (data/get_pessoa)\n\n Pressione Enter para continuar...")

                elif opcao_pessoa == "0":

                    pessoa = "false"    
    
    
        elif opcao == "9":
            
            limpar_console()
            creditos()
            input(f"{Fore.GREEN}\n\n Pressione Enter para VOLTAR...")

        
        elif opcao == "0":
            sys.exit()
            
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    
    main()
