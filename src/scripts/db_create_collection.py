from init_chroma_client import CHROMA_CLIENT, QA_EMBED_FUN, Settings, chromadb
from config import COLLECTION_NAME, TEST_COLLECTION_NAME, DATABASE_LOCAL_PATH, DATABASE_REMOTE_URL
####################################
### HELPERS 

def create_collection(client, collection_name): 
    collection = CHROMA_CLIENT.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}, # l2 is the default
        embedding_function=QA_EMBED_FUN, 
        
    )
    print ("client heartbeat: " , client.heartbeat())
    return collection

def reset_client(client): 
    r = client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.
    return r

####################################
#### GET LOCAL OR REMOTE SETUP ####
# USER_DEFINED_ENV = input("chroma collections LOCAL or REMOTE? ")
# if USER_DEFINED_ENV.upper() not in ["LOCAL", "REMOTE"]:
#     raise ValueError("Invalid input. Please enter 'LOCAL' or 'REMOTE'.")

# if USER_DEFINED_ENV == "LOCAL": 
#    chroma_client = chromadb.PersistentClient(DATABASE_LOCAL_PATH, Settings(allow_reset="True"))
   
# elif USER_DEFINED_ENV == "REMOTE":
#    chroma_client = chromadb.HTTPClient(host=DATABASE_REMOTE_URL, port=8000, settings=Settings(allow_reset=True))
# else: 
#     raise ValueError("Invalid input. Please enter 'LOCAL' or 'REMOTE'.")

####################################
#### CREATE / RESET  ####
DB_ACTION = input("Enter CREATE or RESET. Optionally add a NAME if CREATING collections.  ")
action, *name_parts = DB_ACTION.split()
if action == "CREATE":
    if not name_parts:
        print(create_collection(CHROMA_CLIENT, COLLECTION_NAME))
        print(create_collection(CHROMA_CLIENT, TEST_COLLECTION_NAME))
        pass
    else:
        print(create_collection(CHROMA_CLIENT, name_parts[0]))
elif action == "RESET":
    print(reset_client(CHROMA_CLIENT))
