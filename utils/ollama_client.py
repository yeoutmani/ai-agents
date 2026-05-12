import os
from dotenv import load_dotenv
import ollama

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama.com")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

headers = {}
if OLLAMA_API_KEY:
    headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

client = ollama.Client(host=OLLAMA_HOST, headers=headers if headers else None)
