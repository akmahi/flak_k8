import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DB=os.getenv('DB')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')


psql_connection = psycopg2.connect(host=HOST, port=PORT, database=DB, user=USER, password=PASSWORD)
psql_connection.autocommit = True

ERROR_CODES = {400: "Key not found", 500: "Internal Server Error", 201: "Employee added", 200: "Success", 204: "Not Found", 403: "Duplicate Entry" }

def create_table():
    query = """
            CREATE TABLE IF NOT EXISTS accounts (
            id serial PRIMARY KEY,
            age INT NOT NULL,
            name VARCHAR ( 50 ) UNIQUE NOT NULL
        )
    """
    cur = psql_connection.cursor()
    cur.execute(query)



