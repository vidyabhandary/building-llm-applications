from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, TypedDict, Optional
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openrouter_api_key:
        return ChatOpenAI(
            api_key=openrouter_api_key,
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        )

    if openai_api_key:
        return ChatOpenAI(
            api_key=openai_api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        )

    raise ValueError(
        "Set OPENROUTER_API_KEY or OPENAI_API_KEY in your environment."
    )

# Define typed dictionaries for state handling
class AssistantInfo(TypedDict):
    assistant_type: str
    assistant_instructions: str
    user_question: str

class SearchQuery(TypedDict):
    search_query: str
    user_question: str

class SearchResult(TypedDict):
    result_url: str
    search_query: str
    user_question: str
    is_fallback: Optional[bool]

class SearchSummary(TypedDict):
    summary: str
    result_url: str
    user_question: str
    is_fallback: Optional[bool]

class ResearchReport(TypedDict):
    report: str

# Graph state
class ResearchState(TypedDict):
    user_question: str
    assistant_info: Optional[AssistantInfo]
    search_queries: Optional[List[SearchQuery]]
    search_results: Optional[List[SearchResult]]
    search_summaries: Optional[List[SearchSummary]]
    research_summary: Optional[str]
    final_report: Optional[str]
    used_fallback_search: Optional[bool]
    relevance_evaluation: Optional[Dict[str, Any]]
    should_regenerate_queries: Optional[bool]
    iteration_count: Optional[int]
