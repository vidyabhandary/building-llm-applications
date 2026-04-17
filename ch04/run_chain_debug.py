import json

from chain_1_2 import assistant_instructions_chain
from chain_2_1 import web_searches_chain

# question to debug
question = "Which are the best places to visit in Artoga?"

print("Running assistant selection for question:\n", question)
assistant_result = assistant_instructions_chain.invoke({'user_question': question})
print("\n--- ASSISTANT SELECTION ---")
print(json.dumps(assistant_result, indent=2, ensure_ascii=False))

# Prepare input for web searches chain (the chain's first RunnableLambda will add num_search_queries)
web_input = {
    'assistant_instructions': assistant_result.get('assistant_instructions') if isinstance(assistant_result, dict) else assistant_result,
    'user_question': assistant_result.get('user_question') if isinstance(assistant_result, dict) else question
}

print("\nRunning web search generation with assistant instructions...")
web_searches_result = web_searches_chain.invoke(web_input)
print("\n--- GENERATED WEB SEARCH QUERIES ---")
print(json.dumps(web_searches_result, indent=2, ensure_ascii=False))

print("\nDone.")
