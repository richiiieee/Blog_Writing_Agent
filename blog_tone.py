from initialize_llm import llm
from langchain_core.prompts import PromptTemplate 


def set_blog_tone(blog_content, tone):
    # Create a prompt to set the tone for the blog
    prompt = f"Rewrite the following blog in a {tone} tone:\n\n{blog_content}"
    
    
    # Create an LLMChain to process the tone change
    chain = prompt=PromptTemplate(template=prompt, input_variables=["blog_content"]) | llm
    
    # Execute the chain to generate the content with the specified tone
    result = chain.run({"blog_content": blog_content})
    
    return result

if __name__== '__main__':
    set_blog_tone()