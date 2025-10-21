"""
Módulo centralizado com todas as queries SQL para extração de dados do imóvel.
Organizado por domínio de dados (dados básicos, endereço, proprietários, etc.).

Baseado na estrutura real do banco de dados GEON.
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
    'ATIVADO' AS situacao
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
# ENDEREÇO DO IMÓVEL
# ============================================================================

SQL_ENDERECO_IMOVEL = """
SELECT 
    l.numero AS numero,
    l.complemento AS complemento,
    l.apartamento AS apartamento,
    l.bloco AS bloco,
    l.cep AS cep,
    tl.descricao AS tipo_logradouro,
    log.nome AS logradouro_nome,
    b.nome AS bairro_nome,
    d.nome AS distrito_nome,
    m.nome AS municipio_nome,
    m.uf AS uf
FROM 
    imobiliario.lote l
LEFT JOIN 
    imobiliario.logradouro log 
    ON log.idkey = l.idkey_logradouro
LEFT JOIN 
    imobiliario.tipologradouro tl 
    ON tl.idkey = log.idkey_tipologradouro
LEFT JOIN 
    imobiliario.bairro b 
    ON b.idkey = l.idkey_bairro
LEFT JOIN 
    imobiliario.distrito d 
    ON d.idkey = l.idkey_distrito
LEFT JOIN 
    geral.municipio m 
    ON m.idkey = log.idkey_municipio
WHERE 
    l.cadastro = {cadastro}
"""

# ============================================================================
# PROPRIETÁRIO E RESPONSÁVEIS
# ============================================================================

SQL_PROPRIETARIO = """
SELECT 
    lp.idkey_pessoa AS codigo,
    p.nome AS nome,
    p.cpfcnpj AS cpf_cnpj,
    lp.tipo AS tipo_vinculo
FROM 
    imobiliario.lotepessoa lp
LEFT JOIN 
    imobiliario.pessoa p 
    ON p.idkey = lp.idkey_pessoa
WHERE 
    lp.cadastro = {cadastro}
    AND lp.tipo = 1  -- Proprietário
    AND lp.ativo IS TRUE
ORDER BY 
    lp.idkey 
LIMIT 1
"""

SQL_CORRESPONSAVEL = """
SELECT 
    lp.idkey_pessoa AS codigo,
    p.nome AS nome,
    p.cpfcnpj AS cpf_cnpj
FROM 
    imobiliario.lotepessoa lp
LEFT JOIN 
    imobiliario.pessoa p 
    ON p.idkey = lp.idkey_pessoa
WHERE 
    lp.cadastro = {cadastro}
    AND lp.tipo = 2  -- Corresponsável
    AND lp.ativo IS TRUE
ORDER BY 
    lp.idkey 
LIMIT 1
"""

SQL_TODOS_RESPONSAVEIS = """
SELECT 
    lp.idkey_pessoa AS codigo,
    p.nome AS nome,
    p.cpfcnpj AS cpf_cnpj,
    lp.tipo AS tipo_vinculo
FROM 
    imobiliario.lotepessoa lp
LEFT JOIN 
    imobiliario.pessoa p 
    ON p.idkey = lp.idkey_pessoa
WHERE 
    lp.cadastro = {cadastro}
    AND lp.ativo IS TRUE
ORDER BY 
    lp.tipo, lp.idkey
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
    f.descricao AS face_descricao,
    f.abreviatura AS face_abreviatura
FROM 
    imobiliario.lotetestada lt
LEFT JOIN 
    imobiliario.face f 
    ON f.idkey = lt.idkey_face
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
        WHEN c.tipo = 1 THEN 'VERTICAL'
        WHEN c.tipo = 2 THEN 'HORIZONTAL'
        ELSE 'VERTICAL'
    END AS tipo_condominio,
    tl.descricao AS tipo_logradouro,
    log.nome AS logradouro_nome,
    m.nome AS municipio_nome,
    m.uf AS uf
FROM 
    imobiliario.lote l
LEFT JOIN 
    imobiliario.condominio c 
    ON c.idkey = l.idkey_condominio
LEFT JOIN 
    imobiliario.logradouro log 
    ON log.idkey = c.idkey_logradouro
LEFT JOIN 
    imobiliario.tipologradouro tl 
    ON tl.idkey = log.idkey_tipologradouro
LEFT JOIN 
    geral.municipio m 
    ON m.idkey = log.idkey_municipio
WHERE 
    l.cadastro = {cadastro}
    AND c.nome IS NOT NULL
"""

# ============================================================================
# AGRUPAMENTO
# ============================================================================

SQL_AGRUPAMENTO = """
SELECT 
    a.descricao AS descricao
FROM 
    imobiliario.lote l
LEFT JOIN 
    imobiliario.agrupamento a 
    ON a.idkey = l.idkey_agrupamento
WHERE 
    l.cadastro = {cadastro}
    AND a.descricao IS NOT NULL
"""

# ============================================================================
# SEÇÃO
# ============================================================================

SQL_SECAO = """
SELECT 
    s.secao AS secao
FROM 
    imobiliario.lote l
LEFT JOIN 
    imobiliario.secao s 
    ON s.idkey = l.idkey_secao
WHERE 
    l.cadastro = {cadastro}
    AND s.secao IS NOT NULL
"""

# ============================================================================
# IMOBILIÁRIA
# ============================================================================

SQL_IMOBILIARIA = """
SELECT 
    p.idkey AS codigo,
    p.nome AS nome,
    p.cpfcnpj AS cpf_cnpj
FROM 
    imobiliario.lote l
LEFT JOIN 
    imobiliario.pessoa p 
    ON p.idkey = l.idkey_imobiliaria
WHERE 
    l.cadastro = {cadastro}
    AND p.nome IS NOT NULL
"""
