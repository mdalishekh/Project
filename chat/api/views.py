# Rest APIs for uploading files and question answering
import os
import uuid
import time
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework import status
from django.core.files.uploadedfile import UploadedFile
from chat.api.file_reader import TextExtractor
from chat.api.vector_store import VectorStore
from chat.api.vector_search import GetAnswer
from chat.configuration.config import logging
  
    
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  
def upload_file(request: Request):
    start_time = time.time()
    logging.info("Started API")
    file: UploadedFile = request.FILES.get('file')  
    # If no file sent then returning an error message
    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # If there is no path then it will be created
    UPLOAD_DIR = os.path.join(settings.BASE_DIR, "uploads")  
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    # Creating folder path to store files
    file_path = os.path.join(UPLOAD_DIR, file.name)  
    # Saving file in slected destination
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    text_extractor = TextExtractor()
    text_data = text_extractor.extract_text(file_path)
    # Generating source 
    source_id = str(uuid.uuid4())
    logging.info(source_id)
    vectors = VectorStore()
    vectors.pinecone_insertion(text_data, source_id)
    end_time = time.time()
    ex_time = end_time-start_time
    logging.info(f"Program took {ex_time} secs")
    return JsonResponse({
        "status" : True,
        "message" : "Vector store completed",
        "source" : source_id
    })
   
   
@api_view(["POST"])
def get_answer(request: Request):
    start_time = time.time()
    question: str = request.data.get('question')
    source: str = request.data.get('source')  
    logging.info(f"User Question : {question}")
    gen_answer = GetAnswer()
    answer = gen_answer.generate_answer(question, source)
    logging.info(f"Answer :  {answer}")
    end_time = time.time()
    ex_time = end_time-start_time
    logging.info(f"Program took {ex_time} secs")
    return JsonResponse({
        "status": True,
        "answer" : answer
    })