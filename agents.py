import json
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
# from prompts_templates import extraction_chain,generation_chain
from prompts_templates import generation_chain
from langchain.agents import Tool, initialize_agent
from langgraph.prebuilt import ToolNode
from researcher import agent


class AgentState(TypedDict):
    """

    Attributes:
        question: question
        response: LLM generated blog
        topic : topic of the blog
        tone : tone of the blog
        word_count : word limit of the blog
    """

    # question: str
    response: str
    topic: str
    tone:str
    word_count : int





def generate_blog(state:AgentState):

    """
    Writes up a blog based on the user input 

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("I am inside generate_blog")  #for debugging

    blog =  generation_chain.invoke({
        "topic":state['topic'],
        "tone":state['tone'],
        "word_count":state['word_count']
    })

    return {"response" : blog}



graph_builder = StateGraph(AgentState)

# graph_builder.add_node("Extractor", extract_information)
graph_builder.add_node("Generator", generate_blog)
# research_tool_node = ToolNode(tools=research_tool)
# graph_builder.add_node("tools",research_tool_node)

# graph_builder.add_edge(START,"Extractor")
graph_builder.add_edge(START,"Generator")
# graph_builder.add_edge("Researcher","Generator")
graph_builder.add_edge("Generator",END)

graph = graph_builder.compile()

# print(generation_chain.invoke({'topic': "water scarcity" , 'tone': 'educational' , 'word_count' : 100}))  NOT GIVING ANY CONTENT