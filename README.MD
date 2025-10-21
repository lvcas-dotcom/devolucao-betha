# 🏢 API Devolução Betha - Cornelio Procópio

Sistema modular para geração de JSONs de imóveis compatíveis com a API da Betha Cloud, extraindo dados do banco GEON.

## ✨ Funcionalidades

### Opção 4 - Gerar JSON de IMÓVEL para devolução (Betha)

Extrai dados completos do banco GEON e gera JSON compatível com a API Betha contendo:

#### 📊 Dados Extraídos:

**Informações Básicas:**

- ID do Imóvel
- Inscrição Imobiliária
- Tipo (URBANO/RURAL)
- Situação
- Coordenadas geográficas (latitude/longitude)
- Setor, quadra, lote, matrícula

**Áreas:**

- Área do lote
- Área de cada edificação (por sequência)
- Área total construída

**BICs do Lote (6 campos):**

- Meio Fio
- Pavimentação
- Ocupação
- Utilização
- Situação
- Cerca/Muro

**BICs da Edificação (13 campos):**

- Tipo
- Alinhamento
- Localização
- Posição
- Estrutura
- Cobertura
- Vedação
- Forro
- Revestimento Externo
- Sanitários
- Acabamento Interno
- Piso
- Conservação

#### 🎯 Exemplo de Uso:

```bash
python3 src/main.py
# Escolha opção 4
# Informe o cadastro (ex: 45)
```

**Saída:**

```
✅ JSON gerado com sucesso!
📁 Arquivo: data/json/post_imoveis/45.json

📊 Estatísticas:
   • Cadastro: 45
   • Inscrição: 0101001
   • Tipo: URBANO
   • Total de campos adicionais: 22
   • Áreas: 3
   • BICs do Lote: 6
   • BICs da Edificação: 13
```

## 📋 Estrutura do Projeto

"""

import sys```

from pathlib import Pathcornelio/

├── src/

# Adicionar src ao path│ ├── main.py # Menu principal

sys.path.insert(0, str(Path(**file**).parent / "src"))│ ├── assets/

│ │ ├── sql.py # Queries SQL originais

from utils.transformers.imovel_builder import (│ │ └── token_betha.json # Configuração da API

    build_imovel_payload,│   ├── utils/

    write_imovel_payload,│   │   ├── database/

)│ │ │ └── conn.py # Conexão com banco

from colorama import Fore, Style│ │ ├── transformers/

│ │ │ ├── imovel_builder.py # Construtor principal do JSON

│ │ │ ├── sql_queries_simple.py # Queries SQL organizadas

def gerar_jsons_em_lote(cadastros: list[int]) -> None:│ │ │ ├── data_mappers.py # Mapeadores de dados

    """│   │   │   ├── bic_extractor.py       # Extrator de BICs

    Gera JSONs para uma lista de cadastros.│   │   │   └── areas_extractor.py     # Extrator de áreas

