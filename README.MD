# 🏢 API Devolução Betha - Cornelio Procópio

Sistema modular para geração de JSONs de imóveis compatíveis com a API da Betha Cloud, extraindo dados do banco GEON.

## 📋 Estrutura do Projeto

```
cornelio/
├── src/
│   ├── main.py                          # Menu principal
│   ├── assets/
│   │   ├── sql.py                       # Queries SQL originais
│   │   └── token_betha.json            # Configuração da API
│   ├── utils/
│   │   ├── database/
│   │   │   └── conn.py                 # Conexão com banco
│   │   ├── transformers/
│   │   │   ├── imovel_builder.py      # Construtor principal do JSON
│   │   │   ├── sql_queries_simple.py  # Queries SQL organizadas
│   │   │   ├── data_mappers.py        # Mapeadores de dados
│   │   │   ├── bic_extractor.py       # Extrator de BICs
│   │   │   └── areas_extractor.py     # Extrator de áreas
│   │   └── api/
│   │       ├── imovel/                 # APIs de imóveis
│   │       └── pessoa/                 # APIs de pessoas
│   └── cli/
│       └── console.py                  # Interface do usuário
└── data/
    └── json/
        ├── get_imovel/                 # Downloads da API
        ├── get_imovelcamposadicionais/ # Campos adicionais
        └── post_imoveis/               # JSONs para devolução ✨

```

## 🎯 Funcionalidades Implementadas

### ✅ Dados Extraídos do Banco GEON

1. **Dados Básicos**
   - ID do imóvel
   - Inscrição imobiliária
   - Matrícula
   - Tipo (Urbano/Rural)
   - Situação (Ativado/Inativo)
   - Setor, Quadra, Lote

2. **Localização**
   - Latitude e Longitude (coordenadas geográficas)
   - Endereço completo (quando disponível)

3. **Áreas** 🆕
   - ✅ Área do Lote
   - ✅ Área de cada Edificação (por sequência)
   - ✅ Área Total Construída

4. **BICs (Boletim de Informações Cadastrais)** 🆕
   
   **BICs do Lote:**
   - Meio Fio
   - Pavimentação
   - Ocupação
   - Utilização
   - Situação
   - Cerca/Muro

   **BICs da Edificação:**
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
   - Utilização

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

| Funcionalidade | Status | Observações |
|---------------|--------|-------------|
| Dados básicos | ✅ | Completo |
| Coordenadas | ✅ | Latitude/Longitude |
| Áreas | ✅ | Lote e Edificações |
| BICs Lote | ✅ | Estrutura pronta |
| BICs Edificação | ✅ | Estrutura pronta |
| Proprietários | ⚠️ | Precisa ajuste nas queries |
| Testadas | ⚠️ | Precisa ajuste nas queries |
| Loteamento | ⚠️ | Precisa ajuste nas queries |
| Condomínio | ⚠️ | Precisa ajuste nas queries |

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