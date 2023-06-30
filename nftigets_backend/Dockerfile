FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY . .

RUN pip install --upgrade pip

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN apt-get update && apt-get install -y unzip

RUN apt-get update && apt-get install -y wget

RUN apt-get update && apt-get install -y curl

RUN pip install cx_Oracle --upgrade

RUN mkdir -p /opt/oracle

WORKDIR /opt/oracle

RUN wget https://download.oracle.com/otn_software/linux/instantclient/218000/instantclient-basic-linux.x64-21.8.0.0.0dbru.zip

RUN unzip instantclient-basic-linux.x64-21.8.0.0.0dbru.zip 

RUN apt-get install libaio1

RUN sh -c "echo /opt/oracle/instantclient_21_8 > /etc/ld.so.conf.d/oracle-instantclient.conf"

RUN ldconfig

RUN export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_8:$LD_LIBRARY_PATH

EXPOSE 8000

CMD ["python3", "/code/src/Django/NFTigers/manage.py", "runserver", "0.0.0.0:8000"]