# SELECTS para ATUALIZAÇÃO

# ------------------------------------------------------------------

# Tipo do Terreno (LOTE)
sql_tipo_imovel = """SELECT DISTINCT 
	CASE 
		WHEN lt.descricao LIKE 'PREDIAL' THEN 'P'
		WHEN lt.descricao LIKE 'TERRITORIAL' THEN 'T'
	END AS descricao
FROM 
	imobiliario.lote l 
LEFT JOIN 
	imobiliario.lotetipoimovel lt 
	ON lt.idkey = l.idkey_tipoimovel 
WHERE 
	l.cadastro = {cadastro}"""

# ------------------------------------------------------------------

# quantidade edificacoes no cadastro

sql_qt_edificacoes = """SELECT 
	e.sequencia
FROM 
	imobiliario.edificacao e 
LEFT JOIN
	geo.edificacao ge
	ON ge.idkey_edificacao = e.idkey 
WHERE 
	ge.conferencia IN (2,3,4,6,7)
	AND e.demolido IS NOT TRUE
	AND e.cadastro = {cadastro}"""


sql_edif_demolida = """SELECT
	e.sequencia 
FROM 
	imobiliario.edificacao e
WHERE
	e.demolido IS TRUE
	AND e.cadastro = {cadastro}
	AND e.sequencia = {sequencia}"""

# ------------------------------------------------------------------

# Dados da Edificação

    # 2 - Área Unid. Construída | Regular
    # 3 - Área Geometria        | Irregular 
    # 4 - Área Coberta          | Nova Cadastrada 
    # 6 - Área Unid. Construída | Sobrado Regular
    # 7 - Área Descoberta       | Sobrado Irregular


sql_edificacao = """SELECT 
	COALESCE(e.codigo_integracao::int8, e.idkey::int8) AS id,
	e.sequencia ,
	CASE 
		WHEN e.principal = TRUE THEN 'S'
		ELSE 'N'
	END AS principal,
    CAST(CASE
        WHEN ge.conferencia = ANY (ARRAY[2, 6]) THEN e.areaunidconstruida::double PRECISION	-- 2-6 | Regular - Sobrado Regular
        WHEN ge.conferencia = 3 THEN st_area(ge.geom)										-- 3 | Irregular 
        WHEN ge.conferencia = 4 THEN e.areacoberta::double PRECISION 						-- 4 | Nova Cadastrada
        WHEN ge.conferencia = 7 THEN e.areadescoberta::double PRECISION						-- 7 | Sobrado Irregular
        ELSE 0
    END AS NUMERIC(15,2)) AS area_geo,
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
	AND ge.conferencia = 4"""

# ADICIONA SOMENTE NOVA CADASTRADA, PARA PISCINA DEVE ADICIONAR NESTE ULTIMO FILTRO WHERE


sql_areaunid_edificacao = """SELECT 
CAST(CASE
        WHEN ge.conferencia = ANY (ARRAY[2, 6]) THEN e.areaunidconstruida::double PRECISION	-- 2-6 | Regular - Sobrado Regular
        WHEN ge.conferencia = 3 THEN st_area(ge.geom)										-- 3 | Irregular 
        WHEN ge.conferencia = 4 THEN e.areacoberta::double PRECISION 						-- 4 | Nova Cadastrada
        WHEN ge.conferencia = 7 THEN e.areadescoberta::double PRECISION						-- 7 | Sobrado Irregular
        ELSE e.areaunidconstruida 															-- permanece a mesma
    END AS numeric(15,2)) AS area_geo
FROM 
	geo.edificacao ge
LEFT JOIN
	imobiliario.edificacao e
	ON e.idkey = ge.idkey_edificacao
WHERE
	e.cadastro = {cadastro}
	AND e.sequencia = {sequencia}"""

#================================================================================================================== 
#==================================================================================================================  BICS LOTE
#================================================================================================================== 

sql_bic_meiofio = """"""


