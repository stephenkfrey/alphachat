import requests
from src.scripts.db_query_data import query_db

from src.scripts.config import COLLECTION_NAME, TEST_COLLECTION_NAME, DATABASE_LOCAL_PATH, DATABASE_REMOTE_URL
CONNECTION_URL = DATABASE_REMOTE_URL
CONNECTION_PORT = 8000
NUM_RETRIEVAL_RESULTS=3

####### ####### 

result = query_db ( "speech decode")
print('\n\n\n------------\n direct query_db result - \n',result) 

####### ####### 
selected_db = "AIML"
def get_retrievals_from_server(prompt): 
    selected_db_name = selected_db.replace('\n', '').replace(' ', '')

    try:
        response = requests.post(f"http://{CONNECTION_URL}:{CONNECTION_PORT}/query", 
                                 json={'prompt': prompt, 
                                       'collection_name': selected_db_name,
                                       "num_results":NUM_RETRIEVAL_RESULTS}
                                       )
        if response.status_code == 200:
            print ('response ' , response)
            result = response.json()
            return result
        else:
            # Handle non-200 status code
            print ('response: ', response)
            return None
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None

print ("\n\n\n------------ \n get retrievals from server \n", get_retrievals_from_server("speech decode"))