#!/bin/bash

ssh -l ubuntu 195.148.21.214 "mkdir -p /home/ubuntu/projects/lcl-classifier/newvolume/src; cd /home/ubuntu/projects/lcl-classifier/newvolume/src; rm -rf ./client; rm -rf ./server"

rsync -a --exclude 'client/node_modules' --exclude 'postgres' --exclude 'backup' --exclude 'data' ./ ubuntu@195.148.21.214:/home/ubuntu/projects/lcl-classifier/newvolume/src
