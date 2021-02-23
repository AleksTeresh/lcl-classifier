#!/bin/bash

rsync -chavzP --rsync-path="sudo rsync" --stats ubuntu@195.148.21.214:/home/ubuntu/projects/lcl-classifier/newvolume/src/postgres ./backup/
