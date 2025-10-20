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
            try:
                payload = build_imovel_payload(cadastro)
                out_file = write_imovel_payload(cadastro, payload)
                print(
                    f"\n{Fore.GREEN}JSON gerado para devolução:{Style.RESET_ALL} "
                    f"{Fore.CYAN}{out_file}{Style.RESET_ALL}"
                )
            except Exception as e:
                print(f"Erro ao gerar JSON do cadastro {cadastro}. Detalhes: {e}")

            input("\nPressione Enter para continuar...") 
        
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
