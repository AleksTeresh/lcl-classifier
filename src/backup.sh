#!/bin/bash

source ./.env

mkdir -p backup

pg_dump "host=195.148.21.214 port=5432 dbname=postgres user=postgres password=$POSTGRES_PASSWORD" -f ./backup/$(date '+%Y-%m-%d').sql

psql "host=195.148.21.214 port=5432 dbname=postgres user=postgres password=$POSTGRES_PASSWORD" -c "\copy (SELECT ROW_TO_JSON(t) 
FROM (SELECT * FROM problems) t)
TO '$PWD/backup/$(date '+%Y-%m-%d').json';"
