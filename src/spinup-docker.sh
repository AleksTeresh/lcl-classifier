#!/bin/bash

ssh -l ubuntu 195.148.21.214 "cd /home/ubuntu/projects/lcl-classifier/newvolume/src; docker-compose up --build --force-recreate -d; rm .env"
