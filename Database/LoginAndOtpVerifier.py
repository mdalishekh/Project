# This module is specially made for verify OTP and verify if the user is Logged in or not
from Configuration.config import *

# This function is responsible for validate OTP from database
def otp_validator(user_email, OTP):
    cursor = DB_CONNECTION.cursor()
    cursor.execute(FETCH_OTP, (user_email,))
    result = cursor.fetchone()
    fetched_otp, is_valid = result
    cursor.close()
    if is_valid:
        if OTP == int(fetched_otp):
            LOGGER.info("OTP has been verified")
            return True, "has been verified"
        LOGGER.info("OTP is incorrect")
        return False, "is incorrect"
    LOGGER.info("OTP is invalid or expired")
    return False, "is invalid or expired"


# This function is responsible to authenticate users
def authenticate_user(user_email, user_password):
    cursor = DB_CONNECTION.cursor()
    # Checking if email entered by user is valid or not
    LOGGER.info(f"Checking if {user_email} exist or not")
    exist_query = f"""
            SELECT EXISTS (
            SELECT 1 
            FROM {REGISTRAION_TABLE_NAME}
            WHERE user_email = %s
            );
             """
    cursor.execute(exist_query, (user_email,))
    # If email entered by user exists now authenticate
    exists = cursor.fetchone()[0]     
    if exists:
        LOGGER.info(f"A user with email {user_email} exists")
        password_query = f"SELECT user_password FROM {REGISTRAION_TABLE_NAME} WHERE user_email = %s"
        cursor.execute(password_query, (user_email,))
        fetched_password = cursor.fetchone()[0]
        cursor.close()
        if fetched_password == user_password:
            message = f"Login successfully"
            LOGGER.info(f"User {user_email} has been authenticated")
            return True, message
        message = "Incorrect password"
        LOGGER.error(message)    
        return False, message
    message = f"No users found with this email {user_email}"
    LOGGER.error(message)
    return False, message


# This function is responsible for De-validate OTP in Database 
def otp_devalidator(user_email):
    try:
        # Trying to connect with Database 
        cursor  = DB_CONNECTION.cursor()
        query = f'''
                UPDATE {OTP_TABLE_NAME}
                SET is_valid = false
                WHERE user_email = %s;
                '''
        cursor.execute(query, (user_email,))
        DB_CONNECTION.commit()
        cursor.close()         
        LOGGER.info("OTP HAS BEEN DE-VALIDATED or EXPIRED")
        return True
    except Exception as error:
        LOGGER.error(f"ERROR OCCURRED WHILE DE-VALIDATING OTP : {error}")
        return False
    
    
    
    """
    UPDATE otp_verification
SET is_valid = false, otp_code = '123456'
WHERE user_email = 'mdalishekh2003@gmail.com';

    """