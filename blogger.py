
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.prompts import PromptTemplate 
from llm_tools import llm
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_core.runnables import chain
from langchain.utilities import WikipediaAPIWrapper

from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain.agents import initialize_agent
# from prompts_templates import generation_chain
# from researcher import agent



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

state : AgentState

# blog_topic = "Digital marketing"

@chain
def perform_research(context):

    wikipedia = WikipediaAPIWrapper()

    wikipedia_tool = Tool(
        name='wikipedia',
        func= wikipedia.run,
        description="Useful for when you need to look up a topic, country or person on wikipedia"
    )

    search = DuckDuckGoSearchRun()

    duckduckgo_tool = Tool(
        name='DuckDuckGo Search',
        func= search.run,
        description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
    )

    tools = [wikipedia_tool , duckduckgo_tool]

    

    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
    )

    results = zero_shot_agent.run(context["topic"])

    
    return results



#-----Alternate method using Tool() but not working----------------
# from langchain_core.messages import HumanMessage,SystemMessage
# research_tool = Tool(
#     name = "Research Tool",
#     func = perform_research,
#     description="It searches the internet for the relevant topics and returns the result."
#     )

# tool = DuckDuckGoSearchRun()
# # tool = [research_tool]
# llm_with_tool = llm.bind_tools(tool)

# #asking user query in a new request/prompt
# ai_msg = llm_with_tools.invoke(messages)
# messages.append(ai_msg)

# for tool_call in ai_msg.tool_calls:
#     selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
#     #asking LLM to generate function call with arguments
#     tool_output = selected_tool.invoke(tool_call["args"])
#     messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

# #finally prompting LLM with custom function schema and all required arguments
# llm_with_tools.invoke(messages)
#------------------------------------------------------------------------



#   Prompt Template for generate_blog
blog_template =  """
You are a professional blog writer specializing in crafting optimized and engaging content. Your task is to write a blog on the topic:
"{topic}"

Guidelines:
Research: Research on the given topic and write the blog incorporating the points from the retreived information.

Structure:
Introduction: Begin with a captivating hook to draw readers in.

Body: Divide the content into informative paragraphs with subheadings. Address key aspects of the topic.

Conclusion: Summarize the discussion and include a clear call to action for the reader.

Tone: Write in the {tone} tone. This should align with a valid and recognizable writing style, such as informative, persuasive, casual, 
formal, or creative. If the provided tone is invalid, return an error to the user.

Word Count: "Write a blog about {topic} with exactly {word_count} words. Ensure the word count is strictly followed; no more, no less.
 If you reach the word count limit, stop. If you fall short, add a concise conclusion or additional relevant points to meet the required
word count. After every section, check the word count and adjust accordingly. If necessary, condense or remove parts to stay within
the limit."

SEO Requirements:
Use long-tail keywords relevant to the topic to enhance search engine visibility.
Maintain an organic flow while embedding keywords naturally into the text.

Generate a blog that fully complies with these instructions and reflects high-quality, professional writing.


"""


generate_prompt = PromptTemplate(
    input_variables = ['topic', 'tone', 'word_count'],
    template = blog_template
)





#   Creating a chain combining LLM and prompt
def structure_prompt(promp):
    return promp['x'].text + 'Context is: ' + promp['y']

generation_chain =  RunnableParallel({'x': generate_prompt, 'y': perform_research}) | RunnableLambda(structure_prompt) | llm #llm_with_tool

# generation_chain.invoke({"topic": "cups", "tone" : "pirate" , "word_count" : 100})

# Agent

def generate_blog(state:AgentState):

    """
    Writes up a blog based on the user input 

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    # global blog_topic = state['topic']

    blog =  generation_chain.invoke({
        "topic":state['topic'],
        "tone":state['tone'],
        "word_count":state['word_count']
    })

    return {"response" : blog}


# Defining the graph

graph_builder = StateGraph(AgentState)

graph_builder.add_node("Generator", generate_blog)

graph_builder.add_edge(START,"Generator")
graph_builder.add_edge("Generator",END)

graph = graph_builder.compile()

