import uuid 

from init_chroma_client import CHROMA_CLIENT, QA_EMBED_FUN 
from config import COLLECTION_NAME, TEST_COLLECTION_NAME, DATABASE_LOCAL_PATH, DATABASE_REMOTE_URL

from src.utils.extract_images import extract_image_caption_sets_from_url

############ Helpers ############
def add_data_to_collection(chroma_client, collection_name, documents, metadatas, ids,  embed_func): 
    collection = chroma_client.get_collection(name=collection_name, embedding_function=embed_func)
    result = collection.add(
        documents=documents,
        # embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    return result

############ Add to db ############
### Format data from URL list 
def make_data_dict_list_from_url_list(url_list):
    data_list = []

    for url in url_list:
        list_of_image_dicts = extract_image_caption_sets_from_url(url)
        for single_image_dict in list_of_image_dicts:
            data = {
                "prompt": single_image_dict['caption'],
                "metadata": {
                    "page_url": url,
                    "image_url": single_image_dict['image_url'],
                    "page_title": single_image_dict['page_title']
                }
            }
            data_list.append(data)
    return data_list

### Add Formatted data list to a collection 
def add_list_of_dicts_to_collection(
        data_dict_list, 
        collection_name="AIML"):

    documents = []
    embeddings = []
    metadatas = []
    ids = []
    print('\n\n### add list of dicts to collection -- data', data_dict_list)

    for item in data_dict_list: # data is a list of dicts 
        documents.append(item['prompt']) 
        # embeddings.append(embed_func([item['prompt']])[0]) 
        metadatas.append(item['metadata']) 
        ids.append(str(uuid.uuid4())) 
    
    print ("documents",documents)
    print("metadatas",metadatas)
    print("ids",ids)

    upsert_result = add_data_to_collection(
        chroma_client=CHROMA_CLIENT, 
        collection_name=collection_name, 
        documents=documents, 
        metadatas=metadatas, 
        ids=ids, 
        embed_func=QA_EMBED_FUN
    )
    return upsert_result 

### Full pipe from URL list to upsert to collection
def add_url_list_to_collection(url_list):
    url_data_list = make_data_dict_list_from_url_list(url_list)
    upsert_result = add_list_of_dicts_to_collection(url_data_list)
    return upsert_result 