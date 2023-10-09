#!/bin/bash

mkdir /home/ec2-user/geoservices

# Change to the directory containing your docker-compose.yml file
cd /home/ec2-user/geoservices

sudo yum update -y

sudo amazon-linux-extras install docker httpd -y

sudo pip3 install docker-compose

sudo systemctl enable docker

sudo systemctl start docker

sudo yum install git -y

sudo curl -o https://github.com/AitazazGilani/STAIRS_CHASR/blob/main/docker-compose.yml

# Start the services defined in docker-compose.yml in detached mode
docker-compose up -d
