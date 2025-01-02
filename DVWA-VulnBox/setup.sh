#!/bin/bash

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

# Update package list and install required packages
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y apache2 mysql-server openjdk-11-jdk php php-mysqli php-gd libapache2-mod-php git wget apt-transport-https

# "Setting up Elasticsearch GPG key and repository..."
sudo wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-archive-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list

sudo apt update -y && sudo apt upgrade -y

# Enabling Filebeat service
sudo apt install filebeat
sudo systemctl enable filebeat

# Download DVWA
cd /var/www/html
sudo git clone https://github.com/digininja/DVWA.git
sudo chmod -R 777 DVWA

# Configure DVWA
cd DVWA/config
sudo cp config.inc.php.dist config.inc.php