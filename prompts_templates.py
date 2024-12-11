from langchain_core.prompts import PromptTemplate 
from researcher import agent
from tools import llm,llm_with_tools





# # Template for researcher 
# research_template = """
# You are an expert researcher tasked with gathering insights on a specific topic. Follow the steps below to create a detailed report:

# 1. **Research on the Topic**: Conduct an in-depth exploration of the topic `{topic}`. Surf through credible sources on the internet and gather the most relevant and up-to-date information.

# 2. **Identify the Next Big Trend**: Focus on discovering the next major trend or development related to `{topic}`. Provide a clear description of what this trend involves and why it's important.

# 3. **Analyze the Pros and Cons**:
#     - List the **advantages** of the trend or development.
#     - Highlight the **disadvantages** or potential challenges associated with the trend.

# 4. **Market Opportunities**: Identify and explain any **market opportunities** this trend may present. Consider how businesses or industries might capitalize on this trend.

# 5. **Potential Risks**: Discuss the **risks** or challenges that may arise from pursuing or being affected by this trend. This could include market volatility, legal/regulatory concerns, or ethical considerations.

# 6. **Final Report**: Summarize the key points of your findings, clearly articulating the following:
#     - The identified trend in `{topic}`
#     - The pros and cons associated with it
#     - The market opportunities
#     - The potential risks

# Deliver a well-structured and insightful final report that offers a comprehensive analysis of the topic.
# """



#   Prompt Template for generate_blog
blog_template = """
You are a professional blog writer. Write a comprehensive blog on the topic:
"{topic}"
Use the research tool.

Make sure the blog includes:
1. A catchy introduction.
2. Informative body paragraphs with subheadings.
3. A conclusion with a call to action.

The tone should be {tone}.
Word count: {word_count} words.

Make sure to stick exactly to the {word_count}, do not exceed. Use SEO keywords 
in the blog,specifically long-tail keywords to optimize the blog for search results.

"""

# research_prompt = PromptTemplate(
#     input_variables=['topic'],
#     template = research_template
# )


generate_prompt = PromptTemplate(
    input_variables = ['topic', 'tone', 'word_count'],
    template = blog_template
)



#   Creating a chain combining LLM and prompt
generation_chain = generate_prompt | llm_with_tools  #llm_with_tools not working

## llm_with_tools is the problem, it worked with llm

# -----------------For debugging---------------------------
# formatted_input = generate_prompt.format(topic = 'Human', tone = 'engaging', word_count = '100')
# print("Formatted Input:", formatted_input)

# print(generation_chain.invoke({"topic" : 'Human', "tone" : 'engaging', "word_count" : '100'})) # no content


