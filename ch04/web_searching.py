import os
from typing import List
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

def web_search(
    web_query: str, 
    num_results: int) -> List[str]:
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if tavily_api_key:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_api_key,
                "query": web_query,
                "max_results": num_results,
                "search_depth": "basic",
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return [r["url"] for r in data.get("results", []) if "url" in r]

    with DDGS() as ddgs:
        results = ddgs.text(web_query, max_results=num_results)
        return [r['href'] for r in results]
