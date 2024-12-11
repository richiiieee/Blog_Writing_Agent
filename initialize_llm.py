import configparser
from langchain_core.language_models.llms import LLM
from langchain_groq.chat_models import ChatGroq

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