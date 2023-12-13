# use dotenv to load environemnt 
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from config import COLLECTION_NAME, TEST_COLLECTION_NAME, DATABASE_LOCAL_PATH, DATABASE_REMOTE_URL

REMOTE_PORT = os.environ.get("REMOTE_PORT")

###############################################
####################################
## Local Sqlite3 replacement for Chroma (if running locally on Intel Mac) ##

if os.environ.get('CURRENT_HOST') == 'LOCAL':
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
    sys.modules['sqlite3'].sqlite_version_info = (3,35,0)
    print(sys.modules['sqlite3'])
####################################
import uuid
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
####################################

def setup_local_chroma_client(): 
    CHROMA_CLIENT = chromadb.PersistentClient(DATABASE_LOCAL_PATH, Settings(allow_reset="True"))
    print('chroma heartbeat: ', CHROMA_CLIENT.heartbeat()) # returns a nanosecond heartbeat
    print('chroma host: ', DATABASE_LOCAL_PATH)
    return CHROMA_CLIENT

def setup_remote_chroma_client():
    CHROMA_CLIENT = chromadb.HttpClient(host=DATABASE_REMOTE_URL, port=8000, settings=Settings(allow_reset=True))
    print('chroma heartbeat: ', CHROMA_CLIENT.heartbeat()) # returns a nanosecond heartbeat
    print('chroma host: ', DATABASE_REMOTE_URL)
    return CHROMA_CLIENT

###############################################

def get_chroma_client():
    if os.environ.get('CURRENT_ENVIRONMENT') == 'LOCAL':
        CHROMA_CLIENT = setup_local_chroma_client()
    elif os.environ.get('CURRENT_ENVIRONMENT') == 'REMOTE':
        CHROMA_CLIENT = setup_remote_chroma_client()
    else:
        raise ValueError("Invalid input. Please put in .env 'LOCAL' or 'REMOTE'.")
    return CHROMA_CLIENT

def get_embed_function(): 
    QA_EMBED_FUN = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")
    return QA_EMBED_FUN

CHROMA_CLIENT = get_chroma_client()
QA_EMBED_FUN = get_embed_function()