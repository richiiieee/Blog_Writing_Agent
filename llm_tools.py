import configparser
# from langchain_core.language_models.llms import LLM
from langchain_groq.chat_models import ChatGroq
# from tools import tools
# from langchain_community.tools import DuckDuckGoSearchResults
# from langchain.agents import Tool
# from agents import AgentState
# from llm_tools import llm, llm_with_tools

# state:AgentState

# Initialize configparser
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve values
model = config.get('groq', 'model')
temperature = float(config.get('groq', 'temperature'))
api_key = config.get('groq', 'api_key')

# Use these values to create your LLM instance
llm = ChatGroq(model=model, temperature=temperature, api_key=api_key)





