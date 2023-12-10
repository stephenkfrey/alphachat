from init_chroma_client import CHROMA_CLIENT, QA_EMBED_FUN 

############ Query document ############
def query_db(query_text, collection_name="AIML", num_results=2): 
    print("query text ",query_text)

    try: 
        collection = CHROMA_CLIENT.get_collection(name=collection_name, embedding_function=QA_EMBED_FUN) # this took 0.0010 seconds, but perhaps longer when remote, and could be improved. 

        results = collection.query(
            query_texts=[query_text],
            n_results=num_results
        )
        return results 
    except Exception as e: 
        print (f"error querying collection. \n with {collection_name}, {query_text} \n", e)
        return None
