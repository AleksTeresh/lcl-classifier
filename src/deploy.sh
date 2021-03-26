#!/bin/bash

sh ./backup.sh

sh ./sync-sources.sh

sh ./spinup-docker.sh
