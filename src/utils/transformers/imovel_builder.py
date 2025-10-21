"""
Constrói o payload JSON de imóvel no formato esperado pela API da Betha.

Este módulo é responsável por:
- Extrair dados do banco de dados GEON
- Mapear para o formato esperado pela API Betha
- Gerar JSONs completos e validados para devolução

Estrutura do JSON de saída conforme swagger da API Betha:
https://tributos.suite.betha.cloud/dados/v1/imoveis
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.database.conn import exec_select
from utils.transformers.sql_queries_simple import (
    SQL_AGRUPAMENTO,
    SQL_CONDOMINIO,
    SQL_COORDENADAS,
    SQL_CORRESPONSAVEL,
    SQL_DADOS_BASICOS_IMOVEL,
    SQL_DISTRITO,
    SQL_ENDERECO_IMOVEL,
    SQL_IMOBILIARIA,
    SQL_LOTEAMENTO,
    SQL_PROPRIETARIO,
    SQL_QT_EDIFICACOES,
    SQL_SECAO,
    SQL_SETOR,
    SQL_TESTADAS,
    SQL_TODOS_RESPONSAVEIS,
)
from utils.transformers.areas_extractor import (
    extrair_area_lote,
    formatar_areas_como_campos_adicionais,
)
from utils.transformers.bic_extractor import (
    extrair_bics_lote,
    formatar_bics_para_api,
)
from utils.transformers.data_mappers import (
    formatar_cep,
    map_agrupamento,
    map_bairro,
    map_condominio,
    map_distrito,
    map_loteamento,
    map_logradouro,
    map_pessoa,
    map_secao,
    map_testada,
)


def _get_first_row(rows: Optional[List[tuple]]) -> Optional[tuple]:
    """Retorna a primeira linha de um resultado de query."""
    if rows and len(rows) > 0:
        return rows[0]
    return None


def _get_field(row: Optional[tuple], index: int) -> Any:
    """Extrai um campo específico de uma linha."""
    if row and len(row) > index:
        return row[index]
    return None


def _build_dados_basicos(cadastro: int) -> Dict[str, Any]:
    """
    Constrói os dados básicos do imóvel (identificação, tipo, situação).

    Args:
        cadastro: Número do cadastro do imóvel

    Returns:
        Dicionário com dados básicos do imóvel
    """
    row = _get_first_row(
        exec_select(SQL_DADOS_BASICOS_IMOVEL.format(cadastro=cadastro), silent=True)
    )

    if not row:
        raise ValueError(f"Cadastro {cadastro} não encontrado no banco de dados")

    dados = {
        "idImovel": cadastro,
        "inscricaoImobiliaria": _get_field(row, 1) or str(cadastro),
        "tipoImovel": _get_field(row, 3) or "URBANO",
        "situacao": _get_field(row, 8) or "ATIVADO",
        "unidade": _get_field(row, 7) or 0,
    }

    # Campos opcionais
    if _get_field(row, 2):  # matricula
        dados["matricula"] = str(_get_field(row, 2))

    if _get_field(row, 4):  # setor
        dados["setor"] = str(_get_field(row, 4))

    if _get_field(row, 5):  # quadra
        dados["quadra"] = str(_get_field(row, 5))

    if _get_field(row, 6):  # lote
        dados["lote"] = str(_get_field(row, 6))

    return dados


def _build_coordenadas(cadastro: int) -> Dict[str, Any]:
    """
    Extrai coordenadas geográficas do imóvel.

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com latitude e longitude (se disponíveis)
    """
    row = _get_first_row(
        exec_select(SQL_COORDENADAS.format(cadastro=cadastro))
    )

    coords = {}
    if row:
        lat = _get_field(row, 0)
        lon = _get_field(row, 1)

        if lat is not None:
            try:
                coords["latitude"] = float(lat)
            except (TypeError, ValueError):
                pass

        if lon is not None:
            try:
                coords["longitude"] = float(lon)
            except (TypeError, ValueError):
                pass

    return coords


def _build_endereco(cadastro: int) -> Dict[str, Any]:
    """
    Constrói os dados de endereço do imóvel.

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com dados de endereço
    """
    row = _get_first_row(
        exec_select(SQL_ENDERECO_IMOVEL.format(cadastro=cadastro))
    )

    if not row:
        return {}

    endereco = {}

    # Campos básicos do endereço
    if _get_field(row, 0):  # numero
        endereco["numero"] = str(_get_field(row, 0))

    if _get_field(row, 1):  # complemento
        endereco["complemento"] = str(_get_field(row, 1))

    if _get_field(row, 2):  # apartamento
        endereco["apartamento"] = str(_get_field(row, 2))

    if _get_field(row, 3):  # bloco
        endereco["bloco"] = str(_get_field(row, 3))

    if _get_field(row, 4):  # cep
        cep_formatado = formatar_cep(_get_field(row, 4))
        if cep_formatado:
            endereco["cep"] = cep_formatado

    # Logradouro
    logradouro = map_logradouro(row[5:9])
    if logradouro:
        endereco["logradouro"] = logradouro

    # Bairro
    bairro = map_bairro(_get_field(row, 7))
    if bairro:
        endereco["bairro"] = bairro

    # Distrito
    distrito = map_distrito(_get_field(row, 8))
    if distrito:
        endereco["distrito"] = distrito

    return endereco


def _build_proprietarios(cadastro: int) -> Dict[str, Any]:
    """
    Constrói dados de proprietário e responsáveis.

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com proprietário e corresponsáveis
    """
    pessoas = {}

    # Proprietário principal
    try:
        prop_row = _get_first_row(
            exec_select(SQL_PROPRIETARIO.format(cadastro=cadastro), silent=True)
        )
        if prop_row:
            proprietario = map_pessoa(prop_row)
            if proprietario:
                pessoas["proprietario"] = proprietario
    except Exception:
        pass  # Campo não existe no banco

    # Corresponsável
    try:
        corresp_row = _get_first_row(
            exec_select(SQL_CORRESPONSAVEL.format(cadastro=cadastro), silent=True)
        )
        if corresp_row:
            corresponsavel = map_pessoa(corresp_row)
            if corresponsavel:
                pessoas["corresponsavel"] = corresponsavel
    except Exception:
        pass  # Campo não existe no banco

    return pessoas


def _build_testadas(cadastro: int) -> List[Dict[str, Any]]:
    """
    Constrói lista de testadas do imóvel.

    Args:
        cadastro: Número do cadastro

    Returns:
        Lista de testadas
    """
    try:
        rows = exec_select(SQL_TESTADAS.format(cadastro=cadastro), silent=True)

        if not rows:
            return []

        testadas = []
        for row in rows:
            testada = map_testada(row)
            if testada:
                testadas.append(testada)

        return testadas
    except Exception:
        return []  # Campo não existe no banco


def _build_estruturas_complementares(cadastro: int) -> Dict[str, Any]:
    """
    Constrói estruturas complementares (loteamento, condomínio, etc.).

    Args:
        cadastro: Número do cadastro

    Returns:
        Dicionário com estruturas complementares
    """
    estruturas = {}

    # Loteamento
    try:
        lote_row = _get_first_row(
            exec_select(SQL_LOTEAMENTO.format(cadastro=cadastro), silent=True)
        )
        if lote_row:
            loteamento = map_loteamento(lote_row)
            if loteamento:
                estruturas["loteamento"] = loteamento
    except Exception:
        pass  # Campo não existe no banco

    # Condomínio
    try:
        cond_row = _get_first_row(
            exec_select(SQL_CONDOMINIO.format(cadastro=cadastro), silent=True)
        )
        if cond_row:
            condominio = map_condominio(cond_row)
            if condominio:
                estruturas["condominio"] = condominio
    except Exception:
        pass  # Campo não existe no banco

    # Agrupamento
    try:
        agrup_row = _get_first_row(
            exec_select(SQL_AGRUPAMENTO.format(cadastro=cadastro), silent=True)
        )
        if agrup_row:
            agrupamento = map_agrupamento(_get_field(agrup_row, 0))
            if agrupamento:
                estruturas["agrupamento"] = agrupamento
    except Exception:
        pass  # Campo não existe no banco

    # Seção
    try:
        secao_row = _get_first_row(
            exec_select(SQL_SECAO.format(cadastro=cadastro), silent=True)
        )
        if secao_row:
            secao = map_secao(_get_field(secao_row, 0))
            if secao:
                estruturas["secao"] = secao
    except Exception:
        pass  # Campo não existe no banco

    # Imobiliária
    try:
        imob_row = _get_first_row(
            exec_select(SQL_IMOBILIARIA.format(cadastro=cadastro), silent=True)
        )
        if imob_row:
            imobiliaria = map_pessoa(imob_row)
            if imobiliaria:
                estruturas["imobiliaria"] = imobiliaria
    except Exception:
        pass  # Campo não existe no banco

    return estruturas


def _build_campos_adicionais(cadastro: int) -> List[Dict[str, Any]]:
    """
    Constrói os campos adicionais do imóvel (BICs e áreas).

    Args:
        cadastro: Número do cadastro

    Returns:
        Lista de campos adicionais
    """
    from utils.transformers.bic_extractor import extrair_bics_edificacao

    campos_adicionais = []

    # 1. Adicionar áreas (lote e edificações)
    try:
        areas_campos = formatar_areas_como_campos_adicionais(cadastro)
        campos_adicionais.extend(areas_campos)
    except Exception as e:
        print(f"Aviso: Erro ao extrair áreas do cadastro {cadastro}: {e}")

    # 2. Adicionar BICs do lote
    try:
        bics_lote = extrair_bics_lote(cadastro)
        if bics_lote:
            bics_formatadas = formatar_bics_para_api(bics_lote)
            campos_adicionais.extend(bics_formatadas)
    except Exception as e:
        print(f"Aviso: Erro ao extrair BICs do lote {cadastro}: {e}")

    # 3. Adicionar BICs das edificações
    try:
        # Buscar todas as sequências de edificações (sem filtro de conferência)
        query_edificacoes = f"""
        SELECT sequencia
        FROM imobiliario.edificacao
        WHERE cadastro = {cadastro}
          AND demolido IS NOT TRUE
        ORDER BY sequencia
        """
        seq_rows = exec_select(query_edificacoes)

        if seq_rows:
            for seq_row in seq_rows:
                if not seq_row or len(seq_row) < 1:
                    continue

                sequencia = seq_row[0]

                # Extrair BICs da edificação
                bics_edif = extrair_bics_edificacao(cadastro, sequencia)

                if bics_edif:
                    # Adicionar prefixo para identificar a edificação
                    bics_edif_com_prefixo = {}
                    for chave, valor in bics_edif.items():
                        nova_chave = f"edif_seq{sequencia}_{chave}"
                        bics_edif_com_prefixo[nova_chave] = valor

                    bics_formatadas = formatar_bics_para_api(
                        bics_edif_com_prefixo
                    )
                    campos_adicionais.extend(bics_formatadas)

    except Exception as e:
        print(f"Aviso: Erro ao extrair BICs das edificações {cadastro}: {e}")

    return campos_adicionais


def build_imovel_payload(cadastro: int | str) -> Dict[str, Any]:
    """
    Constrói o payload completo do imóvel para POST na API Betha.

    Este método extrai todos os dados disponíveis no banco GEON e
    monta um JSON compatível com o schema da API Betha.

    Inclui:
    - Dados básicos (identificação, tipo, situação)
    - Coordenadas geográficas
    - Endereço completo
    - Proprietários e responsáveis
    - Testadas
    - Estruturas complementares (loteamento, condomínio, etc.)
    - Campos adicionais (BICs e áreas)

    Args:
        cadastro: Número do cadastro do imóvel

    Returns:
        Dicionário com payload completo do imóvel

    Raises:
        ValueError: Se o cadastro não for encontrado
    """
    cadastro = int(cadastro)

    # 1. Dados básicos (obrigatórios)
    payload = _build_dados_basicos(cadastro)

    # 2. Coordenadas geográficas
    coords = _build_coordenadas(cadastro)
    payload.update(coords)

    # 3. Endereço completo
    endereco = _build_endereco(cadastro)
    payload.update(endereco)

    # 4. Proprietário e responsáveis
    proprietarios = _build_proprietarios(cadastro)
    payload.update(proprietarios)

    # 5. Testadas
    testadas = _build_testadas(cadastro)
    if testadas:
        payload["testadas"] = testadas

    # 6. Estruturas complementares
    estruturas = _build_estruturas_complementares(cadastro)
    payload.update(estruturas)

    # 7. Campos adicionais (BICs e áreas)
    campos_adicionais = _build_campos_adicionais(cadastro)
    if campos_adicionais:
        payload["camposAdicionais"] = campos_adicionais

    # 8. Configurações padrão
    payload["enderecoCorrespondencia"] = "IMOVEL"
    payload["usarEnderecoCondominio"] = "NAO"

    return payload


def write_imovel_payload(cadastro: int | str, payload: Dict[str, Any]) -> Path:
    """
    Escreve o payload do imóvel em arquivo JSON.

    Args:
        cadastro: Número do cadastro
        payload: Dicionário com dados do imóvel

    Returns:
        Path do arquivo gerado
    """
    file_path = Path(__file__).resolve()
    project_root = file_path.parents[3]
    out_dir = project_root / "data" / "json" / "post_imoveis"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{cadastro}.json"

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return out_file
