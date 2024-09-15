# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Configuration.config import *
from Database.DatabaseHandler import insert_registarion_details
import json


# Initiating an instance for FastAPI 
app = FastAPI()

# Creating a route for testing our REST API with GET method
@app.get('/test-api')
def test_api():
    return JSONResponse({"response": "Server is active"})


#  Creating a route for storing user's data in database 
@app.post('/insert')
async def get_registraion_details(request:Request):
    try:
        LOGGER.info("---------------------------------------------------------")
        LOGGER.info("REGISTRATION DETAILS INSERTION HAS BEEN INITIATED")
        json_data = await request.json()
        status, user_email = insert_registarion_details(json_data)
        if status:
            LOGGER.info("REGISTRATION DETAILS INSERTION HAS BEEN COMPLETED")
            response = {
                "status": status,
                "response" : f"User {user_email} has been registered."
            }
            return JSONResponse(response)
    except Exception as error:    
        return JSONResponse({"error occured while storing data" : error}, status_code= 500)