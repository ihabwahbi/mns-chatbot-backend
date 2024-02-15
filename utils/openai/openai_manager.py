from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_handle_initial_msg(prompt):
    thread = client.beta.threads.create()
    thread_id = thread.id
    print("Thread id is ", thread_id)
    print("API Key is ", client)
    return None