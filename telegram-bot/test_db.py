import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)

    print("Successfully connected to PostgreSQL!")

    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)