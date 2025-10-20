"""
Constrói o payload JSON de imóvel no formato esperado pela API da Betha,
utilizando os SQLs disponíveis e o conector de banco do projeto.

Primeiro passo: gerar JSONs em disco para conferência,
sem efetivar POST.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from assets.sql import (
    sql_qt_edificacoes,
    sql_areaunid_edificacao,
    sql_tipo_imovel,
)
from utils.database.conn import exec_select


def _map_tipo_imovel(db_value: str | None) -> str:
    """Mapeia o tipo do imóvel para o domínio da Betha.

    Observação: Sem uma regra clara entre 'PREDIAL/TERRITORIAL' e
    'URBANO/RURAL', adotamos 'URBANO' como padrão. Ajuste quando
    a regra de negócio estiver definida.
    """
    if not db_value:
        return "URBANO"
    db_value = db_value.strip().upper()
    # Heurística básica: tratar qualquer retorno como URBANO inicialmente
    return "URBANO"


def _coalesce_first_row_value(rows: List[tuple], idx: int = 0) -> Any:
    if rows and len(rows[0]) > idx:
        return rows[0][idx]
    return None


def build_imovel_payload(cadastro: int | str) -> Dict[str, Any]:
    """
    Monta um dicionário com o payload do imóvel compatível com
    POST /geoprocessamento/v1/imovel.

    Campos populados nesta primeira iteração (dados confiáveis do
    nosso banco):
    - idImovel, codigo, codigoField
    - tipoImovel (mapeado de forma conservadora)
    - situacao (ATIVADO default)
    - unidade (0 default)
    - camposAdicionais: inclui áreas por unidade (sequência) quando
      disponíveis
    """

    cadastro = int(cadastro)

    # Tipo do imóvel
    tipo_rows = exec_select(sql_tipo_imovel.format(cadastro=cadastro))
    tipo_descr = _coalesce_first_row_value(tipo_rows, 0)
    tipo_imovel = _map_tipo_imovel(tipo_descr)

    # Áreas por edificação (sequências)
    campos_adicionais: List[Dict[str, Any]] = []
    seq_rows = exec_select(sql_qt_edificacoes.format(cadastro=cadastro)) or []
    seqs = [r[0] for r in seq_rows if r and len(r) > 0]

    for sequencia in seqs:
        area_rows = exec_select(
            sql_areaunid_edificacao.format(
                cadastro=cadastro, sequencia=sequencia
            )
        )
        area_val = _coalesce_first_row_value(area_rows, 0)
        if area_val is None:
            continue
        try:
            area_num = float(area_val)
        except (TypeError, ValueError):
            continue

        campos_adicionais.append(
            {
                "campoAdicional": {
                    "titulo": f"Área edificação seq {sequencia}",
                    "tipo": "NUMERICO",
                },
                "vlCampo": round(area_num, 2),
            }
        )

    payload: Dict[str, Any] = {
        # Identificação principal
        "idImovel": cadastro,
        "codigo": cadastro,
        "codigoField": "idImovel",
        # Defaults seguros até termos mapeamento completo
        "unidade": 0,
        "situacao": "ATIVADO",
        "tipoImovel": tipo_imovel,
        # Campos opcionais deixados de fora por enquanto;
        # adicionaremos conforme mapeamento
    }

    if campos_adicionais:
        payload["camposAdicionais"] = campos_adicionais

    return payload


def write_imovel_payload(cadastro: int | str, payload: Dict[str, Any]) -> Path:
    """
    Escreve o payload em data/json/post_imoveis/{cadastro}.json
    e retorna o caminho.
    """
    import json

    file_path = Path(__file__).resolve()
    project_root = file_path.parents[4]
    out_dir = project_root / "data" / "json" / "post_imoveis"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{cadastro}.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out_file
