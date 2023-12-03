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



### Test results ### 

data = [
    {
        'prompts': 'What is the capital of France?',
        'responses': 'The capital of France is Paris.',
        'metadata': {'source': 'geography textbook'}
    },
    {
        'prompts': 'Who wrote Dune??',
        'responses': 'Dune was written by Frank Herbert.',
        'metadata': {'source': 'sci fi'}
    },
]

r = add_to_collection(
    collection = collection,
    data = data, 
    embed_func=qa_embed_fun
)

print ('add result: ', RecursionError)