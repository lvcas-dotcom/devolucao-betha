"""
Módulo de mapeamento de dados entre o banco GEON e o formato da API Betha.
Cada função recebe dados brutos do banco e retorna objetos estruturados.
"""
from typing import Any, Dict, List, Optional


def map_logradouro(row: tuple) -> Optional[Dict[str, Any]]:
    """
    Mapeia dados do logradouro para o formato da API Betha.

    Args:
        row: tupla com (tipo_logradouro, logradouro_nome, municipio_nome, uf)

    Returns:
        Dicionário com estrutura de logradouro ou None
    """
    if not row or len(row) < 4:
        return None

    tipo_log, nome_log, municipio, uf = row[0:4]

    if not nome_log:
        return None

    result = {
        "nome": nome_log,
    }

    if tipo_log:
        result["tipoLogradouro"] = tipo_log

    if municipio and uf:
        result["municipio"] = {
            "nome": municipio,
            "uf": uf
        }

    return result


def map_bairro(nome: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Mapeia o nome do bairro para o formato da API Betha.

    Args:
        nome: Nome do bairro

    Returns:
        Dicionário com estrutura de bairro ou None
    """
    if not nome:
        return None

    return {"nome": nome}


def map_distrito(nome: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Mapeia o nome do distrito para o formato da API Betha.

    Args:
        nome: Nome do distrito

    Returns:
        Dicionário com estrutura de distrito ou None
    """
    if not nome:
        return None

    return {"nome": nome}


def map_pessoa(row: tuple) -> Optional[Dict[str, Any]]:
    """
    Mapeia dados de pessoa (proprietário/corresponsável) para o formato da API.

    Args:
        row: tupla com (codigo, nome, cpf_cnpj)

    Returns:
        Dicionário com estrutura de pessoa ou None
    """
    if not row or len(row) < 3:
        return None

    codigo, nome, cpf_cnpj = row[0:3]

    if not codigo or not nome:
        return None

    result = {
        "codigo": int(codigo),
        "nome": nome,
    }

    if cpf_cnpj:
        # Remove caracteres não numéricos
        cpf_cnpj_limpo = ''.join(filter(str.isdigit, str(cpf_cnpj)))
        if cpf_cnpj_limpo:
            result["cpfCnpj"] = cpf_cnpj_limpo

    return result


def map_testada(row: tuple) -> Optional[Dict[str, Any]]:
    """
    Mapeia dados de testada para o formato da API Betha.

    Args:
        row: tupla com (valor_testada, medida_testada, face_desc, face_abrev)

    Returns:
        Dicionário com estrutura de testada ou None
    """
    if not row or len(row) < 2:
        return None

    valor, medida, face_desc, face_abrev = (
        row[0] if len(row) > 0 else None,
        row[1] if len(row) > 1 else None,
        row[2] if len(row) > 2 else None,
        row[3] if len(row) > 3 else None,
    )

    if not valor:
        return None

    result = {}

    try:
        result["valor"] = float(valor)
    except (TypeError, ValueError):
        return None

    if medida:
        result["medida"] = str(medida)

    if face_desc or face_abrev:
        face = {}
        if face_desc:
            face["descricao"] = face_desc
        if face_abrev:
            face["abreviatura"] = face_abrev
        result["face"] = face

    return result


def map_loteamento(row: tuple) -> Optional[Dict[str, Any]]:
    """
    Mapeia dados de loteamento para o formato da API Betha.

    Args:
        row: tupla com (nome, nro_lotes, nro_caucionados)

    Returns:
        Dicionário com estrutura de loteamento ou None
    """
    if not row or len(row) < 1:
        return None

    nome, nro_lotes, nro_caucionados = (
        row[0] if len(row) > 0 else None,
        row[1] if len(row) > 1 else None,
        row[2] if len(row) > 2 else None,
    )

    if not nome:
        return None

    result = {"nome": nome}

    if nro_lotes is not None:
        try:
            result["nroLotes"] = int(nro_lotes)
        except (TypeError, ValueError):
            pass

    if nro_caucionados is not None:
        try:
            result["nroCaucionados"] = int(nro_caucionados)
        except (TypeError, ValueError):
            pass

    return result


def map_condominio(row: tuple) -> Optional[Dict[str, Any]]:
    """
    Mapeia dados de condomínio para o formato da API Betha.

    Args:
        row: tupla com (nome, tipo, tipo_log, log_nome, municipio, uf)

    Returns:
        Dicionário com estrutura de condomínio ou None
    """
    if not row or len(row) < 2:
        return None

    nome, tipo, tipo_log, log_nome, municipio, uf = (
        row[0] if len(row) > 0 else None,
        row[1] if len(row) > 1 else None,
        row[2] if len(row) > 2 else None,
        row[3] if len(row) > 3 else None,
        row[4] if len(row) > 4 else None,
        row[5] if len(row) > 5 else None,
    )

    if not nome:
        return None

    result = {"nome": nome}

    if tipo:
        result["tipoCondominio"] = tipo

    # Mapear logradouro se disponível
    if log_nome:
        logradouro = {
            "nome": log_nome,
        }
        if tipo_log:
            logradouro["tipoLogradouro"] = tipo_log
        if municipio and uf:
            logradouro["municipio"] = {
                "nome": municipio,
                "uf": uf
            }
        result["logradouro"] = logradouro

    return result


def map_agrupamento(descricao: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Mapeia dados de agrupamento para o formato da API Betha.

    Args:
        descricao: Descrição do agrupamento

    Returns:
        Dicionário com estrutura de agrupamento ou None
    """
    if not descricao:
        return None

    return {"descricao": descricao}


def map_secao(secao: Optional[int]) -> Optional[Dict[str, int]]:
    """
    Mapeia dados de seção para o formato da API Betha.

    Args:
        secao: Número da seção

    Returns:
        Dicionário com estrutura de seção ou None
    """
    if secao is None:
        return None

    try:
        return {"secao": int(secao)}
    except (TypeError, ValueError):
        return None


def map_face(descricao: Optional[str], abreviatura: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Mapeia dados de face para o formato da API Betha.

    Args:
        descricao: Descrição da face
        abreviatura: Abreviatura da face

    Returns:
        Dicionário com estrutura de face ou None
    """
    if not descricao and not abreviatura:
        return None

    result = {}
    if descricao:
        result["descricao"] = descricao
    if abreviatura:
        result["abreviatura"] = abreviatura

    return result


def limpar_cpf_cnpj(cpf_cnpj: Optional[str]) -> Optional[str]:
    """
    Remove caracteres não numéricos de CPF/CNPJ.

    Args:
        cpf_cnpj: String com CPF ou CNPJ

    Returns:
        String apenas com dígitos ou None
    """
    if not cpf_cnpj:
        return None

    limpo = ''.join(filter(str.isdigit, str(cpf_cnpj)))
    return limpo if limpo else None


def formatar_cep(cep: Optional[str]) -> Optional[str]:
    """
    Formata CEP removendo caracteres não numéricos.

    Args:
        cep: String com CEP

    Returns:
        CEP formatado ou None
    """
    if not cep:
        return None

    limpo = ''.join(filter(str.isdigit, str(cep)))
    return limpo if limpo and len(limpo) == 8 else None
