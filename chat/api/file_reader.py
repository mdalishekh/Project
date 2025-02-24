import PyPDF2
import docx
from chat.api.ocr import ocr_image, ocr_pdf

class FileExtractor:
    """
    Base class for file extraction.
    Contains methods for extracting text from various file formats.
    """

    def extract_pdf_text(self, file_path: str) -> str:
        """Extracts text from a PDF file."""
        print("From PDF FILE \n\n")
        try:
            text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                if not text.strip(): #== "" or text.strip() == None:
                    return ocr_pdf(file_path)
            
            return text.strip()
        except:
            return ocr_pdf(file_path)

    def extract_docx_text(self, file_path: str) -> str:
        """Extracts text from a DOCX file using python-docx."""
        
        doc = docx.Document(file_path)
        return "".join([para.text for para in doc.paragraphs])

    def extract_txt_text(self, file_path: str) -> str:
        """Extracts text from a TXT file."""
        
        with open(file_path, "r", encoding="utf-8") as txt_file:
            return txt_file.read().strip()
        
    def extract_image_text(self, file_path: str)-> str:
        
        return ocr_image(file_path)
            

class TextExtractor(FileExtractor):
    """
    Derived class that handles file format checking and calls appropriate extraction methods.
    Inherits from FileExtractor.
    """

    def extract_text(self, file_path: str) -> str:
        """Reads text from various file formats (PDF, DOCX, TXT)."""
        if file_path.endswith(".pdf"):
            return self.extract_pdf_text(file_path)
        elif file_path.endswith(".docx"):
            return self.extract_docx_text(file_path)
        elif file_path.endswith(".txt"):
            return self.extract_txt_text(file_path)
        elif file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            return self.extract_image_text(file_path)
        else:
            return "Unsupported file format."
