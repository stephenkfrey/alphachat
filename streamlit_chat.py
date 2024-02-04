import os 
import sys
import requests
import json
import streamlit as st
from streamlit_shortcuts import add_keyboard_shortcuts
import openai
from dotenv import load_dotenv
load_dotenv()

# sys.path.append(os.path.abspath('../src'))  # Assuming 'src' is located in a sibling directory of the current file's parent directory

from app.openai_functions import create_chat_completion, create_streaming_chat_completion
from src.scripts.config import NUM_RETRIEVAL_RESULTS 

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

MAX_IMAGE_HEIGHT = "350px"  # Set the maximum height you want
MAX_CAPTION_LENGTH = 600
RETRIEVAL_RELEVANCE_THRESHOLD = 0.3
NUM_SUGGESTED_QUESTIONS = 5
DEFAULT_PLACEHOLDER_PROMPT="How do generative video models work?"
PAGE_TITLE = "✨ AlphaChat ✨"

### Prompts ###

DEFAULT_SYSTEM_PROMPT="""You are an expert teacher and explainer. You are here to help people understand complex topics. Next to your prompt, the user is being shown a list of images and diagrams related to their question, so DO NOT mention that you can't show images/diagrams, DO NOT say you don't have access diagrams, we already know that. """

############ Streamlit Setup ############
# layout widemode
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.title("✨ AlphaChat ✨")
st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)

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
body, sidebar = st.columns([0.4,0.6])  # Create two colum
body.markdown("### Words")
sidebar.markdown("### Images")

############ Initialize chat message history ############

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
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


