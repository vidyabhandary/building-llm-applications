import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv() #A


def get_llm(): #B
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    if not provider:
        if openrouter_api_key:
            provider = "openrouter"
        elif google_api_key:
            provider = "google"
        else:
            raise ValueError(
                "Set LLM_PROVIDER plus its API key, or provide either "
                "OPENROUTER_API_KEY or GOOGLE_API_KEY / GEMINI_API_KEY."
            )

    if provider == "openrouter":
        if not openrouter_api_key:
            raise ValueError(
                "Set OPENROUTER_API_KEY in your environment for LLM_PROVIDER=openrouter."
            )

        return ChatOpenAI(
            api_key=openrouter_api_key,
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        )

    if provider in {"google", "gemini"}:
        if not google_api_key:
            raise ValueError(
                "Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment "
                "for LLM_PROVIDER=google."
            )

        return ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
        )

    raise ValueError(
        "Unsupported LLM_PROVIDER. Use 'openrouter' or 'google'."
    )


#A Load environment variables from the .env file
#B Instantiate and return the configured chat model
