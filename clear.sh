#!/bin/bash

docker images -a -q | xargs docker rmi
sleep 2
docker images
