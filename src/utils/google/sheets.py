import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# ID da planilha.
SHEET_ID = "1Ecf04wmBdmXKWBfzqU7YmcxjMAD_rd-HUTKn5w13pCg"


def find_last_row(sheet_id, range_name):
    """Encontra a última linha preenchida na planilha."""
    
    service = build("sheets", "v4", credentials=token_google())
    
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name).execute()
    
    values = result.get('values', [])

    if not values:
        return 0
    else:
        return len(values)


def token_google():
    """Token de autenticação do Google."""
    
    creds = None
    
    # O arquivo token_google.json armazena os tokens de acesso e atualização do usuário e é
    # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez .
    
    if os.path.exists("src/assets/token_google.json"):
        creds = Credentials.from_authorized_user_file("src/assets/token_google.json", SCOPES)

    # se não existir refresh ou não for válido cria;
    if not creds or not creds.valid:
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("src/assets/client_secret.json", SCOPES)
            
            creds = flow.run_local_server(port=0)
        
        # salva para utilizar depois
        with open("src/assets/token_google.json", "w") as token:
            token.write(creds.to_json())
            
    return creds


# DEVE SER COLOCADO COMO PARAMETRO = ROW
