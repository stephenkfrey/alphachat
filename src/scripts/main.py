# main.py
import os
import config
import chromadb 
from services import *

if os.environ.get("PRODUCTION"):
   client = chromadb.HTTPClient(config.DATABASE_URL)
else:  
   client = chromadb.PersistentClient(config.DATABASE_PATH)

