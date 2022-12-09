CREATE OR REPLACE FUNCTION public.euclidian(arr1 double precision[], arr2 double precision[])
 RETURNS double precision
 LANGUAGE sql
AS $function$
select sqrt (SUM (tab.v)) as euclidian from (SELECT
     UNNEST (vec_sub (arr1, arr2)) as v) as tab;
	 $function$
