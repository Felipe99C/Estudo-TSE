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


tb_geral as (
-- Mulheres por estado
SELECT
    SG_PARTIDO,
    NM_PARTIDO,
     sum(case when SG_UF = 'SP' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_SP,
     sum(case when SG_UF = 'AM' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_AM,
     sum(case when SG_UF = 'AL' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_AL,
     sum(case when SG_UF = 'MT' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_MT,
     sum(case when SG_UF = 'MG' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_MG,
     sum(case when SG_UF = 'RJ' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_RJ,
     sum(case when SG_UF = 'BA' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_BA,
     sum(case when SG_UF = 'PB' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_PB,
     sum(case when SG_UF = 'PE' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_PE,
     sum(case when SG_UF = 'CE' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_CE,
     sum(case when SG_UF = 'MA' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_MA,
     sum(case when SG_UF = 'GO' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_GO,
     sum(case when SG_UF = 'SC' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_SC,
     sum(case when SG_UF = 'ES' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_ES,
     sum(case when SG_UF = 'MS' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_MS,
     sum(case when SG_UF = 'PR' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_PR,
     sum(case when SG_UF = 'PA' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_PA,
     sum(case when SG_UF = 'AC' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_AC,
     sum(case when SG_UF = 'SE' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_SE,
     sum(case when SG_UF = 'RO' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_RO,
     sum(case when SG_UF = 'PI' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_PI,
     sum(case when SG_UF = 'TO' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_TO,
     sum(case when SG_UF = 'RS' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_RS,
     sum(case when SG_UF = 'AP' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_AP,
     sum(case when SG_UF = 'RN' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_RN,
     sum(case when SG_UF = 'RR' THEN tx_gen_feminino ELSE 0 END) AS tx_fem_RR,
     1.0 * sum(total_gen_feminino) / sum(total_candidaturas) as tx_feminino_BR,

     sum(case when SG_UF = 'SP' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_SP,
     sum(case when SG_UF = 'AM' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_AM,
     sum(case when SG_UF = 'AL' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_AL,
     sum(case when SG_UF = 'MT' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_MT,
     sum(case when SG_UF = 'MG' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_MG,
     sum(case when SG_UF = 'RJ' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_RJ,
     sum(case when SG_UF = 'BA' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_BA,
     sum(case when SG_UF = 'PB' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_PB,
     sum(case when SG_UF = 'PE' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_PE,
     sum(case when SG_UF = 'CE' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_CE,
     sum(case when SG_UF = 'MA' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_MA,
     sum(case when SG_UF = 'GO' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_GO,
     sum(case when SG_UF = 'SC' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_SC,
     sum(case when SG_UF = 'ES' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_ES,
     sum(case when SG_UF = 'MS' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_MS,
     sum(case when SG_UF = 'PR' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_PR,
     sum(case when SG_UF = 'PA' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_PA,
     sum(case when SG_UF = 'AC' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_AC,
     sum(case when SG_UF = 'SE' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_SE,
     sum(case when SG_UF = 'RO' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_RO,
     sum(case when SG_UF = 'PI' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_PI,
     sum(case when SG_UF = 'TO' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_TO,
     sum(case when SG_UF = 'RS' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_RS,
     sum(case when SG_UF = 'AP' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_AP,
     sum(case when SG_UF = 'RN' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_RN,
     sum(case when SG_UF = 'RR' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_parda_RR,
     1.0 * sum(total_cor_raca_preta_parda) / sum (total_candidaturas) as tx_cor_raca_preta_parda_BR,
        
sum(case when SG_UF = 'SP' THEN tx_cor_raca_preta_parda else 0 end) as tx_cor_raca_preta_SP,
     sum(case when SG_UF = 'AM' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_AM,
     sum(case when SG_UF = 'AL' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_AL,
     sum(case when SG_UF = 'MT' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_MT,
     sum(case when SG_UF = 'MG' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_MG,
     sum(case when SG_UF = 'RJ' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_RJ,
     sum(case when SG_UF = 'BA' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_BA,
     sum(case when SG_UF = 'PB' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_PB,
     sum(case when SG_UF = 'PE' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_PE,
     sum(case when SG_UF = 'CE' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_CE,
     sum(case when SG_UF = 'MA' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_MA,
     sum(case when SG_UF = 'GO' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_GO,
     sum(case when SG_UF = 'SC' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_SC,
     sum(case when SG_UF = 'ES' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_ES,
     sum(case when SG_UF = 'MS' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_MS,
     sum(case when SG_UF = 'PR' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_PR,
     sum(case when SG_UF = 'PA' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_PA,
     sum(case when SG_UF = 'AC' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_AC,
     sum(case when SG_UF = 'SE' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_SE,
     sum(case when SG_UF = 'RO' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_RO,
     sum(case when SG_UF = 'PI' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_PI,
     sum(case when SG_UF = 'TO' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_TO,
     sum(case when SG_UF = 'RS' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_RS,
     sum(case when SG_UF = 'AP' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_AP,
     sum(case when SG_UF = 'RN' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_RN,
     sum(case when SG_UF = 'RR' THEN tx_cor_raca_preta else 0 end) as tx_cor_raca_preta_RR,
     1.0 * sum(total_cor_raca_preta) / sum (total_candidaturas) as tx_cor_raca_preta_BR,

     sum(case when SG_UF = 'SP' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_SP,
     sum(case when SG_UF = 'AM' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_AM,
     sum(case when SG_UF = 'AL' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_AL,
     sum(case when SG_UF = 'MT' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_MT,
     sum(case when SG_UF = 'MG' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_MG,
     sum(case when SG_UF = 'RJ' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_RJ,
     sum(case when SG_UF = 'BA' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_BA,
     sum(case when SG_UF = 'PB' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_PB,
     sum(case when SG_UF = 'PE' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_PE,
     sum(case when SG_UF = 'CE' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_CE,
     sum(case when SG_UF = 'MA' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_MA,
     sum(case when SG_UF = 'GO' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_GO,
     sum(case when SG_UF = 'SC' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_SC,
     sum(case when SG_UF = 'ES' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_ES,
     sum(case when SG_UF = 'MS' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_MS,
     sum(case when SG_UF = 'PR' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_PR,
     sum(case when SG_UF = 'PA' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_PA,
     sum(case when SG_UF = 'AC' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_AC,
     sum(case when SG_UF = 'SE' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_SE,
     sum(case when SG_UF = 'RO' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_RO,
     sum(case when SG_UF = 'PI' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_PI,
     sum(case when SG_UF = 'TO' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_TO,
     sum(case when SG_UF = 'RS' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_RS,
     sum(case when SG_UF = 'AP' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_AP,
     sum(case when SG_UF = 'RN' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_RN,
     sum(case when SG_UF = 'RR' THEN tx_cor_raca_nao_branca else 0 end) as tx_cor_raca_nao_branca_RR,
     1.0 * sum(total_cor_raca_nao_branca) / sum (total_candidaturas) as tx_cor_raca_nao_branca_br,

     sum(total_cor_raca_nao_branca) as total_cor_raca_nao_branca,
     sum(total_cor_raca_preta_parda) as total_cor_raca_preta_parda,
     sum(total_cor_raca_preta) as total_cor_raca_preta,
     sum(total_gen_feminino) as total_gen_feminino,
     sum(total_candidaturas) as total_candidaturas


 FROM tb_group_uf
 
 group by 1,2  
)


/*
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

     1.0 * sum(total_cor_raca_preta) / sum (total_cor_raca_preta) as tx_cor_raca_preta,
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
*/

select * from tb_geral
--LIMIT 10
--WHERE SG_UF = 'BR'
