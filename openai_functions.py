import os 
from openai import OpenAI

# do loaddotenv 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv
load_dotenv()

def create_chat_completion(messages, model="gpt-3.5-turbo"): 
    response = client.chat.completions.create(
        model=model, 
        messages=messages
        )
    return response.choices[0].message.content 