### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
### ###

import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="chromadb")


results = collection.query(
    query_texts=["where are we in history?"],
    n_results=2
)

print ('results:\n', results) 