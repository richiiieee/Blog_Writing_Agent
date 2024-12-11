from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import Tool
from agents import AgentState
from initialize_llm import llm

state:AgentState

def perform_research():
    
   
    search = DuckDuckGoSearchResults()

    print("\nI am inside perform_research\n ")

    # topic = 'Human'

    results = search.invoke(state['topic'])
#state['topic']
#{'topic': topic , 'tone': tone , 'word_count' : word_count}
    return results

# if __name__ == '__main__' :
#     reserach_op = perform_research("what are the different breeds of dogs in India")
#     print(reserach_op)

research_tool = Tool(
    name = "Research Tool",
    func = perform_research,
    description="It searches the internet for the relevant topics and returns the result."
    )

tools = [research_tool]

print(llm.invoke("hi"))

llm_with_tools = llm.bind_tools(tools = tools)   ##some error here ig

print(llm_with_tools.invoke("hi"))


# -----------Debugging--------------

# print(research_tool)
# print(llm_with_tools)

# if __name__ == '__main__':

#     # Run the tool's function directly
#     try:
#         tool_output = research_tool.func()
#         print("Tool Output:", tool_output)
#     except Exception as e:
#         print("Error while testing research_tool:", e)