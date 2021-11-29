#!/bin/bash

echo "Deploy stage"

scp docker-compose.yaml jenkins@swarm-manager:/home/jenkins/docker-compose.yaml

ssh jenkins@swarm-manager \
    CREATE_SCHEMA=true \
    DATABASE_URI=$DATABASE_URI \
    DOCKER_HUB_CREDS_USR=$DOCKER_HUB_CREDS_USR \
    docker stack deploy --compose-file docker-compose.yaml todo-app 

