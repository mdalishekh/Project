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
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


# Setting Up Logger instead of print()
# def setup_logger():
#     logger = logging.getLogger(__name__)
#     logger.setLevel(level=logging.DEBUG)
#     console_handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)
#     return logger 
# LOGGER = setup_logger()



# Defining Database parameters for Postgres SQL
DB_PARAMETER = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

# Email sending credentials
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')

# Building a connection with Postgres SQL 
def db_connection():
        try:
            connection = psycopg2.connect(**DB_PARAMETER)
            return connection
        except Exception as e:
            logging.error(f"Error while connecting to database: {str(e)}")
            
# This varriable stores database connection            
DB_CONNECTION = db_connection()

# # Setting a table name to be created in run time 
# REGISTRAION_TABLE_NAME  = 'registration_details'
# OTP_TABLE_NAME = 'registration_otp_verification'
# FORGOT_PASSWORD_OTP_TABLE_NAME = 'forgot_password_otp_verification'
            
# # This function is responsible to insert user's registration data into database            
# def registration_insert_query():
#     query = f'''
#             INSERT INTO {REGISTRAION_TABLE_NAME} (
#                 user_email, 
#                 first_name, 
#                 last_name, 
#                 phone_number, 
#                 user_password, 
#                 registration_date, 
#                 registration_time
#             )
#             VALUES (%s, %s, %s, %s, %s, %s, %s);
#             '''        
#     return query        

# # Creating a table in Postgres SQL for Registraion
# def registration_create_query():
#     query = f'''
#             CREATE TABLE {REGISTRAION_TABLE_NAME} (
#                 ID SERIAL PRIMARY KEY,
#                 user_email VARCHAR,         
#                 first_name VARCHAR,         
#                 last_name VARCHAR,          
#                 phone_number BIGINT,        
#                 user_password VARCHAR,      
#                 registration_date DATE,     
#                 registration_time TIME      
#             );
#             '''
#     return query        


# #  Creating a table in Postgres SQL for OTP verification    
# def otp_verification_create_query():
#     query = f'''
#              CREATE TABLE {OTP_TABLE_NAME} (
#                 ID SERIAL PRIMARY KEY,
#                 user_email VARCHAR,
#                 OTP VARCHAR,
#                 is_valid BOOLEAN,
#                 otp_date DATE,
#                 otp_time TIME
#             );
#             '''       
#     return query

# # This function is responsible to insert user's registration OTP data into database
# def otp_insert_query():
#     query = f'''
#             INSERT INTO {OTP_TABLE_NAME} (user_email, OTP, is_valid, otp_date, otp_time)
#             VALUES (%s, %s, %s, %s, %s);
#              '''
#     return query

# # OTP validator fetch query
# FETCH_OTP = f"SELECT otp, is_valid FROM {OTP_TABLE_NAME} WHERE user_email = %s"



# # This function is resposible for returning a query to check the table exists or not 
# def is_table_exist_query(table_name):
#     query = f"""
#                 SELECT EXISTS (
#                 SELECT 1 
#                 FROM information_schema.tables 
#                 WHERE table_name = '{table_name}'
#             );
#             """ 
#     return query        

# # This function is responsible for returning a query to update OTP
# def update_otp_query(table_name):
#     otp_update_query = f"""
#                     UPDATE {table_name}
#                     SET otp = %s, is_valid = true,
#                     otp_date = %s, otp_time = %s
#                     WHERE user_email = %s;
#                     """
#     return  otp_update_query


# # Creating table For , Forgot password otp verification
# def forgot_password_otp_create_query():
#     query = f'''
#              CREATE TABLE {FORGOT_PASSWORD_OTP_TABLE_NAME} (
#                 ID SERIAL PRIMARY KEY,
#                 user_email VARCHAR,
#                 OTP VARCHAR,
#                 is_valid BOOLEAN,
#                 otp_date DATE,
#                 otp_time TIME
#             );
#             '''       
#     return query

# # This function is responsible to insert forgot password OTP data into database
# def forgot_otp_insert_query():
#     query = f'''
#             INSERT INTO {FORGOT_PASSWORD_OTP_TABLE_NAME} (user_email, OTP, is_valid, otp_date, otp_time)
#             VALUES (%s, %s, %s, %s, %s);
#              '''
#     return query