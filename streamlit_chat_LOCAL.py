import os 
import streamlit as st
import requests
import json
from openai import OpenAI
from openai_functions import create_chat_completion

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

############ Select a collection ############
one,two,three,four,five=st.columns(5)
# Read the database names from db_names.txt
with open('db_names.txt', 'r') as file:
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
        {"role": "assistant", "content": "👀 🔎 🌍. What do you want to understand more?"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    # st.chat_message(msg["role"]).write(msg["content"])
    body.chat_message(msg["role"]).write(msg["content"])

############ Helper fun ############

def get_retrievals_from_server(prompt): 
    selected_db_name = selected_db.replace('\n', '').replace(' ', '')
    response = requests.post('http://localhost:5000/query', 
                             json={'prompt': prompt, 
                                   'collection_name': selected_db_name,
                                   "num_results":NUM_RETRIEVAL_RESULTS}
                                   )
    result = response.json()
    return result 

############ Main conversation and retrieval loop ############

if user_prompt := st.chat_input(placeholder="How do generative video models work?"):
    with st.spinner("👀"):
        messages.append({"role": "user", "content": user_prompt})
        # st.chat_message("user").write(user_prompt)
        body.chat_message("user").write(user_prompt)

        ########### Get LLM response ###########
        response = create_chat_completion(messages=messages)
        st.session_state["response"] = response

        ########### Get and filter retrievals ###########
        retrievals = get_retrievals_from_server(user_prompt) 

        # Filter out retrievals with distance greater than THRESHOLD 
        filtered_retrievals = [doc for doc, dist in zip(retrievals['documents'][0], retrievals['distances'][0]) if dist > RETRIEVAL_RELEVANCE_THRESHOLD]
        retrievals['documents'][0] = filtered_retrievals
        print(retrievals)
    #################################################

    ########### Display text response and images ###########
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})

        # body.write(st.session_state["response"])
        body.markdown(f"<p style='font-size:20px;'>{st.session_state['response']}</p>", unsafe_allow_html=True)
        # st.write(st.session_state["response"])

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


