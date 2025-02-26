WITH vars as (
	select 900 as numLote
), dados AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY Id) AS linha, -- Numera as linhas sequencialmente
        rowid % vars.numLote as test, 
        *
    FROM dadosapi, vars
)
SELECT 
    (linha - 1) / vars.numLote AS grupo,
    json_group_array(json_object('email',  email))
FROM dados, vars
GROUP BY grupo
ORDER BY grupo;
