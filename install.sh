#!/bin/bash

sudo apt -y update

sudo apt install -y mysql-server

sudo systemctl enable mysql

sudo mysql -u root -e "CREATE DATABASE xmeme"

sudo mysql -u root xmeme < backend/xmeme.sql

sudo mysql -u root -e "USE mysql; UPDATE user SET plugin='mysql_native_password' WHERE User='root'; FLUSH PRIVILEGES;"

sudo service mysql restart

sudo apt install -y python3-pip

pip3 install -r requirements.txt
