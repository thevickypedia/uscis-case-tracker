#!/bin/bash

### BEFORE RUNNING THIS SCRIPT MAKE SURE TO COMMENT THE BELOW UNNECESSARY PARTS
### RUNNING THIS SCRIPT AS IT IS WILL DELETE ALL YOUR DOCKER CONTAINERS INCLUDING THE DOCKER IMAGES

# stops all existing docker containers
echo -e '\n**********************************************************************************************'
echo Stopping Containers
echo -e '**********************************************************************************************'
# shellcheck disable=SC2046
docker stop $(docker ps -a -q)

# deletes all existing docker containers
echo -e '\n**********************************************************************************************'
echo Deleting Idle Containers
echo -e '**********************************************************************************************'
# shellcheck disable=SC2046
docker rm $(docker ps -a -q)

# force deletes all existing docker images
echo -e '\n**********************************************************************************************'
echo Executing Force Deletion of Docker Images
echo -e '**********************************************************************************************'
# shellcheck disable=SC2046
docker rmi $(docker images -q) -f

# builds docker image uscis with tag 1.0
echo -e '\n**********************************************************************************************'
echo Bulding New Docker Image
echo -e '**********************************************************************************************'
docker build -t uscis:1.0 .

# runs the docker image
echo -e '\n**********************************************************************************************'
echo Running Docker Image uscis:1.0
echo -e '**********************************************************************************************'
docker run uscis:1.0
