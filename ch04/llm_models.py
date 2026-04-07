from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv() #A
google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") #B

def get_llm(): #C
    if not google_api_key:
        raise ValueError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment.")

    return ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-2.5-flash",
    )
#A Load the environment variables from the .env file
#B Get the Google API key from the environment variables
#C Instantiate and return the Gemini chat model
