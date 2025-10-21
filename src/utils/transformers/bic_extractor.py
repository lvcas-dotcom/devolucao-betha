"""
Extrator de BICs (Boletim de Informações Cadastrais) para edificações e lotes.
Utiliza as queries SQL já definidas no projeto.
"""
from typing import Any, Dict, List, Optional

from assets.sql import (
    sql_bic_alinhamento,
    sql_bic_cobertura,
    sql_bic_conservacao,
    sql_bic_estrutura,
    sql_bic_forro,
    sql_bic_insteletrica,
    sql_bic_localizacao,
    sql_bic_ocupacao_lote,
    sql_bic_piso,
    sql_bic_posicao,
    sql_bic_revestimentoext,
    sql_bic_sanitarios,
    sql_bic_situacao_lote,
    sql_bic_tipoimovel,
    sql_bic_utilizacao_edif,
    sql_bic_utilizacao_lote,
    sql_bic_vedacao,
)
from utils.database.conn import exec_select


def _extrair_bic_generica(
    sql_query: str,
    cadastro: int,
    sequencia: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Extrai uma BIC genérica e retorna no formato estruturado.

    Args:
        sql_query: Query SQL para buscar a BIC
        cadastro: Número do cadastro
        sequencia: Sequência da edificação (opcional, para BICs de edificação)

    Returns:
        Dicionário com informações da BIC ou None
    """
    if sequencia is not None:
        query = sql_query.format(cadastro=cadastro, sequencia=sequencia)
    else:
        query = sql_query + str(cadastro)

    try:
        rows = exec_select(query)
        if not rows or len(rows) == 0:
            return None

        # Primeira linha com os dados
        row = rows[0]

        # Estrutura esperada conforme SQL:
        # 0: descricao
        # 1: resposta_id
        # 2: resposta_codigo
        # 3: resposta_desc
        # 4: campo_id
        # 5: campo_codigo
        # 6: campo_descricao
        # 7: campo_multiresposta
        # 8: campo_tipo
        # 9: grupo_id
        # 10: grupo_grupo
        # 11: grupo_descricao
        # 12: segmento

        return {
            "descricao": row[0] if len(row) > 0 else None,
            "resposta": {
                "id": row[1] if len(row) > 1 else None,
                "codigo": row[2] if len(row) > 2 else None,
                "descricao": row[3] if len(row) > 3 else None,
            },
            "campo": {
                "id": row[4] if len(row) > 4 else None,
                "codigo": row[5] if len(row) > 5 else None,
                "descricao": row[6] if len(row) > 6 else None,
                "multiresposta": row[7] if len(row) > 7 else None,
                "tipo": row[8] if len(row) > 8 else None,
            },
            "grupo": {
                "id": row[9] if len(row) > 9 else None,
                "grupo": row[10] if len(row) > 10 else None,
                "descricao": row[11] if len(row) > 11 else None,
            }
        }
    except Exception as e:
        print(f"Erro ao extrair BIC: {e}")
        return None


def extrair_bics_edificacao(
    cadastro: int,
    sequencia: int
) -> Dict[str, Any]:
    """
    Extrai todas as BICs de uma edificação.

    Args:
        cadastro: Número do cadastro
        sequencia: Sequência da edificação

    Returns:
        Dicionário com todas as BICs da edificação
    """
    bics = {}

    # TIPO
    bic_tipo = _extrair_bic_generica(sql_bic_tipoimovel, cadastro, sequencia)
    if bic_tipo:
        bics["tipo"] = bic_tipo

    # ALINHAMENTO
    bic_alinhamento = _extrair_bic_generica(
        sql_bic_alinhamento, cadastro, sequencia
    )
    if bic_alinhamento:
        bics["alinhamento"] = bic_alinhamento

    # LOCALIZAÇÃO
    bic_localizacao = _extrair_bic_generica(
        sql_bic_localizacao, cadastro, sequencia
    )
    if bic_localizacao:
        bics["localizacao"] = bic_localizacao

    # POSIÇÃO
    bic_posicao = _extrair_bic_generica(sql_bic_posicao, cadastro, sequencia)
    if bic_posicao:
        bics["posicao"] = bic_posicao

    # ESTRUTURA
    bic_estrutura = _extrair_bic_generica(
        sql_bic_estrutura, cadastro, sequencia
    )
    if bic_estrutura:
        bics["estrutura"] = bic_estrutura

    # COBERTURA
    bic_cobertura = _extrair_bic_generica(
        sql_bic_cobertura, cadastro, sequencia
    )
    if bic_cobertura:
        bics["cobertura"] = bic_cobertura

    # VEDAÇÃO
    bic_vedacao = _extrair_bic_generica(sql_bic_vedacao, cadastro, sequencia)
    if bic_vedacao:
        bics["vedacao"] = bic_vedacao

    # FORRO
    bic_forro = _extrair_bic_generica(sql_bic_forro, cadastro, sequencia)
    if bic_forro:
        bics["forro"] = bic_forro

    # REVESTIMENTO EXTERNO
    bic_revest = _extrair_bic_generica(
        sql_bic_revestimentoext, cadastro, sequencia
    )
    if bic_revest:
        bics["revestimentoExterno"] = bic_revest

    # SANITÁRIOS
    bic_sanitarios = _extrair_bic_generica(
        sql_bic_sanitarios, cadastro, sequencia
    )
    if bic_sanitarios:
        bics["sanitarios"] = bic_sanitarios

    # INSTALAÇÃO ELÉTRICA (ACABAMENTO INTERNO)
    bic_inst_eletrica = _extrair_bic_generica(
        sql_bic_insteletrica, cadastro, sequencia
    )
    if bic_inst_eletrica:
        bics["instalacaoEletrica"] = bic_inst_eletrica

    # PISO
    bic_piso = _extrair_bic_generica(sql_bic_piso, cadastro, sequencia)
    if bic_piso:
        bics["piso"] = bic_piso

    # CONSERVAÇÃO
    bic_conservacao = _extrair_bic_generica(
        sql_bic_conservacao, cadastro, sequencia
    )
    if bic_conservacao:
        bics["conservacao"] = bic_conservacao

    # UTILIZAÇÃO
    bic_utilizacao = _extrair_bic_generica(
        sql_bic_utilizacao_edif, cadastro, sequencia
    )
    if bic_utilizacao:
        bics["utilizacao"] = bic_utilizacao

    return bics


def extrair_bics_lote(cadastro: int) -> Dict[str, Any]:
    """
    Extrai todas as BICs de um lote.

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com todas as BICs do lote
    """
    bics = {}

    # OCUPAÇÃO
    bic_ocupacao = _extrair_bic_generica(sql_bic_ocupacao_lote, cadastro)
    if bic_ocupacao:
        bics["ocupacao"] = bic_ocupacao

    # UTILIZAÇÃO
    bic_utilizacao = _extrair_bic_generica(
        sql_bic_utilizacao_lote, cadastro
    )
    if bic_utilizacao:
        bics["utilizacao"] = bic_utilizacao

    # SITUAÇÃO
    bic_situacao = _extrair_bic_generica(sql_bic_situacao_lote, cadastro)
    if bic_situacao:
        bics["situacao"] = bic_situacao

    return bics


def formatar_bics_para_api(bics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Formata as BICs para o formato esperado pela API Betha.

    A API espera um array de campos adicionais no formato:
    {
      "campoAdicional": {
        "titulo": "string",
        "tipo": "TEXTO|NUMERICO|DATA|..."
      },
      "vlCampo": "valor"
    }

    Args:
        bics: Dicionário com as BICs extraídas

    Returns:
        Lista de campos adicionais formatados
    """
    campos_adicionais = []

    for chave, bic_data in bics.items():
        if not bic_data or not isinstance(bic_data, dict):
            continue

        # Pegar informações do campo
        campo = bic_data.get("campo", {})
        resposta = bic_data.get("resposta", {})

        if not campo or not resposta:
            continue

        titulo = campo.get("descricao") or chave
        tipo_campo = campo.get("tipo", "T")

        # Mapear tipo do campo para tipo da API
        tipo_api = "TEXTO"
        if tipo_campo == "N":
            tipo_api = "NUMERICO"
        elif tipo_campo == "D":
            tipo_api = "DATA"

        # Valor da resposta
        valor = resposta.get("descricao") or resposta.get("codigo")

        if valor:
            campos_adicionais.append({
                "campoAdicional": {
                    "titulo": titulo,
                    "tipo": tipo_api,
                },
                "vlCampo": str(valor)
            })

    return campos_adicionais