sql_bic_ocupacao_lote = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.lote lote 
LEFT JOIN 
	imobiliario.lotebic tpl_bic 
	ON tpl_bic.idkey_lote = lote.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 1 -- Informacoes Sobre o Imovel / Ocupacao
	AND lote.cadastro = """ 

#================================================================================================================== Iluminação

sql_bic_utilizacao_lote = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.lote lote 
LEFT JOIN 
	imobiliario.lotebic tpl_bic 
	ON tpl_bic.idkey_lote = lote.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 3 -- Informacoes Sobre o Imovel / Utilizacao
	AND lote.cadastro = """

#================================================================================================================== Meio - Fio 

sql_bic_situacao_lote = """SELECT DISTINCT 
    modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.lote lote 
LEFT JOIN 
	imobiliario.lotebic tpl_bic 
	ON tpl_bic.idkey_lote = lote.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 8 -- Informacoes Sobre o Terreno / Situacao
	AND lote.cadastro = """

#================================================================================================================== 
#================================================================================================================== BICS EDIFICACAO
#==================================================================================================================  Informações da Edificação

sql_bic_tipoimovel = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 11	 -- Informações da Edificação / Tipo Imovel
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================


sql_bic_alinhamento = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 12	 -- Informações da Edificação / Alinhamento
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_localizacao = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 13	 -- Informações da Edificação / Localizacao
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================


sql_bic_posicao = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 14	 -- Informações da Edificação / Posição
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================


sql_bic_estrutura = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 15	 -- Informações da Edificação / Estrutura
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""


#==================================================================================================================

sql_bic_cobertura = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 16	 -- Informações da Edificação / Cobertura
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================


sql_bic_vedacao = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 17	 -- Informações da Edificação / Vedação
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_forro = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 18	 -- Informações da Edificação / Forro
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_revestimentoext = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 19	 -- Informações da Edificação / Revestimento Externo
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_sanitarios = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 20	 -- Informações da Edificação / Sanitarios
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""


#==================================================================================================================

sql_bic_insteletrica = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 21	 -- Informações da Edificação / Instalacao Eletrica
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_piso = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 22	 -- Informações da Edificação / Piso
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""

#==================================================================================================================

sql_bic_conservacao = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 23	 -- Informações da Edificação / Conservacao
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""


#==================================================================================================================



sql_bic_utilizacao_edif = """SELECT DISTINCT 
	modelocamporesposta.descricao AS descricao,						--0 
	modelocamporesposta.idkey AS resposta_id,						--1
    modelocamporesposta.modeloresposta  AS resposta_codigo,			--2 
    modelocamporesposta.descricao AS resposta_desc,					--3
	modelocampo.idkey  AS campo_id,									--4
	modelocampo.campo AS campo_codigo,								--5
	modelocampo.descricao AS campo_descricao,						--6
	CASE 
		WHEN modelocampo.multiresposta IS TRUE THEN 'S'
		WHEN modelocampo.multiresposta IS NOT TRUE THEN 'N'
	END::TEXT AS campo_multiresposta,								--7
	CASE
		WHEN t.idkey = 1 THEN 'P'
		WHEN t.idkey = 2 THEN 'N'
		WHEN t.idkey = 3 THEN 'T'
	END AS campo_tipo,												--8
    modelogrupo.idkey AS grupo_id,									--9
	modelogrupo.grupo AS grupo_grupo,								--10
	modelogrupo.descricao AS grupo_descricao,						--11	
	'S'::text AS segmento											--12
FROM
	imobiliario.edificacao edificacao
LEFT JOIN 
	imobiliario.edificacaobic tpl_bic 
	ON tpl_bic.idkey_edificacao = edificacao.idkey
LEFT JOIN 
	geral.biccamporespostas camporesposta -- nada
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
	modelocampo.idkey = 61	 -- Informações da Edificação / utilizacao
	AND edificacao.cadastro = {cadastro}
	AND edificacao.sequencia = {sequencia}"""