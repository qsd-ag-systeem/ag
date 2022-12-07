CREATE OR REPLACE FUNCTION public.vec_sub(arr1 double precision[], arr2 double precision[])
 RETURNS double precision[]
 LANGUAGE sql
 STRICT
AS $function$
SELECT array_agg (result)
    FROM (SELECT (val1 - val2) * (val1 - val2)
        AS result
        FROM (SELECT UNNEST ($1) AS val1
               , UNNEST ($2) AS val2) tuple) inn;
	$function$