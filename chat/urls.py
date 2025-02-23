from django.urls import path, include

urlpatterns = [
    path('api/', include('chat.api.urls')),  # Include API routes
]
