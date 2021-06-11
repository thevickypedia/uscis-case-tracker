#!/bin/bash

### BEFORE RUNNING THIS SCRIPT MAKE SURE TO COMMENT THE BELOW UNNECESSARY PARTS

# looks for brew installation and installs only if brew is not found in /usr/local/bin
brew_check=$(which brew)
brew_condition="/usr/local/bin/brew"
if [[ "$brew_check" != "$brew_condition" ]]; then
  echo "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  else echo "Found Homebrew, skipping installation"
fi

# looks for git and installs only if git is not found in /usr/bin or /usr/local/bin (if installed using brew)
docker_check=$(which docker)
docker_condition="/usr/local/bin/docker"
if [[ "$docker_check" == "$docker_condition" ]]; then
  echo "Found Docker, skipping installation"
  else echo "Refer Docker installation steps: https://medium.com/crowdbotics/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3"
  exit
fi

echo -e "\n**********************************************************************************************************"
echo "RUNNING THIS STEP WILL DELETE ALL YOUR DOCKER CONTAINERS INCLUDING THE DOCKER IMAGES"
echo "**********************************************************************************************************"
read -p "Are you sure you want to continue? <Y/N> " prompt
if [[ $prompt =~ [yY](es)* ]]
then
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
fi

echo -e "\n**********************************************************************************************************"
echo "RUNNING THIS STEP WILL BUILD AN IMAGE FOR USCIS-CASE-TRACKER AND RUN IT"
echo "**********************************************************************************************************"
read -p "Are you sure you want to continue? <Y/N> " prompt
if [[ $prompt =~ [yY](es)* ]]
then

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
  else
    echo "GOOD BYE"
fi
done