from tavily import TavilyClient
from dotenv import load_dotenv
import os   
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")    

client = TavilyClient(api_key=TAVILY_API_KEY)

def web_search(query):
    res = client.search(query=query, max_results=3)
    return [r["content"] for r in res["results"]]
