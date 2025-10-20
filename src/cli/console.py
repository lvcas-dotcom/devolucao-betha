import os
import sys
from colorama import Fore, Style, Back
from utils.processamento import *

def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    limpar_console()    
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┏┓┏┓┳ {Fore.WHITE} ┳┓┏┓┓┏┏┓┓ ┳┳┏┓┏┓┏┓ {Fore.LIGHTCYAN_EX} ┳┓┏┓┏┳┓┓┏┏┓                    ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┣┫┃┃┃ {Fore.WHITE} ┃┃┣ ┃┃┃┃┃ ┃┃┃ ┣┫┃┃ {Fore.LIGHTCYAN_EX} ┣┫┣  ┃ ┣┫┣┫                    ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┛┗┣┛┻ {Fore.WHITE} ┻┛┗┛┗┛┗┛┗┛┗┛┗┛┛┗┗┛ {Fore.LIGHTCYAN_EX} ┻┛┗┛ ┻ ┛┗┛┗                    ")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|                                                                         |")
    print(f"|{Fore.GREEN} [ 1 ] {Fore.LIGHTCYAN_EX}DOWNLOAD {Style.RESET_ALL}/ {Fore.GREEN}GET                           {Style.RESET_ALL}                         |")
    print(f"|{Fore.GREEN} [ 2 ] {Fore.LIGHTCYAN_EX}UPDATE {Style.RESET_ALL}  / {Fore.GREEN}PUT                           {Style.RESET_ALL}                         |") 
    print(f"|                                                                         |")
    print(f"|{Fore.RED} [ 0 ] Sair{Style.RESET_ALL}                                                              |")
    print(f"|=========================================================================|")
    opcao = input(f"|{Fore.LIGHTCYAN_EX} Escolha uma opção: {Fore.GREEN}")
    print(f"{Style.RESET_ALL}|=========================================================================|")

    # Opções de menu
    
    if opcao == "1":
        menu_download()
        
    elif opcao == "2":
        menu_update()
    
    elif opcao == "0":
        sys.exit()
        
    else:
        print("Opção inválida. Tente novamente.")
        
    
    
def menu_download():
    limpar_console()    
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                            {Fore.WHITE} ┳┓┏┓┓ ┏┳┓┓ ┏┓┏┓┳┓   {Fore.LIGHTCYAN_EX}                          ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                            {Fore.WHITE} ┃┃┃┃┃┃┃┃┃┃ ┃┃┣┫┃┃   {Fore.LIGHTCYAN_EX}                          ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                            {Fore.WHITE} ┻┛┗┛┗┻┛┛┗┗┛┗┛┛┗┻┛   {Fore.LIGHTCYAN_EX}                          ")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|                                                                         |")
    print(f"|{Fore.GREEN} [ 1 ] {Style.RESET_ALL} BETHA {Fore.LIGHTMAGENTA_EX}Unico cadastro.json{Style.RESET_ALL}                                         |")
    print(f"|{Fore.GREEN} [ 2 ] {Style.RESET_ALL} GEON {Fore.LIGHTMAGENTA_EX}Unico cadastro.json{Style.RESET_ALL}                                         |")
    print(f"|{Fore.GREEN} [ 3 ] {Style.RESET_ALL} GEON {Fore.LIGHTMAGENTA_EX}Lista de cadastros {Style.RESET_ALL}                                         |")
    print(f"|                                                                         |")
    print(f"|{Fore.RED} [ 0 ] Voltar{Style.RESET_ALL}                                                            |")
    print(f"|=========================================================================|")

    opcao_download = input(f"|{Fore.LIGHTCYAN_EX} Escolha uma opção: {Fore.GREEN}")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    
    if opcao_download == "1":
        
        cadastro_baixar = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))

        get_cadastro(cadastro_baixar)
        
        input(f"\n{Style.RESET_ALL}Verifique a pasta de downloads (data/get_cadastros)\n\n Pressione Enter para continuar...")  
    
    elif opcao_download == "2":
        
        cadastro_baixar = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))
        
        # Json GEON mesclado
        dados_alterados = json_merge(cadastro_baixar)
    
        # Json GEON mesclado -> salvo
        write_json(dados_alterados, cadastro_baixar)
        
        input("\nVerifique a pasta de downloads (data/put_cadastros)\n\n Pressione Enter para continuar...")
        
    elif opcao_download == "3":
        
        input("\nVerifique a pasta de downloads (data/get_cadastros)\n\n Pressione Enter para continuar...")
    
    elif opcao_download == "0":
        return 
        
    else:
        print("Opção inválida. Tente novamente.")

    
