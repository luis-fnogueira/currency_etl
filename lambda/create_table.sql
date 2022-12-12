CREATE TABLE IF NOT EXISTS public.currency
(
	id bigint identity(1, 1),
	code VARCHAR(256)   ENCODE lzo
	,codein VARCHAR(256)   ENCODE lzo
	,name VARCHAR(256)   ENCODE lzo
	,high NUMERIC(5,4)   ENCODE az64
	,low NUMERIC(5,4)   ENCODE az64
	,varbid NUMERIC(5,4)   ENCODE az64
	,pctchange NUMERIC(5,4)   ENCODE az64
	,bid NUMERIC(5,4)   ENCODE az64
	,ask NUMERIC(5,4)   ENCODE az64
	,create_date TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"timestamp" INTEGER   ENCODE az64
);