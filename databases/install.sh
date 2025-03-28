#!/bin/sh

# postgresql stuff
sudo apt-get update -y
sudo apt-get install libpq-dev python3-dev -y

# mssql obdc 
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update -y
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18

# pip modules
cat requirements.txt | xargs -I {} pip install {} --no-cache --break-system-packages
cat requirements.txt | xargs -I {} pip3 install {} --no-cache --break-system-packages

