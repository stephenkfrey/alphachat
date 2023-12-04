### Sqlite3 replacement for Chroma ### 
import os
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
### ###

from add_query import query_db
####### ####### 

result = query_db ( "generative video model")
print('result - ',result) 