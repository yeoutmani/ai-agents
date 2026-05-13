import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Chargement des variables d'environnement (.env)
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama.com/api")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

# Configuration des headers HTTP requis pour Ollama Cloud
headers = {}
if OLLAMA_API_KEY:
    headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

# Initialisation du composant ChatOllama pour le cloud
model = ChatOllama(
    model="gpt-oss:120b-cloud",
    base_url=OLLAMA_HOST,  # Définit l'URL cloud à la place de localhost
    client_kwargs={        # Transmet les headers de sécurité au client HTTP interne
        "headers": headers if headers else None
    }
)

