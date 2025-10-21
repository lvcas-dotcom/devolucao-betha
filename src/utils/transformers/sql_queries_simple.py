"""
SQLs simplificadas baseadas na estrutura real do banco GEON de Cornélio Procópio.
Versão focada nos dados essenciais disponíveis no banco.
"""

# ============================================================================
# DADOS BÁSICOS DO IMÓVEL
# ============================================================================

SQL_DADOS_BASICOS_IMOVEL = """
SELECT
    l.cadastro AS codigo,
    COALESCE(
        l.codigo_inscricao,
        COALESCE(l.insc_campo01, '') ||
        COALESCE(l.insc_campo02, '') ||
        COALESCE(l.insc_campo03, '')
    ) AS inscricao_imobiliaria,
    l.lotedescricao AS matricula,
    CASE
        WHEN lt.descricao ILIKE 'PREDIAL' THEN 'URBANO'
        WHEN lt.descricao ILIKE 'TERRITORIAL' THEN 'URBANO'
        ELSE 'URBANO'
    END AS tipo_imovel,
    l.insc_campo01 AS setor,
    l.insc_campo02 AS quadra,
    l.insc_campo03 AS lote,
    0 AS unidade,
    'ATIVADO' AS situacao,
    l.lotearea AS area_terreno
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.lotetipoimovel lt
    ON lt.idkey = l.idkey_tipoimovel
WHERE
    l.cadastro = {cadastro}
"""

SQL_COORDENADAS = """
SELECT
    ST_Y(ST_Centroid(gl.geom)) AS latitude,
    ST_X(ST_Centroid(gl.geom)) AS longitude
FROM
    imobiliario.lote l
LEFT JOIN
    geo.lote gl ON gl.idkey_lote = l.idkey
WHERE
    l.cadastro = {cadastro}
"""

# ============================================================================
# PROPRIETÁRIOS E RESPONSÁVEIS
# ============================================================================

SQL_PROPRIETARIO = """
SELECT
    lr.idkey_responsavel AS codigo,
    lr.nomeresponsavel AS nome,
    lr.cpfcnpjresponsavel AS cpf_cnpj,
    lr.idkey_loteresponsaveltipo AS tipo_vinculo
FROM
    imobiliario.loteresponsavel lr
WHERE
    lr.cadastro = {cadastro}
    AND lr.idkey_loteresponsaveltipo = 1
    AND lr.ativo IS TRUE
ORDER BY
    lr.idkey
LIMIT 1
"""

SQL_CORRESPONSAVEL = """
SELECT
    lr.idkey_responsavel AS codigo,
    lr.nomeresponsavel AS nome,
    lr.cpfcnpjresponsavel AS cpf_cnpj
FROM
    imobiliario.loteresponsavel lr
WHERE
    lr.cadastro = {cadastro}
    AND lr.idkey_loteresponsaveltipo = 2
    AND lr.ativo IS TRUE
ORDER BY
    lr.idkey
LIMIT 1
"""

SQL_TODOS_RESPONSAVEIS = """
SELECT
    lr.idkey_responsavel AS codigo,
    lr.nomeresponsavel AS nome,
    lr.cpfcnpjresponsavel AS cpf_cnpj,
    lr.idkey_loteresponsaveltipo AS tipo_vinculo
FROM
    imobiliario.loteresponsavel lr
WHERE
    lr.cadastro = {cadastro}
    AND lr.ativo IS TRUE
ORDER BY
    lr.idkey_loteresponsaveltipo, lr.idkey
"""

# ============================================================================
# EDIFICAÇÕES
# ============================================================================

SQL_QT_EDIFICACOES = """
SELECT
    e.sequencia,
    e.idkey
FROM
    imobiliario.edificacao e
LEFT JOIN
    geo.edificacao ge
    ON ge.idkey_edificacao = e.idkey
WHERE
    ge.conferencia IN (2,3,4,6,7)
    AND e.demolido IS NOT TRUE
    AND e.cadastro = {cadastro}
ORDER BY
    e.sequencia
"""

