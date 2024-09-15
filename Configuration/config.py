# Importing some useful packages 
import os
import logging
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


# Current Date and Time
CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
CURRENT_TIME = datetime.now().strftime('%H:%M:%S')


# Setting Up Logger instead of print()
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    file_handler = logging.FileHandler('Logs/app.log')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger 
LOGGER = setup_logger()

# Defining Database parameters for Postgres SQL
DB_PARAMETER = {
        'dbname': os.environ['DB_NAME'],
        'user': os.environ['DB_USERNAME'],
        'password': os.environ['DB_PASSWORD'],
        'host': os.environ['DB_HOST'],
        'port': os.environ['DB_PORT']
    }

# Building a connection with Postgres SQL 
def db_connection():
        try:
            connection = psycopg2.connect(**DB_PARAMETER)
            return connection
        except Exception as e:
            logging.error(f"Error while connecting to database: {str(e)}")
            
# This varriable stores database connection            
DB_CONNECTION = db_connection()

# Setting a table name to be created in run time 
REGISTRAION_TABLE_NAME  = 'registration'
OTP_TABLE_NAME = 'otp_verification'
            
# This function is responsible to insert user's registration data into database            
def registration_insert_query():
    query = f'''
            INSERT INTO {REGISTRAION_TABLE_NAME} (
                user_email, 
                first_name, 
                last_name, 
                phone_number, 
                user_password, 
                registration_date, 
                registration_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''        
    return query        

# Creating a table in Postgres SQL for registraion
def registration_create_query():
    query = f'''
            CREATE TABLE {REGISTRAION_TABLE_NAME} (
                ID SERIAL PRIMARY KEY,
                user_email VARCHAR,         
                first_name VARCHAR,         
                last_name VARCHAR,          
                phone_number BIGINT,        
                user_password VARCHAR,      
                registration_date DATE,     
                registration_time TIME      
            );
            '''
    return query        

# This function is resposible for returning a query to check the table exists or not 
def is_table_exist_query(table_name):
    query = f"""
                SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
            """ 
    return query        