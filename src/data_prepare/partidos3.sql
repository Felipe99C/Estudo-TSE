WITH tb_cand as (

select  DISTINCT
        NM_CANDIDATO,
        SQ_CANDIDATO,
        SG_UF,
        DS_CARGO,
        SG_PARTIDO,
        NM_PARTIDO,
        DT_NASCIMENTO,
        DS_GENERO,
        DS_GRAU_INSTRUCAO,
        DS_COR_RACA,
        DS_ESTADO_CIVIL,
        DS_OCUPACAO

from tb_candidatos
),

tb_total_bens as (

select SQ_CANDIDATO,
       sum(CAST(REPLACE(VR_BEM_CANDIDATO,',','.') as DECIMAL(20,2))) as totalBens
FROM tb_bens
GROUP BY 1
),


tb_info_completo_cand as (
select t1.*,
        coalesce(t2.totalBens,0) as totalBens,
        date('now') - date(
           substr(DT_NASCIMENTO, 7, 4) || '-' || 
            substr(DT_NASCIMENTO, 4, 2) || '-' || 
            substr(DT_NASCIMENTO, 1, 2)
        ) AS NR_IDADE 

FROM tb_cand as t1
LEFT JOIN tb_total_bens as t2 
on t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
),

tb_group_uf as (
select 
    SG_PARTIDO,
    NM_PARTIDO,
    'GERAL' as DS_CARGO,
    SG_UF,
    avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_gen_feminino,
    sum(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS total_gen_feminino,
    avg(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta_parda,
    sum(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS total_cor_raca_preta_parda,
    avg(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
    sum(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS total_cor_raca_preta,
    avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca,
    sum(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS total_cor_raca_nao_branca,
    SUM(totalBens) as totalBens,
    avg(totalBens) as avgBens,
    COALESCE(avg(case when totalBens > 1 then totalBens end),0) as avgBensNotZero,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='CASADO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilCasado,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='SOLTEIRO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSolteiro,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL IN ('DIVORCIADO(A))', 'SEPARADO(A) JUDICIALMENTE') THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSeparadoDivorciado,
    AVG(NR_IDADE) AS avgIdade,
    count(*) AS total_candidaturas    
FROM tb_info_completo_cand as t1
group by 1,2,3,4
),


tb_group_br as (
 select 
    SG_PARTIDO,
    NM_PARTIDO,
    'GERAL' as DS_CARGO,
    'BR' as SG_UF,
    avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_gen_feminino,
    sum(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS total_gen_feminino,
    avg(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta_parda,
    sum(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS total_cor_raca_preta_parda,
    avg(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
    sum(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS total_cor_raca_preta,
    avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca,
    sum(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS total_cor_raca_nao_branca,
    SUM(totalBens) as totalBens,
    avg(totalBens) as avgBens,
    COALESCE(avg(case when totalBens > 1 then totalBens end),0) as avgBensNotZero,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='CASADO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilCasado,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='SOLTEIRO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSolteiro,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL IN ('DIVORCIADO(A))', 'SEPARADO(A) JUDICIALMENTE') THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSeparadoDivorciado,
    AVG(NR_IDADE) AS avgIdade,
    count(*) AS total_candidaturas    

FROM tb_info_completo_cand as t1
group by 1,2,3,4
     ),

tb_group_cargo_uf AS (

 select 
    SG_PARTIDO,
    NM_PARTIDO,
    DS_CARGO,
    SG_UF,
    avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_gen_feminino,
    sum(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS total_gen_feminino,
    avg(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta_parda,
    sum(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS total_cor_raca_preta_parda,
    avg(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
    sum(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS total_cor_raca_preta,
    avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca,
    sum(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS total_cor_raca_nao_branca,
    SUM(totalBens) as totalBens,
    avg(totalBens) as avgBens,
    COALESCE(avg(case when totalBens > 1 then totalBens end),0) as avgBensNotZero,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='CASADO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilCasado,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='SOLTEIRO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSolteiro,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL IN ('DIVORCIADO(A))', 'SEPARADO(A) JUDICIALMENTE') THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSeparadoDivorciado,
    AVG(NR_IDADE) AS avgIdade,
    count(*) AS total_candidaturas    

FROM tb_info_completo_cand as t1
group by 1,2,3,4
),

tb_group_cargo_br AS (
     select 
    SG_PARTIDO,
    NM_PARTIDO,
    DS_CARGO,
    'BR' AS SG_UF,
    avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_gen_feminino,
    sum(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS total_gen_feminino,
    avg(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta_parda,
    sum(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS total_cor_raca_preta_parda,
    avg(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
    sum(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS total_cor_raca_preta,
    avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca,
    sum(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS total_cor_raca_nao_branca,
    SUM(totalBens) as totalBens,
    avg(totalBens) as avgBens,
    COALESCE(avg(case when totalBens > 1 then totalBens end),0) as avgBensNotZero,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='CASADO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilCasado,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL='SOLTEIRO(A)' THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSolteiro,
    1.0 * SUM(CASE WHEN DS_ESTADO_CIVIL IN ('DIVORCIADO(A))', 'SEPARADO(A) JUDICIALMENTE') THEN 1 ELSE 0 END) / count(*) AS txEstadoCivilSeparadoDivorciado,
    AVG(NR_IDADE) AS avgIdade,
    count(*) AS total_candidaturas    

FROM tb_info_completo_cand as t1
group by 1,2,3,4
),

tb_union_all as (

select * from tb_group_br

UNION ALL

select * from tb_group_uf

union ALL

SELECT * FROM tb_group_cargo_br

UNION ALL

SELECT * FROM tb_group_cargo_uf

)

select * from tb_union_all
--where sg_uf = 'SP' and ds_cargo = 'PREFEITO'
