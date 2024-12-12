
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.prompts import PromptTemplate 
from llm_tools import llm
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_core.runnables import chain

from langchain_core.runnables import RunnablePassthrough
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

blog_topic = "Digital marketing"

@chain
def perform_research(context:PromptTemplate):

    search = DuckDuckGoSearchRun()

    results = search.invoke(context["topic"])  #pass blog_topic instead
    print("\n\nResearch Results : \n\n",results)

    return results


#-----Alternate method using Tool() but not working----------------

# research_tool = Tool(
#     name = "Research Tool",
#     func = perform_research,
#     description="It searches the internet for the relevant topics and returns the result."
#     )


# tool = [research_tool]
# llm_with_tool = llm.bind_tools(tool)
#------------------------------------------------------------------------



#   Prompt Template for generate_blog
blog_template = """
You are a professional blog writer specializing in crafting optimized and engaging content. Your task is to write a blog on the topic:
"{topic}"

Guidelines:
Research: Use the provided research tool to gather information on the topic. Incorporate accurate and relevant details from your findings.
Structure:
Introduction: Begin with a captivating hook to draw readers in.
Body: Divide the content into informative paragraphs with subheadings. Address key aspects of the topic.
Conclusion: Summarize the discussion and include a clear call to action for the reader.
Tone: Write in the {tone} tone. This should align with a valid and recognizable writing style, such as informative, persuasive, casual, 
formal, or creative. If the provided tone is invalid, return an error to the user.
Word Count: Ensure the blog is exactly {word_count} words. Do not exceed or fall short of this count.
SEO Requirements:
Use long-tail keywords relevant to the topic to enhance search engine visibility.
Maintain an organic flow while embedding keywords naturally into the text.
Validation:
Tone Check: Validate that the tone is applicable to blog writing. If invalid, inform the user and halt progress until corrected.
Word Count Check: Ensure the word count is a valid integer. If not, prompt the user to re-enter a valid value.
Generate a blog that fully complies with these instructions and reflects high-quality, professional writing.


"""


generate_prompt = PromptTemplate(
    input_variables = ['topic', 'tone', 'word_count'],
    template = blog_template
)


# Using RunnablePassthrough() to keep the data unchanged but data still being converted to string

#   Creating a chain combining LLM and prompt
generation_chain = ({"topic":RunnablePassthrough(),"tone":RunnablePassthrough(),"word_count":RunnablePassthrough()} | generate_prompt | perform_research| llm )#llm_with_tool

# testing
generation_chain.invoke({"topic":"Digital marketing","tone":"Pirate","word_count":100})

# # -----------------For debugging---------------------------
# # formatted_input = generate_prompt.format(topic = 'Human', tone = 'engaging', word_count = '100')
# # print("Formatted Input:", formatted_input)

# # print(generation_chain.invoke({"topic" : 'Human', "tone" : 'engaging', "word_count" : '100'})) # no content


# Agent

def generate_blog(state:AgentState):

    """
    Writes up a blog based on the user input 

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    # print("I am inside generate_blog")  #for debugging
    global blog_topic 
    blog_topic = state['topic']
    # tone = state['tone']
    # word_count = state['word_count']
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

