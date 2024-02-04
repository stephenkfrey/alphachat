import os
from dotenv import load_dotenv
load_dotenv()

## Database setup 
COLLECTION_NAME = "AIML"
TEST_COLLECTION_NAME = "TEST"

## Database paths 

DATABASE_LOCAL_PATH = "./chromadb" 

DATABASE_REMOTE_URL = os.environ.get("DATABASE_REMOTE_URL")

LOCAL_CONNECTION_PORT = 5000
REMOTE_CONNECTION_PORT = 8000

NUM_RETRIEVAL_RESULTS=5


