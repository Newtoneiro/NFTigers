import cx_Oracle
import random
import hashlib
import os


def execute(sql_command):
    try:
        cursor.execute(sql_command)
    except Exception as e:
        print(f'ERROR: {e}')
        if len(sql_command) < 100:
            print('COMMAND:')
            for line in sql_command.split('\n'):
                print(f'    {line}')
        else:
            print('(not displaying command beacuse it is very long)')
        print()


# detect graphics
DIR_PATH = 'scripts/graphics'
graphics = []
for path in os.listdir(DIR_PATH):
    graphics.append(os.path.join(DIR_PATH, path))
graphics_iter = iter(graphics)

# connect to DB
with open('src/Django/NFTigers/NFTigers/.env', 'r') as file:
    lines = [line.strip() for line in file]

name = lines[0].replace('DB_NAME=', '')
user = lines[1].replace('DB_USER=', '')
password = lines[2].replace('DB_PASSWORD=', '')

nft_id = 0

with cx_Oracle.connect(
    user=user,
    password=password,
    dsn=name,
    encoding='UTF-8'
) as connection:
    cursor = connection.cursor()

    with open('scripts/db/seed.sql') as file:
        sql = file.read()
        sql_commands = sql.split(';')
        sql_commands = [
            command.strip() for command in sql_commands
            if command.strip() and ('--') not in command
        ]

    for sql_command in sql_commands:
        # add token and graphic
        if 'INSERT INTO SCHOOLWORKS' in sql_command:
            token = hashlib.sha256(
                str(random.random()).encode('utf-8')
            ).hexdigest()
            sql_command = sql_command.replace('token', token)

            execute(sql_command)

            with open(next(graphics_iter), 'rb') as f:
                img_data = f.read()
                cursor.execute(
                    'UPDATE SCHOOLWORKS SET GRAPHIC = :image WHERE NFT_ID = :id',
                    image=img_data, id=nft_id
                )

            nft_id += 1
        else:
            execute(sql_command)

    connection.commit()
    cursor.close()
