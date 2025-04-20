import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_llm():
    """Initialize and return the language model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")
        
    return ChatOpenAI(
        model="gpt-4",  # or another model of your choice
        temperature=0.7,
        api_key=api_key
    )
