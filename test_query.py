### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
### ###
import uuid
import chromadb
from chromadb.utils import embedding_functions
from add_query import query_db
####### ####### 

result = query_db ( "speech decode")
print('result - ',result) 