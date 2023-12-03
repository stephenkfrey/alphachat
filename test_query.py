### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
### ###
import uuid

import chromadb
from chromadb.utils import embedding_functions

from add_query import query_db

# chroma_client = chromadb.PersistentClient(path="chromadb")

## Connect to saved chroma db 
# print('chroma heartbeat: ', chroma_client.heartbeat()) # returns a nanosecond heartbeat. Useful for making sure the client remains connected.

# ## Import embed function 
# qa_embed_fun = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")

# ## Set up Collection 
# collection = chroma_client.get_collection(name="imagecoll", embedding_function=qa_embed_fun)

result = query_db ( "speech decode")
print('result - ',result) 