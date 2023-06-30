#!/bin/bash

cd src/Django/NFTigers

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
