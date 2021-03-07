#!/bin/bash

pg_dumpall -h 195.148.21.214 -U postgres -f ./backup/$(date '+%Y-%m-%d').sql

psql -h 195.148.21.214 -U postgres -c "\copy (SELECT ROW_TO_JSON(t) 
FROM (SELECT * FROM problems) t)
TO '$PWD/backup/$(date '+%Y-%m-%d').json';"
