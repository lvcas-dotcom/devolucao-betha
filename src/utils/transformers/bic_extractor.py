"""
Extrator de BICs (Boletim de Informações Cadastrais) para edificações e lotes.
Utiliza as queries SQL já definidas no projeto.
"""
from typing import Any, Dict, List, Optional

# Imports não mais necessários - usando queries genéricas
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
    # Usar query genérica para buscar todas as BICs disponíveis
    query = f"""
    SELECT DISTINCT
        modelocampo.idkey AS campo_id,
        modelocampo.campo AS campo_codigo,
        modelocampo.descricao AS campo_descricao,
        modelocamporesposta.idkey AS resposta_id,
        modelocamporesposta.modeloresposta AS resposta_codigo,
        modelocamporesposta.descricao AS resposta_desc,
        CASE
            WHEN t.idkey = 1 THEN 'P'
            WHEN t.idkey = 2 THEN 'N'
            WHEN t.idkey = 3 THEN 'T'
            ELSE 'T'
        END AS campo_tipo,
        modelogrupo.descricao AS grupo_descricao
    FROM
        imobiliario.edificacao edif
    LEFT JOIN
        imobiliario.edificacaobic tpl_bic
        ON tpl_bic.idkey_edificacao = edif.idkey
    LEFT JOIN
        geral.biccamporespostas camporesposta
        ON tpl_bic.idkey_biccamporespostas = camporesposta.idkey
    JOIN
        geral.bicrespostaperiodos periodo
        ON camporesposta.idkey_bicrespostaperiodo = periodo.idkey
        AND periodo.fim_periodo IS NULL
    LEFT JOIN
        geral.tpl_biccamporespostas_bicmodelocamporesposta tpl
        ON tpl.idkey_biccamporespostas = camporesposta.idkey
    LEFT JOIN
        geral.bicmodelocamporesposta modelocamporesposta
        ON tpl.idkey_bicmodelocamporesposta = modelocamporesposta.idkey
    LEFT JOIN
        geral.bicmodelocampo modelocampo
        ON modelocamporesposta.idkey_bicmodelocampo = modelocampo.idkey
    LEFT JOIN
        geral.tipocampo t
        ON t.idkey = modelocampo.tipocampo_idkey
    LEFT JOIN
        geral.bicmodelogrupo modelogrupo
        ON modelocampo.idkey_bicmodelogrupo = modelogrupo.idkey
    WHERE
        edif.cadastro = {cadastro}
        AND edif.sequencia = {sequencia}
        AND modelocampo.idkey IS NOT NULL
        AND modelocamporesposta.descricao IS NOT NULL
    ORDER BY
        campo_id
    """

    try:
        rows = exec_select(query)
        if not rows:
            return {}

        bics = {}

        for row in rows:
            campo_descricao = row[2] if len(row) > 2 else None
            resposta_desc = row[5] if len(row) > 5 else None

            if not campo_descricao:
                continue

            # Criar chave limpa (sem espaços e caracteres especiais)
            chave = campo_descricao.lower().replace(" ", "_").replace(".", "")
            chave = ''.join(c for c in chave if c.isalnum() or c == '_')

            bics[chave] = {
                "campo": {
                    "id": row[0] if len(row) > 0 else None,
                    "codigo": row[1] if len(row) > 1 else None,
                    "descricao": campo_descricao,
                    "tipo": row[6] if len(row) > 6 else "T",
                },
                "resposta": {
                    "id": row[3] if len(row) > 3 else None,
                    "codigo": row[4] if len(row) > 4 else None,
                    "descricao": resposta_desc,
                },
                "grupo": {
                    "descricao": row[7] if len(row) > 7 else None,
                }
            }

        return bics

    except Exception as e:
        print(f"Erro ao extrair BICs da edificação: {e}")
        return {}


def extrair_todas_bics_lote(cadastro: int) -> Dict[str, Any]:
    """
    Extrai TODAS as BICs disponíveis de um lote (query genérica).

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com todas as BICs do lote
    """
    query = f"""
    SELECT DISTINCT
        modelocampo.idkey AS campo_id,
        modelocampo.campo AS campo_codigo,
        modelocampo.descricao AS campo_descricao,
        modelocamporesposta.idkey AS resposta_id,
        modelocamporesposta.modeloresposta AS resposta_codigo,
        modelocamporesposta.descricao AS resposta_desc,
        CASE
            WHEN t.idkey = 1 THEN 'P'
            WHEN t.idkey = 2 THEN 'N'
            WHEN t.idkey = 3 THEN 'T'
            ELSE 'T'
        END AS campo_tipo,
        modelogrupo.descricao AS grupo_descricao
    FROM
        imobiliario.lote lote
    LEFT JOIN
        imobiliario.lotebic tpl_bic
        ON tpl_bic.idkey_lote = lote.idkey
    LEFT JOIN
        geral.biccamporespostas camporesposta
        ON tpl_bic.idkey_biccamporespostas = camporesposta.idkey
    JOIN
        geral.bicrespostaperiodos periodo
        ON camporesposta.idkey_bicrespostaperiodo = periodo.idkey
        AND periodo.fim_periodo IS NULL
    LEFT JOIN
        geral.tpl_biccamporespostas_bicmodelocamporesposta tpl
        ON tpl.idkey_biccamporespostas = camporesposta.idkey
    LEFT JOIN
        geral.bicmodelocamporesposta modelocamporesposta
        ON tpl.idkey_bicmodelocamporesposta = modelocamporesposta.idkey
    LEFT JOIN
        geral.bicmodelocampo modelocampo
        ON modelocamporesposta.idkey_bicmodelocampo = modelocampo.idkey
    LEFT JOIN
        geral.tipocampo t
        ON t.idkey = modelocampo.tipocampo_idkey
    LEFT JOIN
        geral.bicmodelogrupo modelogrupo
        ON modelocampo.idkey_bicmodelogrupo = modelogrupo.idkey
    WHERE
        lote.cadastro = {cadastro}
        AND modelocampo.idkey IS NOT NULL
        AND modelocamporesposta.descricao IS NOT NULL
    ORDER BY
        campo_id
    """

    try:
        rows = exec_select(query)
        if not rows:
            return {}

        bics = {}

        for row in rows:
            campo_descricao = row[2] if len(row) > 2 else None
            resposta_desc = row[5] if len(row) > 5 else None

            if not campo_descricao:
                continue

            # Criar chave limpa (sem espaços e caracteres especiais)
            chave = campo_descricao.lower().replace(" ", "_").replace(".", "")
            chave = ''.join(c for c in chave if c.isalnum() or c == '_')

            bics[chave] = {
                "campo": {
                    "id": row[0] if len(row) > 0 else None,
                    "codigo": row[1] if len(row) > 1 else None,
                    "descricao": campo_descricao,
                    "tipo": row[6] if len(row) > 6 else "T",
                },
                "resposta": {
                    "id": row[3] if len(row) > 3 else None,
                    "codigo": row[4] if len(row) > 4 else None,
                    "descricao": resposta_desc,
                },
                "grupo": {
                    "descricao": row[7] if len(row) > 7 else None,
                }
            }

        return bics

    except Exception as e:
        print(f"Erro ao extrair BICs do lote: {e}")
        return {}


def extrair_bics_lote(cadastro: int) -> Dict[str, Any]:
    """
    Extrai todas as BICs de um lote.

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com todas as BICs do lote
    """
    # Usar a query genérica que busca todas as BICs
    return extrair_todas_bics_lote(cadastro)


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
