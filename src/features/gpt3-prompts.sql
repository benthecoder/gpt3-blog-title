DECLARE score_threshold INT64 DEFAULT 200;

WITH
    base_tb AS (
        SELECT
            title,
            claps
        FROM
            `mlops-zoomcamp-361419`.gpt3_blog.medium
    ),

    good_stories AS (
        SELECT
            *
        FROM
            base_tb
        WHERE
            claps >= score_threshold
    ),

    bad_stories AS (
        SELECT
            *
        FROM
            base_tb
        WHERE
            -- sample n rows by doing RAND() < [prop of good post to bad post], vectorized and in O(1) time
            -- other option is ORDER BY RAND() LIMIT N but O(nlogn) time
            RAND() < (SELECT COUNT(*) FROM good_stories) / ((SELECT COUNT(*) FROM base_tb) - (SELECT COUNT(*) FROM good_stories))
        AND
            claps < score_threshold
    ),

    all_stories AS (
        SELECT
            *
        FROM
            good_stories
        UNION ALL (
            SELECT
                *
            FROM
                bad_stories
        )
    )

SELECT DISTINCT
  CONCAT("Title: ", title, " ->") AS prompt,
  IF (claps >= score_threshold, " good", " bad") AS completion
FROM
    all_stories;