def menu_update():
    limpar_console()    
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                          {Fore.WHITE} ┳┳┏┓┳┓┏┓┏┳┓┏┓  ┏┓┳┏┓┏┓ {Fore.LIGHTCYAN_EX}                         ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                          {Fore.WHITE} ┃┃┃┃┃┃┣┫ ┃ ┣   ┣┫┃┗┓┣  {Fore.LIGHTCYAN_EX}                         ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                          {Fore.WHITE} ┗┛┣┛┻┛┛┗ ┻ ┗┛  ┛┗┻┗┛┗┛ {Fore.LIGHTCYAN_EX}                         ")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|                                                                         |")
    print(f"|{Fore.GREEN} [ 1 ] {Fore.CYAN} UNICO {Fore.GREEN}cadastro{Style.RESET_ALL}                                                   |")
    print(f"|{Fore.GREEN} [ 2 ] {Fore.LIGHTCYAN_EX} TODOS {Fore.GREEN}cadastros{Style.RESET_ALL}                                                  |")
    print(f"|                                                                         |")
    print(f"|{Fore.RED} [ 0 ] Voltar{Style.RESET_ALL}                                                            |")
    print(f"|=========================================================================|")
    opcao_update = input(f"|{Fore.LIGHTCYAN_EX} Escolha uma opção: {Fore.GREEN}")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    
    if opcao_update == "1":
        
        cadastro_atualizar = str(input(f"|{Fore.LIGHTCYAN_EX} Informe o cadastro: {Fore.GREEN}"))
    
        processamento(cadastro_atualizar)
        
        input("\nPressione Enter para continuar...")
        
    elif opcao_update == "2":
        
        processar_todos()
        
        input("\nPressione Enter para continuar...") 
        
    elif opcao_update == "0":
        return 
        
    else:
        print("Opção inválida. Tente novamente.")
    
    
    
    
def exibir_menu():
    
    # https://patorjk.com/software/taag/#p=display&f=Calvin%20S&t=API%20devolucao%20-%20cornelio%20BETHA
    limpar_console()
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┏┓┏┓┳ {Fore.WHITE} ┳┓┏┓┓┏┏┓┓ ┳┳┏┓┏┓┏┓ {Fore.LIGHTCYAN_EX} ┳┓┏┓┏┳┓┓┏┏┓                    ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┣┫┃┃┃ {Fore.WHITE} ┃┃┣ ┃┃┃┃┃ ┃┃┃ ┣┫┃┃ {Fore.LIGHTCYAN_EX} ┣┫┣  ┃ ┣┫┣┫                    ")
    print(f"{Back.MAGENTA}{Fore.LIGHTCYAN_EX}                   ┛┗┣┛┻ {Fore.WHITE} ┻┛┗┛┗┛┗┛┗┛┗┛┗┛┛┗┗┛ {Fore.LIGHTCYAN_EX} ┻┛┗┛ ┻ ┛┗┛┗                    ")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|                                                                         |")
    print(f"|{Fore.LIGHTGREEN_EX} [ 1 ] {Style.RESET_ALL}Baixar um {Fore.GREEN}IMOVEL{Style.RESET_ALL}                                                  |")
    print(f"|{Fore.LIGHTGREEN_EX} [ 2 ] {Style.RESET_ALL}Baixar um {Fore.GREEN}IMOVEL com informações adicionais{Style.RESET_ALL}                       |")
    print(f"|{Fore.LIGHTGREEN_EX} [ 3 ] {Style.RESET_ALL}Atualizar{Fore.YELLOW} base BETHA {Style.RESET_ALL}com informações da{Fore.LIGHTBLUE_EX} base GEON{Style.RESET_ALL}                 |")
    print(f"|{Fore.LIGHTGREEN_EX} [ 4 ] {Style.RESET_ALL}Gerar {Fore.GREEN}JSON de IMÓVEL{Style.RESET_ALL} para devolução (Betha){Style.RESET_ALL}             |")
    print(f"|{Fore.LIGHTGREEN_EX} [ 5 ] {Style.RESET_ALL}Cadastro de {Fore.GREEN}PESSOAS{Style.RESET_ALL}                                               |")
    print(f"|                                                                         |")
    print(f"|{Fore.LIGHTMAGENTA_EX} [ 9 ] Créditos                                                   {Style.RESET_ALL}       |")
    print(f"|{Fore.LIGHTRED_EX} [ 0 ] Sair{Style.RESET_ALL}                                                              |")
    print(f"|=========================================================================|")
    
    
