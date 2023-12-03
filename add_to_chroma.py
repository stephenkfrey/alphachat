### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
### ###
import uuid

import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="chromadb")

## Connect to saved chroma db 
print('chroma heartbeat: ', chroma_client.heartbeat()) # returns a nanosecond heartbeat. Useful for making sure the client remains connected.

## Import embed function 
qa_embed_fun = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")

## Set up Collection 
collection = chroma_client.get_collection(name="imagecoll", embedding_function=qa_embed_fun)

############ Main Add function ############
def add_to_collection(collection, data, embed_func):
    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for item in data:
        documents.append(item['prompts'])
        embeddings.append(embed_func([item['responses']])[0])
        metadatas.append(item['metadata'])
        ids.append(str(uuid.uuid4()))

    print (documents, embeddings, metadatas, ids) 

    result = collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    return result 

