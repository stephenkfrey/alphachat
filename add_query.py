### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
sys.modules['sqlite3'].sqlite_version_info = (3,35,0)
print(sys.modules['sqlite3'])

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

############ Add ############
def add_list_of_dicts_to_collection(data, collection=collection, embed_func=qa_embed_fun):
    documents = []
    embeddings = []
    metadatas = []
    ids = []
    print('\n\n### add list of dicts to collection -- data', data)

    for item in data: # data is a list of dicts 
        documents.append(item['prompt']) 
        # embeddings.append(embed_func([item['prompt']])[0]) 
        metadatas.append(item['metadata']) 
        ids.append(str(uuid.uuid4())) 
    
    print ("documents",documents)
    print("metadatas",metadatas)
    print("ids",ids)

    result = collection.add(
        documents=documents,
        # embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    return result 

############ Add ############
def query_db(query_text): 
    print("query text ",query_text)

    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )
    return results 
