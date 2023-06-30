#!/bin/bash

echo "Consider dropping all tables before continuing"
echo "(Press ENTER to continue)"
read

cd ./src/Django/NFTigers

python3 manage.py migrate --fake auctions zero
python3 manage.py migrate --fake users zero

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python3 manage.py makemigrations

python3 manage.py migrate --fake-initial

# python3 manage.py migrate auctions zero
# python3 manage.py migrate

# inspiration:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
# https://dev.to/rawas_aditya/how-to-reset-django-migrations-169o
