# 1️ Use an official Python image as the base
FROM python:3.11

# 2️ Set the working directory inside the container
WORKDIR /app

# 3️ Install system dependencies (Tesseract OCR & Poppler for pdf2image)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \  
    && rm -rf /var/lib/apt/lists/*

# 4️ Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️ Copy the Django project files
COPY . .

# 6️ Expose port 8000 for Django
EXPOSE 8000

# 7️ Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
