# This module is specially made for performing database related tasks
# Importing some useful Packages to be used in database related tasks

from Configuration.config import *

# This function is responsibe to check if table exist or not
def is_table_exist(table_name):
    try:
        pg_cursor = DB_CONNECTION.cursor()
        pg_cursor.execute(is_table_exist_query(table_name), (table_name,))
        exists = pg_cursor.fetchone()[0]
        pg_cursor.close()
        return exists
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE CHECKING {table_name} EXISTANCE: " f"{error}")
        return False

# Filtering registraion details to be stored in database
def registration_data_filter(registration_json_data):
    # Getting resgistraion details key values
    json_data = registration_json_data['registrationDetails']
    user_email = json_data['userEmail']
    first_name = json_data['firstName']
    last_name = json_data['lastName']
    phone_number = json_data['phoneNumber']
    password = json_data['password']
    # insert values tuple 
    insert_values = (user_email, first_name, last_name, phone_number, password, CURRENT_DATE, CURRENT_TIME)
    return insert_values, user_email
    
    
# This function is responsible to store user's registration details  
def insert_registration_details(registration_json_data):
    try:
        # Getting filterd resgistraion details to insert in database
        insert_values, user_email = registration_data_filter(registration_json_data)
        cursor = DB_CONNECTION.cursor()
        # Creating a table if not exist in database
        if not is_table_exist(REGISTRAION_TABLE_NAME): 
            LOGGER.info("Table doesn't exist in database")
            try:
                LOGGER.info(f"Creating a table named {REGISTRAION_TABLE_NAME} in database")
                cursor.execute(registration_create_query())
                LOGGER.info(f"A table named {REGISTRAION_TABLE_NAME} has been created in database")
            except Exception as e:
                    LOGGER.error(f"An error occurred while creating table: {e}")  
        else:
            LOGGER.info("Table already exist in database")
        LOGGER.info("Inserting registration details in database")
        cursor.execute(registration_insert_query(), insert_values)
        DB_CONNECTION.commit()
        cursor.close()
        return True, user_email
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE DATA INSERTION IN {REGISTRAION_TABLE_NAME} :" f"{error}")
        
        
# This fucntion is responsible to insert OTP details in Database
def insert_otp_details(user_email, OTP):
    cursor = DB_CONNECTION.cursor()
    # Creating a table if not exist in database
    if not is_table_exist(OTP_TABLE_NAME): 
        LOGGER.info("Table doesn't exist in database")
        try:
            LOGGER.info(f"Creating a table named {OTP_TABLE_NAME} in database")
            cursor.execute(otp_verification_create_query())
            LOGGER.info(f"A table named {OTP_TABLE_NAME} has been created in database")
        except Exception as error:
                LOGGER.error(f"An error occurred while creating table: {error}")
    insert_values = (user_email, str(OTP), True, CURRENT_DATE, CURRENT_TIME)  
    LOGGER.info("Inserting OTP details in database")
    cursor.execute(otp_insert_query(), insert_values)
    DB_CONNECTION.commit()
    cursor.close()
    return True, user_email     
    