def creditos():
    

    
    print(f"{Fore.LIGHTMAGENTA_EX}╔╦╗  ╦═╗  ╦  ╔╗   ╦ ╦  ╔╦╗  ╔═╗  ╔═╗  ╦ ╦               ")
    print(f"{Fore.LIGHTMAGENTA_EX} ║   ╠╦╝  ║  ╠╩╗  ║ ║   ║   ║╣   ║    ╠═╣               ")
    print(f"{Fore.LIGHTMAGENTA_EX} ╩   ╩╚═  ╩  ╚═╝  ╚═╝   ╩   ╚═╝  ╚═╝  ╩ ╩               ")
    print(f"{Fore.MAGENTA}                                                        ")
    print(f"{Fore.MAGENTA}                                                        ")
    print(f"{Fore.MAGENTA}                                                        ")
    print(f"{Fore.LIGHTGREEN_EX}┬┌┬┐┌─┐┬  ┬┌─┐┬┌─┐  ┌┐ ┬ ┬   ╦═╗╦╔═╗╦ ╦╔═╗╦═╗╔╦╗        ")
    print(f"{Fore.LIGHTGREEN_EX}│││││ │└┐┌┘├┤ │└─┐  ├┴┐└┬┘   ╠╦╝║║  ╠═╣╠═╣╠╦╝ ║║        ")
    print(f"{Fore.LIGHTGREEN_EX}┴┴ ┴└─┘ └┘ └─┘┴└─┘  └─┘ ┴    ╩╚═╩╚═╝╩ ╩╩ ╩╩╚══╩╝        ")
    print(f"{Fore.LIGHTGREEN_EX}┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  ┌┐ ┬ ┬   ╔═╗╔═╗╔╗ ╦═╗╦╔═╗╦    ╦  ╦")
    print(f"{Fore.LIGHTGREEN_EX}├─┘├┤ └─┐└─┐│ │├─┤  ├┴┐└┬┘   ║ ╦╠═╣╠╩╗╠╦╝║║╣ ║    ╚╗╔╝")
    print(f"{Fore.LIGHTGREEN_EX}┴  └─┘└─┘└─┘└─┘┴ ┴  └─┘ ┴    ╚═╝╩ ╩╚═╝╩╚═╩╚═╝╩═╝   ╚╝o")
    
    
    
def exibir_menu_pessoa():
    limpar_console()
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|{Fore.LIGHTCYAN_EX}                     BAIXAR Cadastros de PESSOAS{Style.RESET_ALL}                         |")
    print(f"{Style.RESET_ALL}|=========================================================================|")
    print(f"|                                                                         |")
    print(f"|{Fore.GREEN} [ 1 ] {Style.RESET_ALL}Baixar uma {Fore.GREEN}pessoa{Style.RESET_ALL} (BETHA)                                         |")
    print(f"|{Fore.GREEN} [ 2 ] {Style.RESET_ALL}Baixar todas as {Fore.GREEN}pessoas{Style.RESET_ALL} (BETHA)                                   |")
    print(f"|                                                                         |")
    print(f"|{Fore.RED} [ 0 ] Voltar{Style.RESET_ALL}                                                            |")
    print(f"|=========================================================================|")