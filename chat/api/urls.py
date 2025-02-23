from django.urls import path
from .views import upload_file, get_answer

# Api urls
urlpatterns = [
    path('upload/', upload_file, name='upload-file'),  
    path('get-answer/', get_answer, name='get-answer')
]
