#!/bin/bash

docker build -t simplekv:v1 .
docker-compose down
docker-compose up -d
