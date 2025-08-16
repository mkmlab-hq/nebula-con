CREATE OR REPLACE TABLE  AS
SELECT
  id,
  title,
  text,
  ML.GENERATE_EMBEDDING(
    MODEL ,
    STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
  ) AS embedding
FROM
  
WHERE
  title IS NOT NULL OR text IS NOT NULL
LIMIT 1000
