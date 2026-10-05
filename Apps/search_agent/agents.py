from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
import os

# tools
@tool
def google_search(query:str) -> str:
    """
        Search Google for up to date information on the web.

        Args: query: What to search on google

        Returns: Top search results as the plan texts
    """
    search=GoogleSerperAPIWrapper(serper_api_key=os.getenv("SERPER_API_KEY"))
    return search.run(query)

# LLM = GROQ
llm=ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT="""
    You are a helpful research assistant with access to google.

"""

agent=create_agent(
    model=llm,
    tools=[google_search],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)
# result=agent.invoke({"messages":[{"role":"user","content":"What is the RAG ?"}]},
#                     config={"configurable":{"thread_id":"1"}})
# print(result["messages"][-1].content)
