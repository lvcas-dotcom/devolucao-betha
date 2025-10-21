"""
Extrator de áreas e medidas de imóveis.
Inclui áreas de lote, edificações e testadas.
"""
from typing import Any, Dict, List, Optional

from assets.sql import (
    sql_areaunid_edificacao,
    sql_edificacao,
    sql_qt_edificacoes,
)
from utils.database.conn import exec_select


def extrair_area_lote(cadastro: int) -> Optional[float]:
    """
    Extrai a área do lote/terreno.

    Args:
        cadastro: Número do cadastro

    Returns:
        Área do lote em m² ou None
    """
    query = f"""
    SELECT
        l.lotearea AS area_lote
    FROM
        imobiliario.lote l
    WHERE
        l.cadastro = {cadastro}
    """

    try:
        rows = exec_select(query)
        if rows and len(rows) > 0 and rows[0][0] is not None:
            return float(rows[0][0])
    except (TypeError, ValueError, IndexError):
        pass

    return None


def extrair_areas_edificacoes(cadastro: int) -> List[Dict[str, Any]]:
    """
    Extrai as áreas de todas as edificações de um cadastro.

    Args:
        cadastro: Número do cadastro

    Returns:
        Lista de dicionários com informações de área por edificação
    """
    areas_edificacoes = []

    # Buscar todas as sequências de edificações
    seq_rows = exec_select(sql_qt_edificacoes.format(cadastro=cadastro))

    if not seq_rows:
        return areas_edificacoes

    for seq_row in seq_rows:
        if not seq_row or len(seq_row) < 1:
            continue

        sequencia = seq_row[0]

        # Buscar área da edificação
        area_rows = exec_select(
            sql_areaunid_edificacao.format(
                cadastro=cadastro,
                sequencia=sequencia
            )
        )

        if area_rows and len(area_rows) > 0:
            area_value = area_rows[0][0]

            if area_value is not None:
                try:
                    area_num = float(area_value)
                    areas_edificacoes.append({
                        "sequencia": sequencia,
                        "area": round(area_num, 2),
                        "descricao": f"Área edificação seq {sequencia}"
                    })
                except (TypeError, ValueError):
                    continue

    return areas_edificacoes


def extrair_detalhes_edificacao(
    cadastro: int,
    sequencia: int
) -> Optional[Dict[str, Any]]:
    """
    Extrai detalhes completos de uma edificação.

    Args:
        cadastro: Número do cadastro
        sequencia: Sequência da edificação

    Returns:
        Dicionário com detalhes da edificação ou None
    """
    rows = exec_select(
        sql_edificacao.format(cadastro=cadastro, sequencia=sequencia)
    )

    if not rows or len(rows) == 0:
        return None

    row = rows[0]

    # Estrutura do SQL:
    # 0: id
    # 1: sequencia
    # 2: principal (S/N)
    # 3: area_geo
    # 4: tipo_id
    # 5: tipo_descricao

    return {
        "id": row[0] if len(row) > 0 else None,
        "sequencia": row[1] if len(row) > 1 else None,
        "principal": row[2] if len(row) > 2 else "N",
        "area": float(row[3]) if len(row) > 3 and row[3] else None,
        "tipo": {
            "id": row[4] if len(row) > 4 else None,
            "descricao": row[5] if len(row) > 5 else None,
        }
    }


def extrair_todas_edificacoes(cadastro: int) -> List[Dict[str, Any]]:
    """
    Extrai detalhes de todas as edificações de um cadastro.

    Args:
        cadastro: Número do cadastro

    Returns:
        Lista com detalhes de todas as edificações
    """
    edificacoes = []

    # Buscar todas as sequências
    seq_rows = exec_select(sql_qt_edificacoes.format(cadastro=cadastro))

    if not seq_rows:
        return edificacoes

    for seq_row in seq_rows:
        if not seq_row or len(seq_row) < 1:
            continue

        sequencia = seq_row[0]

        # Buscar detalhes da edificação
        detalhes = extrair_detalhes_edificacao(cadastro, sequencia)

        if detalhes:
            edificacoes.append(detalhes)

    return edificacoes


def calcular_area_total_construida(cadastro: int) -> float:
    """
    Calcula a área total construída somando todas as edificações.

    Args:
        cadastro: Número do cadastro

    Returns:
        Área total construída em m²
    """
    areas = extrair_areas_edificacoes(cadastro)
    return sum(item["area"] for item in areas if item.get("area"))


def formatar_areas_como_campos_adicionais(
    cadastro: int
) -> List[Dict[str, Any]]:
    """
    Formata as áreas como campos adicionais para a API Betha.

    Args:
        cadastro: Número do cadastro

    Returns:
        Lista de campos adicionais com as áreas
    """
    campos_adicionais = []

    # Área do lote
    area_lote = extrair_area_lote(cadastro)
    if area_lote:
        campos_adicionais.append({
            "campoAdicional": {
                "titulo": "Área do Lote",
                "tipo": "NUMERICO"
            },
            "vlCampo": round(area_lote, 2)
        })

    # Áreas das edificações
    areas_edificacoes = extrair_areas_edificacoes(cadastro)
    for area_info in areas_edificacoes:
        campos_adicionais.append({
            "campoAdicional": {
                "titulo": area_info["descricao"],
                "tipo": "NUMERICO"
            },
            "vlCampo": area_info["area"]
        })

    # Área total construída
    area_total = calcular_area_total_construida(cadastro)
    if area_total > 0:
        campos_adicionais.append({
            "campoAdicional": {
                "titulo": "Área Total Construída",
                "tipo": "NUMERICO"
            },
            "vlCampo": round(area_total, 2)
        })

    return campos_adicionais
