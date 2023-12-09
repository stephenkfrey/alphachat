from init_chroma_client import CHROMA_CLIENT, QA_EMBED_FUN 

############ Query document ############
def query_db(query_text, collection_name="AIML", num_results=2): 
    print("query text ",query_text)

    collection = CHROMA_CLIENT.get_collection(name=collection_name, embedding_function=QA_EMBED_FUN) # this took 0.0010 seconds 

    results = collection.query(
        query_texts=[query_text],
        n_results=num_results
    )
    return results 
