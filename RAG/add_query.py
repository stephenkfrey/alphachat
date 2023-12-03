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

chroma_client = chromadb.PersistentClient(path="./chromadb")

## Connect to saved chroma db 
print('chroma heartbeat: ', chroma_client.heartbeat()) # returns a nanosecond heartbeat. Useful for making sure the client remains connected.

## Import embed function 
qa_embed_fun = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")

## Set up Collection 


############ Add to db ############
def add_list_of_dicts_to_collection(data, embed_func=qa_embed_fun, collection_name="AIML"):
    documents = []
    embeddings = []
    metadatas = []
    ids = []
    print('\n\n### add list of dicts to collection -- data', data)

    collection = chroma_client.get_collection(name=collection_name, embedding_function=qa_embed_fun)

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

############ Query document ############
def query_db(query_text, collection_name="AIML", num_results=2): 
    print("query text ",query_text)

    collection = chroma_client.get_collection(name=collection_name, embedding_function=qa_embed_fun) # this took 0.0010 seconds 

    results = collection.query(
        query_texts=[query_text],
        n_results=num_results
    )
    return results 
