from langgraph.prebuilt import create_react_agent
from initialize_llm import llm
# from tools import research_tool
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchResults

tools = [DuckDuckGoSearchResults()]
# tools = []
prompt = (
    "You are a helpful assistant. "
    "You may not need to use tools for every query - the user may just want to chat!"
)

agent = create_react_agent(model = llm, tools = tools, state_modifier=prompt)

# response = agent.invoke({"messages":[ HumanMessage(content = "What is the current conservation status of the Great Barrier Reef?")],})
# print(response)