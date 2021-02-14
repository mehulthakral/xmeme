#!/bin/bash

sudo apt install -y mysql-server

mysql -u root -e "CREATE DATABASE xmeme"

mysql -u root -p xmeme < backend/xmeme.sql

pip install -r requirements.txt