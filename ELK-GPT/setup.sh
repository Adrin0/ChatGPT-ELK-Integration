#!/bin/bash

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

echo "Updating system and installing prerequisites..."
apt update && apt upgrade -y
apt install -y wget curl apt-transport-https openjdk-11-jdk docker.io

echo "Installing docker-compose"
sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Setting up Elasticsearch GPG key and repository..."
sudo wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-archive-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list

echo "Installing ELK Stack components..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y elasticsearch logstash kibana

echo "Enabling and starting services..."
systemctl enable --now elasticsearch
systemctl enable --now kibana
systemctl enable --now logstash

echo "Setup complete! Ready for docker-compose up"