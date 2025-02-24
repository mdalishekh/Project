import os
import openai
import threading
import queue
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationBufferMemory  
from langchain.chains import ConversationalRetrievalChain  
from chat.configuration.config import *
from dotenv import load_dotenv

# Loading essential environment varriables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
os.getenv("PINECONE_API_KEY")
  
# Getting Answer from file data also performing Similarity search
class GetAnswer:
    """
    This class only gets answers from inside file data.
    
    `functions`
    >>> retrieve_vector_data(source_id (str), question (str))
    >>> get_answer(source_id (str), question (str))
    
    """
    def __init__(self):
        # Add chat memory initialization
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Performing Similarity search
    def retrieve_vector_data(self, source_id: str, result_queue: object) -> list:
        """
        **List of Documents most similar to the query and score for each**.
        
        Args
        -----
            (str) : source_id  To filter data from Pinecone.
            
        Returns
        -------
            [list] : vector data
        """
        logging.info(f"Similarity search has been initiated")
        pc = Pinecone(os.getenv("PINECONE_API_KEY"))
        index = pc.Index(PINECONE_INDEX_NAME)
        vectorstore = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())
        # Retrieving with similarity search
        retrievers = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "filter": {"source": f"{source_id}"}  
            }
        ) 
        result_queue.put(retrievers)
        return retrievers

    # Getting Answer from vector store
    def generate_answer(self, query: str, source_id: str,) -> str:
        """
        **Gets user question along with Node Id and returns answer**.
    
        Args
        ----
            (str) : `query ` To get answer from Pinecone.
            (str) : `source_id ` To filter data from Pinecone.
        
        Returns
        -------
            (str) : An AI generated answer for user question.
        """
        try:    
            llm = ChatOpenAI(  
                openai_api_key=os.getenv("OPENAI_API_KEY"),  
                model_name='gpt-3.5-turbo', 
                temperature=0.0  
            )  
            # Making a queue to get value from threading function
            result_queue = queue.Queue()
            add_thread = threading.Thread(target=self.retrieve_vector_data, 
                                          args=(source_id, result_queue))
            # Staring Thread
            add_thread.start()
            # Getting returned value 
            retrievers = result_queue.get()

            #Use conversational retrieval chain with memory
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retrievers,
                memory=self.memory
            )
            # Generate the answer with chat memory
            response = chain({"question": query, "chat_history": self.memory.chat_memory})
            answer = response.get("answer", "No answer found.")

            # Log and return the answer
            # logging.info(f"Answer: {answer}")
            return answer
        except Exception as e:
            message = f"An error occurred while getting answer: {e}"
            logging.error(message)
            return message        