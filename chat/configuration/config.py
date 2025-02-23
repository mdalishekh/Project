import logging
PINECONE_INDEX_NAME = "vectors"

# Setting Up Logger instead of print()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")