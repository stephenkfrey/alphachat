import os 
import streamlit as st
import requests
import json
#from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv()

import sys
import os
# sys.path.append(os.path.abspath('../src'))  # Assuming 'src' is located in a sibling directory of the current file's parent directory

from app.openai_functions import create_chat_completion, create_streaming_chat_completion

# print(os.getcwd()) # /Users/stephen/Dev/alphac
# sys.path.append(os.path.abspath('..'))

sys.path.append(os.path.abspath('../'))
# print('syspath---\n',sys.path)

from src.scripts.db_query_data import query_db

############ Env and remote url  ############
ENVIRONMENT = os.environ.get('CURRENT_ENVIRONMENT')

if ENVIRONMENT == 'LOCAL':
    CONNECTION_URL = "localhost"
    CONNECTION_PORT = 5000
elif ENVIRONMENT == 'REMOTE':
    CONNECTION_URL = DATABASE_REMOTE_URL = os.environ.get("DATABASE_REMOTE_URL")
    CONNECTION_PORT = 8000

### Vars #### 

RETRIEVAL_RELEVANCE_THRESHOLD=0.3
NUM_RETRIEVAL_RESULTS = 3

############ Streamlit Setup ############
# layout widemode
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.title("✨ AlphaChat ✨")
st.markdown("<h1 style='text-align: center;'>✨ AlphaChat ✨</h1>", unsafe_allow_html=True)

############ Streamlit font customization ############
# to use with bionic font eventually 
# https://alive-son-632.notion.site/Bionic-Reading-API-v1-d91e2c4a69ee46ceaf750fd090f95046

# streamlit_style = """
# 			<style>
# 			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

# 			html, body, [class*="css"]  {
# 			font-family: 'Roboto', sans-serif;
# 			}
# 			</style>
# 			"""
# st.markdown(streamlit_style, unsafe_allow_html=True)


############ Select a collection ############
one,two,three,four,five=st.columns(5)
# Read the database names from db_names.txt
with open('app/db_names.txt', 'r') as file:
    db_names = file.readlines()

# Create a dropdown menu to display the database names
selected_db = one.selectbox("Select a database", db_names)

############ Body, Sidebar Columns ############
st.markdown("---")  # Horizontal line for separation
body, sidebar = st.columns(2)  # Create two columns
body.markdown("### Words")
sidebar.markdown("### Images")

############ Initialize chat message history ############

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an expert teacher and explainer. You are here to help people understand complex topics. Next to your prompt, the user is being shown a list of images and diagrams related to their question, so don't mention that you can't show images/diagrams. "},
        {"role": "assistant", "content": "👀 🔎 🌍. What do you want to understand more?"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
messages = [msg for msg in messages if msg["role"] != "system"]


for msg in messages:
    # st.chat_message(msg["role"]).write(msg["content"])
    body.chat_message(msg["role"]).write(msg["content"])

############ Helper fun ############

# def get_retrievals_from_server(prompt): 
#     selected_db_name = selected_db.replace('\n', '').replace(' ', '')

#     try:
#         response = requests.post(f"http://{CONNECTION_URL}:{CONNECTION_PORT}/query", 
#                                  json={'prompt': prompt, 
#                                        'collection_name': selected_db_name,
#                                        "num_results":NUM_RETRIEVAL_RESULTS}
#                                        )
#         if response.status_code == 200:
#             result = response.json()
#             return result
#         else:
#             # Handle non-200 status code
#             print ('response: ', response)
#             return None
#     except Exception as e:
#         # Handle other exceptions
#         print(f"Error: {e}")
#         return None

############ Main conversation and retrieval loop ############

if user_prompt := st.chat_input(placeholder="How do generative video models work?"):
    with st.spinner("👀"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        # st.chat_message("user").write(user_prompt)
        body.chat_message("user").write(user_prompt)

        ########### Get and filter retrievals/images ###########
        retrievals = query_db(user_prompt) 
        # print('\n-----retreivals-----\n',retrievals)

        # Filter out retrievals with distance greater than THRESHOLD 
        filtered_retrievals = [doc for doc, dist in zip(retrievals['documents'][0], retrievals['distances'][0]) if dist > RETRIEVAL_RELEVANCE_THRESHOLD]
        retrievals['documents'][0] = filtered_retrievals
        print('\n-----retreivals-----\n',retrievals)

        ##### Display retrieved images #### 
        # sidebar.write(retrievals) ## displays the raw text 
        for i in range(len(retrievals['documents'][0])):
            metadata = retrievals['metadatas'][0][i]
            if metadata is None:
                continue 
            
            # Display the image
            sidebar.image(metadata['image_url'])

            # Display the document
            sidebar.write(retrievals['documents'][0][i])

            # Display the page title as a clickable link
            page_title = metadata['page_title']
            page_url = metadata['page_url']
            sidebar.markdown(f"[{page_title}]({page_url})")
        
        ########### Get static LLM response ###########
        # response = create_chat_completion(messages=messages)
        # st.session_state["response"] = response

    ########### Display streaming LLM text response ###########
    with st.chat_message("assistant"):
        this_response_message = ""
        message_placeholder = body.empty()

    for response in create_streaming_chat_completion(messages=st.session_state.messages):
        print('response: ', response)
        this_response_message += (response.choices[0].delta.content or "")
        print('this_response_message: ', this_response_message)
        message_placeholder.markdown(this_response_message + " ")
        # message_placeholder.markdown(f"<p style='font-size:16px;'>{this_response_message}</p>", unsafe_allow_html=True)


    st.session_state.messages.append({"role": "assistant", "content": this_response_message})

    print ('message_placeholder: \n ', message_placeholder, '\n\nsession-state-messages: \n', st.session_state.messages, '\n\nresponse: \n', response)


####### Suggested Prompts ######
if st.session_state["response"]:
    buttons = st.empty()
    placeholder = st.empty()

    # # Create a section for buttons
    # st.markdown("---")  # Horizontal line for separation
    # col1, col2 = st.columns(2)  # Create two columns

    # # Add buttons to the columns
    # button_names = ["Button1Button1Button1", "Button2Button2Button2Button2Button2Button2", "Button3", "Button4Button4Button4Button4", "Button5", "Button6"]
    # for i in range(3):
    #     col1.button(button_names[i])
    #     col2.button(button_names[i+3])

    # st.markdown("---")  # Horizontal line for separation