SQL_EDIFICACAO_DETALHES = """
SELECT
    COALESCE(e.codigo_integracao::int8, e.idkey::int8) AS id,
    e.sequencia,
    CASE
        WHEN e.principal = TRUE THEN 'S'
        ELSE 'N'
    END AS principal,
    CAST(CASE
        WHEN ge.conferencia = ANY (ARRAY[2, 6]) THEN e.areaunidconstruida::double PRECISION
        WHEN ge.conferencia = 3 THEN st_area(ge.geom)
        WHEN ge.conferencia = 4 THEN e.areacoberta::double PRECISION
        WHEN ge.conferencia = 7 THEN e.areadescoberta::double PRECISION
        ELSE e.areaunidconstruida
    END AS NUMERIC(15,2)) AS area_construida,
    e.idkey_edificacaotipo AS tipo_id,
    et.descricao AS tipo_descricao
FROM
    imobiliario.edificacao e
LEFT JOIN
    imobiliario.edificacaotipo et
    ON et.idkey = e.idkey_edificacaotipo
LEFT JOIN
    geo.edificacao ge
    ON ge.idkey_edificacao = e.idkey
WHERE
    e.cadastro = {cadastro}
    AND e.sequencia = {sequencia}
    AND e.demolido IS NOT TRUE
"""

# ============================================================================
# TESTADAS
# ============================================================================

SQL_TESTADAS = """
SELECT
    lt.valor AS valor_testada,
    lt.medida AS medida_testada,
    NULL AS face_descricao,
    NULL AS face_abreviatura
FROM
    imobiliario.lotetestada lt
WHERE
    lt.cadastro = {cadastro}
ORDER BY
    lt.idkey
"""

# ============================================================================
# LOTEAMENTO
# ============================================================================

SQL_LOTEAMENTO = """
SELECT
    lot.nome AS nome,
    lot.nrolotes AS nro_lotes,
    lot.nrocaucionados AS nro_caucionados
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.loteamento lot
    ON lot.idkey = l.idkey_loteamento
WHERE
    l.cadastro = {cadastro}
    AND lot.nome IS NOT NULL
"""

# ============================================================================
# CONDOMÍNIO
# ============================================================================

SQL_CONDOMINIO = """
SELECT
    c.nome AS condominio_nome,
    CASE
        WHEN ct.descricao ILIKE '%vertical%' THEN 'VERTICAL'
        WHEN ct.descricao ILIKE '%horizontal%' THEN 'HORIZONTAL'
        ELSE 'VERTICAL'
    END AS tipo_condominio
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.condominio c
    ON c.idkey = l.idkey_condominio
LEFT JOIN
    imobiliario.condominiotipo ct
    ON ct.idkey = c.idkey_condominiotipo
WHERE
    l.cadastro = {cadastro}
    AND c.nome IS NOT NULL
"""

# ============================================================================
# DISTRITO
# ============================================================================

SQL_DISTRITO = """
SELECT
    d.nome AS distrito_nome
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.distrito d
    ON d.idkey = l.idkey_distrito
WHERE
    l.cadastro = {cadastro}
    AND d.nome IS NOT NULL
"""

# ============================================================================
# SETOR
# ============================================================================

SQL_SETOR = """
SELECT
    s.nome AS setor_nome
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.setor s
    ON s.idkey = l.idkey_setor
WHERE
    l.cadastro = {cadastro}
    AND s.nome IS NOT NULL
"""

# ============================================================================
# IMOBILIÁRIA
# ============================================================================

SQL_IMOBILIARIA = """
SELECT
    i.idkey AS codigo,
    i.nome AS nome,
    i.cpfcnpj AS cpf_cnpj
FROM
    imobiliario.lote l
LEFT JOIN
    imobiliario.imobiliaria i
    ON i.idkey = l.idkey_imobiliaria
WHERE
    l.cadastro = {cadastro}
    AND i.nome IS NOT NULL
"""

# Placeholders para queries não implementadas ainda
SQL_ENDERECO_IMOVEL = """
SELECT NULL LIMIT 0
"""

SQL_AGRUPAMENTO = """
SELECT NULL LIMIT 0
"""

SQL_SECAO = """
SELECT NULL LIMIT 0
"""
