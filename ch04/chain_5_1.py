from llm_models import get_llm
from prompts import (
    RESEARCH_REPORT_PROMPT_TEMPLATE
)
from chain_1_2 import assistant_instructions_chain
from chain_2_1 import web_searches_chain
from chain_3_1 import search_result_urls_chain
from chain_4_1 import search_result_text_and_summary_chain

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

extract_user_question = RunnableLambda(
    lambda x: x.get('user_question', '') if isinstance(x, dict) else x
)

search_and_summarization_chain = (
    search_result_urls_chain 
    | search_result_text_and_summary_chain.map() # parallelize for each url
    | RunnableLambda(lambda x: 
        {
            'summary': '\n'.join([i['summary'] for i in x]), 
            'user_question': x[0]['user_question'] if len(x) > 0 else ''
        })
)

web_research_chain = (
    RunnableParallel(
        {
            'original_question': extract_user_question,
            'assistant_input': extract_user_question | assistant_instructions_chain
        }
    )
    | RunnableParallel(
        {
            'original_question': lambda x: x['original_question'],
            'web_searches': RunnableLambda(
                lambda x: x['assistant_input']
            ) | web_searches_chain
        }
    )
    | RunnableParallel(
        {
            'original_question': lambda x: x['original_question'],
            'search_summaries': RunnableLambda(
                lambda x: x['web_searches']
            ) | search_and_summarization_chain.map() # parallelize for each web search
        }
    )
    | RunnableLambda(lambda x:
        {
            'research_summary': '\n\n'.join(
                [i['summary'] for i in x['search_summaries']]
            ),
            'user_question': (
                x['search_summaries'][0]['user_question']
                if len(x['search_summaries']) > 0
                else x['original_question']
            )
        }
    )
    | RESEARCH_REPORT_PROMPT_TEMPLATE | get_llm() | StrOutputParser()
)
