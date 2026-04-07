from duckduckgo_search import DDGS
from typing import List

def web_search(
    web_query: str, 
    num_results: int) -> List[str]:
    with DDGS() as ddgs:
        results = ddgs.text(web_query, max_results=num_results)
        return [r['href'] for r in results]