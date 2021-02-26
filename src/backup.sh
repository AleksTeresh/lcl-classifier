#!/bin/bash

pg_dumpall -h 195.148.21.214 -U postgres -f ./backup/$(date '+%Y-%m-%d').sql
