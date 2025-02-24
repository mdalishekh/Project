# This files handles pinecone insertion 
import os
import openai
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from chat.configuration.config import *
from dotenv import load_dotenv

# Loading essential environment varriables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
os.getenv("PINECONE_API_KEY")
# openai.api_key = OPENAI_API_KEY

class VectorStore:
    """_summary_
    """
    def pinecone_insertion(self, text: str, source_id: str)-> None:
        """_summary_

        Args:
            text (str): _description_
            source_id (str): _description_
        """
        format_text = [Document(metadata={'source': source_id}, page_content=text)]
        logging.info("Spliiting text")
        # Optimize chunk size for better performance
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, 
                                                       chunk_overlap=100, 
                                                       length_function=len)
        
        docs = text_splitter.split_documents(format_text)
        logging.info("Text splitted")
        logging.info("Vector storing")
        # pc  = Pinecone(PINECONE_API_KEY)
        vectors = PineconeVectorStore.from_documents(docs, 
                        index_name= PINECONE_INDEX_NAME, 
                        embedding= OpenAIEmbeddings())
        logging.info("Vector data stored")
        