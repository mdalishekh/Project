# This module is specially made for performing database related tasks
# Importing some useful Packages to be used in database related tasks

from Configuration.config import *
from Configuration.sqlQuery import *

# Filtering registraion details to be stored in database
def registration_data_filter(registration_json_data):
    # Getting resgistraion details key values
    json_data = registration_json_data.get('registrationDetails')
    user_email = json_data.get('userEmail')
    first_name = json_data.get('firstName')
    last_name = json_data.get('lastName')
    phone_number = json_data.get('phoneNumber')
    password = json_data.get('password')
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
            logging.info("Table doesn't exist in database")
            try:
                logging.info(f"Creating a table named {REGISTRAION_TABLE_NAME} in database")
                cursor.execute(registration_create_query())
                logging.info(f"A table named {REGISTRAION_TABLE_NAME} has been created in database")
            except Exception as e:
                    logging.error(f"An error occurred while creating table: {e}")  
        else:
            logging.info("Table already exist in database")
        logging.info("Inserting registration details in database")
        cursor.execute(registration_insert_query(), insert_values)
        DB_CONNECTION.commit()
        cursor.close()
        return True, user_email
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE DATA INSERTION IN {REGISTRAION_TABLE_NAME} :" f"{error}")
        
               
# This fucntion is responsible to insert OTP details in Database
def insert_otp_details(user_email, OTP):
    cursor = DB_CONNECTION.cursor()
    # Creating a table if not exist in database
    if not is_table_exist(OTP_TABLE_NAME): 
        logging.info("Table doesn't exist in database")
        try:
            logging.info(f"Creating a table named {OTP_TABLE_NAME} in database")
            cursor.execute(otp_verification_create_query())
            logging.info(f"A table named {OTP_TABLE_NAME} has been created in database")
        except Exception as error:
                logging.error(f"An error occurred while creating table: {error}")
                
    logging.info(f"Checking if {user_email} already exist or not in OTP Table")           
    # cursor.execute(is_user_exist(user_email, OTP_TABLE_NAME), (user_email,))
    exists = is_user_exist(user_email, OTP_TABLE_NAME) 
    # If user has already generated an OTP before
    if exists:
        logging.info(f"{user_email} already exist in OTP table")
        # If OTP is invalid / expired 
        if is_table_exist(REGISTRAION_TABLE_NAME):
            logging.info(f"{REGISTRAION_TABLE_NAME} already exist in database")
            # If user is not registered then proceeding to send new OTP 
            if not is_user_exist(user_email, REGISTRAION_TABLE_NAME) :
                logging.info(f"{user_email} is not registered")
                cursor.execute(update_otp_query(), (str(OTP), CURRENT_DATE, CURRENT_TIME, user_email)) 
                logging.info(f"OTP for {user_email} has been updated")    
                DB_CONNECTION.commit()
                cursor.close()
                return True, f"New OTP has been sent" 
            return False, f"User already exist"
        else:
            # If email exist in OTP table but not registered then update OTP table with new OTP
            logging.info("Registration table doesn't exist in database so user is not registered yet.")
            cursor.execute(update_otp_query(), (str(OTP), CURRENT_DATE, CURRENT_TIME, user_email))  
            DB_CONNECTION.commit()
            cursor.close()  
            return True, "New OTP has been sent"    
    else:
        # If OTP is not generated by the user nor the user is registered
        insert_values = (user_email, str(OTP), True, CURRENT_DATE, CURRENT_TIME, False)  
        logging.info("Inserting OTP details in database")
        cursor.execute(otp_insert_query(), insert_values)
        DB_CONNECTION.commit()
        cursor.close()
        return True, "OTP has been sent"      
    
    
# This function is responsible for storing forgot password OTP in Database
def insert_forgot_otp(user_email, OTP):
    try:
        cursor = DB_CONNECTION.cursor()
        try :
            cursor.execute(update_otp_query(), (str(OTP), CURRENT_DATE, CURRENT_TIME, user_email))
        except:
            insert_values = (user_email, str(OTP), True, CURRENT_DATE, CURRENT_TIME)
            cursor.execute(otp_insert_query(), insert_values)
        DB_CONNECTION.commit()
        cursor.close()  
        return True, "OTP has been sent"
    except Exception as error:
        logging.error("Error occurred while storing in to database :", error)
        return False, "Error occurred"
    
    
# This function is responsible for assigning eligiblilty to user if they verified OTP
# Also if user changed thier password , this function will assign ineligibilty to user
def password_change_eligibility(user_email, is_eligible):
    cursor = DB_CONNECTION.cursor()
    user_exist = is_user_exist(user_email, OTP_TABLE_NAME)
    if user_exist:
        cursor.execute(can_change_allow_query(), (CURRENT_DATE, CURRENT_TIME, is_eligible, user_email))  
        DB_CONNECTION.commit()
        cursor.close()
        return True
    return False


# This function is responsible for update user password if they are eligible 
def update_password(user_email:str, new_password:str):
    cursor = DB_CONNECTION.cursor()
    user_exist = is_user_exist(user_email, REGISTRAION_TABLE_NAME)
    if user_exist:
        cursor.execute(update_password_query(), (new_password, CURRENT_DATE, CURRENT_TIME, user_email))  
        DB_CONNECTION.commit()
        cursor.close()       
        return True, "Password chnaged successfully"
    return False, "Can't change password"   