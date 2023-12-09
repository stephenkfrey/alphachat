import requests
from db_query_data import query_db

####### ####### 

result = query_db ( "speech decode")
print('\n\n\n------------\n direct query_db result - \n',result) 

####### ####### 
selected_db = "AIML"
def get_retrievals_from_server(prompt): 
    selected_db_name = selected_db.replace('\n', '').replace(' ', '')
    response = requests.post('http://localhost:5000/query', 
                             json={'prompt': prompt, 
                                   'collection_name': selected_db_name,
                                   "num_results":3}
                                   )
    print('\n\n\n------------\nretreivals from server response: \n', response)
    result = response.json()
    return result 

print ("\n\n\n------------\n", get_retrievals_from_server("speech decode"))