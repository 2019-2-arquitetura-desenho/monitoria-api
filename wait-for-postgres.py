#Check if postgres is running or not
import psycopg2
import time

while True:
    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='monitoria-db'")
        print('Connected')
        break
    except Exception as ex:
        print('Waiting for DB connection')
        time.sleep(0.5)
