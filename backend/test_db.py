
import mysql.connector
from dotenv import load_dotenv
import os

# Load .env from the current backend folder
load_dotenv(dotenv_path=".env", override=True)

# Read database details
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

print("Host loaded:", bool(db_host))
print("Username loaded:", bool(db_user))
print("Password loaded:", bool(db_password))
print("Database loaded:", bool(db_name))

connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

print("MySQL Connected Successfully!")

connection.close()
