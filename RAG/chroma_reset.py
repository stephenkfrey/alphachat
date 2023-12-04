####################################
## Sqlite3 replacement for Chroma ##
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
sys.modules['sqlite3'].sqlite_version_info = (3,35,0)
print(sys.modules['sqlite3'])
####################################
import uuid
import chromadb
from chromadb.utils import embedding_functions
####################################
#get client
chroma_client = chromadb.PersistentClient(path="../chromadb")
#import embed function
qa_embed_fun = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")
## Set up Collection 
collection = chroma_client.get_collection(name="AIML", embedding_function=qa_embed_fun)


####################################
##### Main RESET ###############
chroma_client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.


