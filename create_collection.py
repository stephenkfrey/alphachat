### Sqlite3 replacement for Chroma ### 
import os
import sys
#import pysqlite3
#sys.modules['sqlite3'] = pysqlite3

#sys.modules['sqlite3'].sqlite_version_info = (3,35,0)
### ###
# 
# import chromadb
import chromadb
from chromadb.utils import embedding_functions

# create client 
chroma_client = chromadb.PersistentClient(path="./chromadb")

# create embed function 
qa_embed_fun = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")

# create collection
collection = chroma_client.create_collection(
        name="AIML",
        metadata={"hnsw:space": "cosine"}, # l2 is the default
        embedding_function=qa_embed_fun
)
