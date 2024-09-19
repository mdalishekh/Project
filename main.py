# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Configuration.config import *
from Database.DatabaseHandler import *
from Database.LoginAndOtpVerifier import otp_validator, authenticate_user
from Emails.MailSender import *
from Cron.cron import cron_scheduler
import random

# Initiating an instance for FastAPI 
app = FastAPI()

# Define the origins you want to allow
origins = [
    "http://127.0.0.1:5500",  # Your frontend URL
    "http://localhost:5500",
    "https://gocab.netlify.app",
    "https://gocab.netlify.app/",
    # You can add more origins here if needed
]

# Add the CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins allowed to make requests
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Creating a route for keeping server active
@app.get('/')
def cron_expression():
    cron_scheduler()
    return JSONResponse({"response": "Our Application / Server is active"})

# Creating a route for testing our REST API with GET method
@app.get('/test-api')
def test_api():
    LOGGER.info("Our Application / Server is active")
    return JSONResponse({"response": "Our Application / Server is active"})
   
# 1.Creating a route for sending OTP to users via e-mail
@app.post('/send-otp')
async def send_otp_api(request:Request):
    try:
        LOGGER.info("---------------------------------------------------------")
        LOGGER.info("OTP SENDING HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data['userEmail']
        user_first_name = json_data['firstName']
        OTP = random.randint(100000, 999999)
        # Inserting OTP details in Database
        insert_otp_details(user_email, OTP)
        # Sending OTP to user email
        status = send_otp_by_mail(user_email, user_first_name, OTP)
        LOGGER.info(f"Generated OTP for {user_email} is : {OTP}")
        # If OTP is successfully sent to user email
        if status:
            LOGGER.info(f"OTP HAS BEEN SENT TO {user_email}")
            response = {"status": status,"response" : f"OTP has been sent to {user_email}"}
            return  JSONResponse(response)
        return JSONResponse({"status" : status, "error" : f"Sending OTP to {user_email} has been failed"}, status_code=500)
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE SENDING OTP TO {user_email}")
        return JSONResponse({"error occured while sending otp" : error}, status_code= 500)
    
    
# 2. Creating route for sending registration success to users via e-mail     
@app.post('/otp-verification')
async def otp_verification_api(request:Request):
    try:
        LOGGER.info("---------------------------------------------------------")
        LOGGER.info("OTP VERIFICATION HAS BEEN INITIATED")
        # Getting JSON data  
        json_data = await request.json()
        user_email = json_data['userEmail']
        user_first_name = json_data['firstName']
        OTP = int(json_data['OTP'])        
        # validating OTP if it's correct or not
        is_otp_valid , message = otp_validator(user_email, OTP)
        if is_otp_valid:
            # If OTP verification is success
            LOGGER.info("User has been verified")
            status = registration_success_mail(user_email, user_first_name)
        else:
            LOGGER.info("OTP validation has failed")
            return JSONResponse({"status" : False, "error" : f"OTP entered by {user_email} {message}"})
        # If OTP is correct and confirmation email sent to user
        if status:
            LOGGER.info(f"CONFIRMATION E-MAIL HAS BEEN SENT TO THE {user_email}")
            response = {"status": status,"response" : f"User has been verified confirmation e-mail has been sent to {user_email}"}
            return  JSONResponse(response)
        # If OTP is correct but confirmation e-mail not sent to user
        return JSONResponse({"status" : status, "error" : f"Sending e-mail to {user_email} has been failed"}, status_code=500)
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE SENDING CONFIRMATION E-MAIL : {user_email}")
        return JSONResponse({"error occured while sending confirmation e-mail" : error}, status_code= 500)
        
        
# 3. Creating a route for storing user's registration data in database 
@app.post('/insert')
async def get_registraion_details_api(request:Request):
    try:
        LOGGER.info("---------------------------------------------------------")
        LOGGER.info("REGISTRATION DETAILS INSERTION HAS BEEN INITIATED")
        json_data = await request.json()
        status, user_email = insert_registration_details(json_data)
        if status:
            LOGGER.info("REGISTRATION DETAILS INSERTION HAS BEEN COMPLETED")
            response = {"status" : status, "response" : f"User {user_email} has been registered."}
            return JSONResponse(response)
        return JSONResponse({"status" : status, "error" : f"Storing data for user {user_email} has been failed"}, status_code=500)
    except Exception as error:    
        LOGGER.error(f"ERROR OCCURED WHILE STORING DATA : {error}")
        return JSONResponse({"error occured while storing data" : error}, status_code= 500)        
    
# 4. Creating a route for User Login
@app.post('/authenticate')
async def get_login_details_api(request:Request):
    try:
        LOGGER.info("---------------------------------------------------------")
        LOGGER.info("USER AUTHENTICATION HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data['userEmail']
        password = json_data['password']
        status, message = authenticate_user(user_email, password)
        if status:
            LOGGER.info("USER AUTHENTICATION HAS BEEN COMPLETED")
            response = {"status" : status, "user" : user_email, "response" : message}
            return JSONResponse(response)
        return JSONResponse({"status" : status, "user" : user_email, "error" : message}, status_code= 500)
    except Exception as error:    
        LOGGER.error(f"ERROR OCCURED WHILE AUTHENTICATING USER : {error}")
        return JSONResponse({"error occured while authenticating user" : error}, status_code= 500)   