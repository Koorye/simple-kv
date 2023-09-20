#!/bin/bash

docker build -t simplekv:v1 .
docker network create simplekv_rdp
docker-compose down
docker-compose up -d