│ │ └── api/

    Args:│   │       ├── imovel/                 # APIs de imóveis

        cadastros: Lista de números de cadastro│   │       └── pessoa/                 # APIs de pessoas

    """│   └── cli/

    total = len(cadastros)│       └── console.py                  # Interface do usuário

    sucessos = 0└── data/

    erros = 0    └── json/

        ├── get_imovel/                 # Downloads da API

    print(f"\n{Fore.CYAN}Gerando JSONs para {total} cadastros...{Style.RESET_ALL}\n")        ├── get_imovelcamposadicionais/ # Campos adicionais

    print("=" * 70)        └── post_imoveis/               # JSONs para devolução ✨



    for i, cadastro in enumerate(cadastros, 1):```

        try:

            # Gerar payload## 🎯 Funcionalidades Implementadas

            payload = build_imovel_payload(cadastro)

### ✅ Dados Extraídos do Banco GEON

            # Salvar arquivo

            arquivo = write_imovel_payload(cadastro, payload)1. **Dados Básicos**

- ID do imóvel

         # Estatísticas   - Inscrição imobiliária

         campos_adicionais = len(payload.get("camposAdicionais", []))   - Matrícula

- Tipo (Urbano/Rural)

         print(   - Situação (Ativado/Inativo)

             f"{Fore.GREEN}✓{Style.RESET_ALL} [{i}/{total}] "   - Setor, Quadra, Lote

             f"Cadastro {cadastro}: "

             f"{campos_adicionais} campos adicionais"2. **Localização**

         )   - Latitude e Longitude (coordenadas geográficas)

- Endereço completo (quando disponível)

         sucessos += 1

3.  **Áreas** 🆕

         except Exception as e:   - ✅ Área do Lote

             print(   - ✅ Área de cada Edificação (por sequência)

                 f"{Fore.RED}✗{Style.RESET_ALL} [{i}/{total}] "   - ✅ Área Total Construída

                 f"Cadastro {cadastro}: {str(e)[:50]}..."

             )4. **BICs (Boletim de Informações Cadastrais)** 🆕

             erros += 1

    **BICs do Lote:**

    print("=" \* 70) - Meio Fio

    print(f"\n{Fore.CYAN}Resumo:{Style.RESET_ALL}") - Pavimentação

    print(f" {Fore.GREEN}✓ Sucessos: {sucessos}{Style.RESET_ALL}") - Ocupação

    if erros > 0: - Utilização

         print(f"  {Fore.RED}✗ Erros: {erros}{Style.RESET_ALL}")   - Situação

    print(f"\n{Fore.YELLOW}Arquivos salvos em: data/json/post_imoveis/{Style.RESET_ALL}\n") - Cerca/Muro

    **BICs da Edificação:**

if **name** == "**main**": - Tipo

    # Lista de cadastros para processar   - Alinhamento

    # Você pode modificar esta lista conforme necessário   - Localização

    CADASTROS = [   - Posição

        1, 47, 1000, 1001, 1002,   - Estrutura

        1498, 29264   - Cobertura

    ]   - Vedação

- Forro

  # Ou ler de um arquivo: - Revestimento Externo

  # with open("cadastros.txt") as f: - Sanitários

  # CADASTROS = [int(line.strip()) for line in f if line.strip()] - Acabamento Interno

- Piso

  # Gerar JSONs - Conservação

  gerar_jsons_em_lote(CADASTROS) - Utilização

## 🚀 Como Usar

### Opção 1: Via Menu Interativo

```bash
cd "cornelio"
python3 src/main.py
```

Escolha a opção **[ 4 ] Gerar JSON de IMÓVEL para devolução**

### Opção 2: Via Código Python

```python
from src.utils.transformers.imovel_builder import build_imovel_payload, write_imovel_payload

# Gerar JSON para um cadastro específico
cadastro = 1
payload = build_imovel_payload(cadastro)

# Salvar em arquivo
arquivo = write_imovel_payload(cadastro, payload)
print(f"JSON salvo em: {arquivo}")
```

### Opção 3: Gerar Múltiplos JSONs

```python
from src.utils.transformers.imovel_builder import build_imovel_payload, write_imovel_payload

cadastros = [1, 47, 1000, 1001, 1002]

for cadastro in cadastros:
    try:
        payload = build_imovel_payload(cadastro)
        arquivo = write_imovel_payload(cadastro, payload)
        print(f"✓ Cadastro {cadastro}: {arquivo}")
    except Exception as e:
        print(f"✗ Cadastro {cadastro}: Erro - {e}")
```

## 📄 Exemplo de JSON Gerado

```json
{
  "idImovel": 1,
  "inscricaoImobiliaria": "0101001",
  "tipoImovel": "URBANO",
  "situacao": "ATIVADO",
  "unidade": 0,
  "matricula": "0231-A",
  "setor": "01",
  "quadra": "01",
  "lote": "001",
  "latitude": 7436507.451099921,
  "longitude": 535993.3114857201,
  "camposAdicionais": [
    {
      "campoAdicional": {
        "titulo": "Área do Lote",
        "tipo": "NUMERICO"
      },
      "vlCampo": 231.0
    },
    {
      "campoAdicional": {
        "titulo": "Área edificação seq 1",
        "tipo": "NUMERICO"
      },
      "vlCampo": 220.87
    },
    {
      "campoAdicional": {
        "titulo": "Área Total Construída",
        "tipo": "NUMERICO"
      },
      "vlCampo": 220.87
    }
  ],
  "enderecoCorrespondencia": "IMOVEL",
  "usarEnderecoCondominio": "NAO"
}
```

## 🔧 Arquitetura Clean Code

O projeto segue princípios de **Clean Code** e **SOLID**:

- **Modularidade**: Cada módulo tem uma responsabilidade única
- **Separação de Responsabilidades**: SQL, mapeamento e construção são módulos independentes
- **Fácil Manutenção**: Código organizado e documentado
- **Extensível**: Fácil adicionar novos campos e funcionalidades

### Módulos Principais

1. **`imovel_builder.py`**: Orquestrador principal que monta o JSON
2. **`sql_queries_simple.py`**: Todas as queries SQL organizadas
3. **`data_mappers.py`**: Conversão de dados brutos para formato API
4. **`bic_extractor.py`**: Extração de BICs do banco
5. **`areas_extractor.py`**: Extração e cálculo de áreas

## 📊 Status da Implementação

| Funcionalidade  | Status | Observações                |
| --------------- | ------ | -------------------------- |
| Dados básicos   | ✅     | Completo                   |
| Coordenadas     | ✅     | Latitude/Longitude         |
| Áreas           | ✅     | Lote e Edificações         |
| BICs Lote       | ✅     | Estrutura pronta           |
| BICs Edificação | ✅     | Estrutura pronta           |
| Proprietários   | ⚠️     | Precisa ajuste nas queries |
| Testadas        | ⚠️     | Precisa ajuste nas queries |
| Loteamento      | ⚠️     | Precisa ajuste nas queries |
| Condomínio      | ⚠️     | Precisa ajuste nas queries |

## 🔄 Próximos Passos

1. Ajustar queries de proprietários/responsáveis
2. Completar extração de testadas
3. Adicionar dados de loteamento/condomínio
4. Implementar validação dos JSONs antes do POST
5. Criar logs de processamento

## 💻 Requisitos

- Python 3.8+
- PostgreSQL com banco GEON
- Bibliotecas: `psycopg2`, `requests`, `colorama`

## 📞 Suporte

Para dúvidas ou sugestões, consulte a documentação da API Betha:

- https://arrecadacao.ajuda.betha.cloud/tributos/conteudostecnicos/migracao
- https://arrecadacao.ajuda.betha.cloud/tributos/conteudostecnicos/interacao/geoprocessamento
