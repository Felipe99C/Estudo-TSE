WITH tb_cand as (

select  
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
       sum(CAST(REPLACE(VR_BEM_CANDIDATO,',','.') as DECIMAL(15,2))) as total_BEM_CANDIDATO
FROM tb_bens
GROUP BY 1
),


tb_info_completo_cand as (
select t1.*,
        coalesce(t2.total_BEM_CANDIDATO,0) as total_bens
FROM tb_cand as t1
LEFT JOIN tb_total_bens as t2 
on t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
),

-- select 
--     SG_PARTIDO,
--     NM_PARTIDO,
--     avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_feminino,
--     avg(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
--     avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca
-- FROM tb_info_completo_cand
-- group by 1,2
-- order by 3 DESC

tb_group_uf as (
select 
    SG_PARTIDO,
    NM_PARTIDO,
    SG_UF,
    avg(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS tx_gen_feminino,
    sum(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS total_gen_feminino,
    avg(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta_parda,
    sum(CASE WHEN DS_COR_RACA in ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS total_cor_raca_preta_parda,
    avg(CASE WHEN DS_COR_RACA in ('PRETA') THEN 1 ELSE 0 END) AS tx_cor_raca_preta,
    sum(CASE WHEN DS_COR_RACA in ('PRETA') THEN 1 ELSE 0 END) AS total_cor_raca_preta,
    avg(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS tx_cor_raca_nao_branca,
    sum(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS total_cor_raca_nao_branca,
    count(*) as total_candidaturas    
FROM tb_info_completo_cand as t1
group by 1,2,3
),


tb_group_br as (

 SELECT 
     SG_PARTIDO,
     NM_PARTIDO,
     'BR' AS SG_UF,
     1.0 * sum(total_gen_feminino) / sum (total_candidaturas) as tx_gen_feminino,
     sum(total_gen_feminino) as total_gen_feminino, 

     1.0 * sum(total_cor_raca_nao_branca) / sum (total_candidaturas) as tx_cor_raca_nao_branca,
     sum(total_cor_raca_nao_branca) as total_cor_raca_nao_branca,

     1.0 *sum(total_cor_raca_preta_parda) / sum (total_candidaturas) as tx_cor_raca_preta_parda,
     sum(total_cor_raca_preta_parda) as total_cor_raca_preta_parda,

     1.0 * sum(total_cor_raca_preta) / sum (total_candidaturas) as tx_cor_raca_preta,
     sum(total_cor_raca_preta) as total_cor_raca_preta,

    sum (total_candidaturas) as total_candidaturas

 from tb_group_uf
 GROUP by 1,2,3
     ),

tb_union_all as (
select * from tb_group_br

UNION ALL

select * from tb_group_uf
)

select * from tb_union_all
--WHERE SG_PARTIDO = 'UP'
--where SG_UF = "SP"