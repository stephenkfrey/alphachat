import os 
import streamlit as st
from openai import OpenAI

from openai_functions import create_chat_completion
from add_query import query_db

# layout widemode
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("ChatGPT-like clone")

st.markdown("---")  # Horizontal line for separation
body, sidebar = st.columns(2)  # Create two columns
body.markdown("## Body")
sidebar.markdown("## Sidebar")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    response = create_chat_completion(messages=messages)
    st.session_state["response"] = response

    retrievals = query_db(user_prompt) 
    print(retrievals)

    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        sidebar.write(retrievals)
        st.write(st.session_state["response"])

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
