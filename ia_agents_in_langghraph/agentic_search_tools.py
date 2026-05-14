from dotenv import load_dotenv
import os
from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re
import json
from pygments import highlight, lexers, formatters

# load environment variables from .env file
_ = load_dotenv()

# connect
# Tavily est un moteur de recherche d'IA qui utilise des modèles de langage pour fournir des réponses synthétiques à partir de résultats de recherche. Il est conçu pour être utilisé dans des applications d'agents IA, de RAG (Retrieval-Augmented Generation) et de frameworks comme LangChain et LangGraph.
# Très bon pour :

# agents IA,
# réponses synthétiques,
# RAG,
# LangChain/LangGraph.

# Retourne :

# réponse IA,
# contenu nettoyé,
# résultats structurés.
client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

result = client.search("What is in Nvidia's new Blackwell GPU?",
                       include_answer=True)

# print the answer
print(result["answer"])

## Regular search
city = "Nador"

query = f"""
    what is the current weather in {city}?
    Should I travel there today?
"""
# DDGS est un moteur de recherche qui utilise DuckDuckGo pour fournir des résultats de recherche. Il est conçu pour être utilisé dans des applications d'agents IA, de scraping léger et de récupération rapide de liens.

# Très bon pour :

# recherche simple,
# scraping léger,
# récupérer rapidement des liens.

# Retourne surtout :

# liens,
# snippets,
# résultats “bruts”.
ddg = DDGS()


def search(query, max_results=5):
    result = ddg.text(query, max_results=max_results)
    return [i["href"] for i in result]

for i in search(query):
    print(i)

def scrape_weather_info(url):
    """Scrape content from the given URL"""
    if not url:
        return "Weather information could not be found."
    
    # fetch data
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve the webpage."

    # parse result
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


url = search(query)[0]

# scrape first wesbsite
soup = scrape_weather_info(url)

# print(f"Website: {url}\n\n")
# print(str(soup.body)[:50000])

weather_data = []
for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
    text = tag.get_text(" ", strip=True)
    weather_data.append(text)

# combine all elements into a single string
weather_data = "\n".join(weather_data)

# remove all spaces from the combined text
weather_data = re.sub(r'\s+', ' ', weather_data)
    
print(f"Website: {url}\n\n")
print(weather_data)


## Agentic Search

# run search
result = client.search(query, max_results=1)

# print first result
data = result["results"][0]["content"]

print(data)

# parse JSON
parsed_json = json.loads(data.replace("'", '"'))

# pretty print JSON with syntax highlighting
formatted_json = json.dumps(parsed_json, indent=4)
colorful_json = highlight(formatted_json,
                          lexers.JsonLexer(),
                          formatters.TerminalFormatter())

print(colorful_json)