if user_prompt := st.chat_input(placeholder=DEFAULT_PLACEHOLDER_PROMPT):
    with st.spinner("👀"):
        
        ########### Get and filter retrievals/images ###########
        retrievals = query_db(user_prompt) 
        # print('\n-----retreivals-----\n',retrievals)

        # Filter out retrievals with distance greater than THRESHOLD 
        filtered_retrievals = [doc for doc, dist in zip(retrievals['documents'][0], retrievals['distances'][0]) if dist > RETRIEVAL_RELEVANCE_THRESHOLD]
        retrievals['documents'][0] = filtered_retrievals
        print('\n-----retreivals-----\n',retrievals)

        ### Append retrievals to prompt === 

        full_prompt_with_retrievals = "QUERY:\n" + user_prompt + ".\n\n. \nInstructions: You can refer to the following pieces of content, and see if any are relevant to the conversation, and if so the incporate them into a concise, accessible response to the user. \nCONTEXT:\n\n " + " ".join(filtered_retrievals) + " \n\n Further instructions: DO NOT mention that you can't show images/diagrams, DO NOT say you don't have access diagrams, we already know that."

        print('\n\n##### full_prompt_with_retrievals\n\n',full_prompt_with_retrievals)
        # Now you can refer to the following pieces of context to create a summarized reply to the user's query:

        st.session_state.messages.append({"role": "user", "content": user_prompt})
        body.chat_message("user").write(user_prompt)


        ##### Display retrieved images #### 
        # sidebar.write(retrievals) ## displays the raw text 
        # for i in range(len(retrievals['documents'][0])):
        #     metadata = retrievals['metadatas'][0][i]
        #     if metadata is None:
        #         continue 

        #     image_url = metadata['image_url']
        #     max_height = "300px"  # Set the maximum height you want

        #     # Display the image with a maximum height
        #     # sidebar.markdown(f"<img src='{image_url}' style='max-height: {max_height};'>", unsafe_allow_html=True)
        #     sidebar.markdown(f"<a href='{image_url}' target='_blank'><img src='{image_url}' style='max-height: {max_height};'></a>", unsafe_allow_html=True)

        #     # Display the document 
        #     sidebar.write(retrievals['documents'][0][i])
        #     # Display the document URL as a clickable link 
        #     page_title = metadata['page_title']
        #     page_url = metadata['page_url']
        #     sidebar.markdown(f"[{page_title}]({page_url})")

        # Modified code for displaying images in two columns
        image_columns = sidebar.columns(2)  # Create two columns for images
        for i, metadata in enumerate(retrievals['metadatas'][0]):
            if metadata is None:
                continue
            image_url = metadata['image_url']

            col_index = i % 2  # Determine which column to use (0 or 1)

            # Create a clickable image that expands to show a larger image
            with image_columns[col_index].expander("Click to view image", expanded=False):
                image_columns[col_index].markdown(f"<a href='{image_url}' target='_blank'><img src='{image_url}' style='max-height: {MAX_IMAGE_HEIGHT};'></a>", unsafe_allow_html=True)
                image_caption = retrievals['documents'][0][i][:MAX_CAPTION_LENGTH]
                image_columns[col_index].write(image_caption)

                # image_columns[col_index].image(image_url, caption=metadata['page_title'])

            # image_columns[col_index].markdown(f"<a href='{image_url}' target='_blank'><img src='{image_url}' style='max-height: {max_height};'></a>", unsafe_allow_html=True)

            # image_columns[col_index].write(retrievals['documents'][0][i])
            
            page_title = metadata['page_title']
            page_url = metadata['page_url']
            image_columns[col_index].markdown(f"[{page_title}]({page_url})")
            
            # # Display the image
            # sidebar.image(metadata['image_url'])

            # # Display the document
        
            # # Display the page title as a clickable link
            # page_title = metadata['page_title']
            # page_url = metadata['page_url']
            # sidebar.markdown(f"[{page_title}]({page_url})")
        
        ########### Get static LLM response ###########
        # response = create_chat_completion(messages=messages)
        # st.session_state["response"] = response

    ########### Display streaming LLM text response ###########
    with st.chat_message("assistant"):
        this_response_message = ""
        message_placeholder = body.empty()

    # format_past_first_paragraph = False # bookmark for later: make the first paragraph larger 

    copy_of_messages_for_prompt = st.session_state.messages 
    copy_of_messages_for_prompt.append({"role": "user", "content": full_prompt_with_retrievals})

    for response in create_streaming_chat_completion(messages=copy_of_messages_for_prompt):
        print('response: ', response)
        this_response_message += (response.choices[0].delta.content or "")
        message_placeholder.markdown(this_response_message + " ")

    st.session_state.messages.append({"role": "assistant", "content": this_response_message})

    # print ('message_placeholder: \n ', message_placeholder, '\n\nsession-state-messages: \n', st.session_state.messages, '\n\nresponse: \n', response)

    #####
    ### Keyboard shortcuts 
    

    ########################################################
    #### Suggested Questions ####
    ########################################################

    # post_response_messages_list = st.session_state.messages

    # print ('post_response_messages_list: \n', post_response_messages_list)

    # post_response_messages_list.append({"role": "user", "content": f"Given the above conversation, please generate a list of {NUM_SUGGESTED_QUESTIONS} insightful, thoughtful, diverse, intelligent questions that examine the heart of the matter, the potential applications, analagous systems for the topic. Respond with a list of 5 questions, separated by a newline character."})

    # print('copy_of_messages_for_question_gen: \n', post_response_messages_list)

    # suggested_questions_raw = create_chat_completion(messages=post_response_messages_list)

    # try:
    #     suggested_questions_list = suggested_questions_raw.split('\n')
    #     if not suggested_questions_list: # or len(questions_list) < 5:
    #         raise ValueError("Generated questions list doesn't exist.")
    # except Exception as e:
    #     st.error(f"Failed to parse generated questions: {e}")
    #     suggested_questions_list = []


    #  # Create a section for buttons
    # # st.markdown("---")  # Horizontal line for separation

    # # Define the callback function to update session state
    # def select_callback(i):
    #     st.session_state.selected_button = f"{i} SELECTED!"

    # # Initialize the session state variable if it doesn't exist
    # if 'selected_button' not in st.session_state:
    #     st.session_state.selected_button = ""

    # for i in range(NUM_SUGGESTED_QUESTIONS):
    #     this_button_name = suggested_questions_list[i]
    #     # Use the index `i` to create a unique key for each button
    #     button_key = f"button_{i}"
    #     if body.button(this_button_name, key=button_key, on_click=select_callback, args=(i,)):
    #         # This block is not necessary unless you want to do something immediately after the button click
    #         pass
    
    #     add_keyboard_shortcuts({
    #         f"Ctrl+{i}": suggested_questions_list[i],
    #         })

    # # Display the selected button message
    # if st.session_state.selected_button:
    #     sidebar.write(st.session_state.selected_button)

    # st.markdown("---")  # Horizontal line for separation
    ########################################################
