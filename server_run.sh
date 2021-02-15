#!/bin/bash

cd backend

python3 main_local.py &

python3 main_swagger.py &
