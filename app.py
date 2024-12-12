from blogger import graph
import streamlit as st


# The function that starts the graph

def stream_graph_updates(topic: str, tone : str, wordcount : int):
    for event in graph.stream({'topic': topic , 'tone': tone , 'word_count' : wordcount}) :
        for value in event.values():
          if "response" in value:
            # Display chatbot response
                with st.spinner("Thinking..."):
                    st.text_area("Chatbot:", value=value["response"].content, height=200)
                    print("\nAssistant:\n\n", value["response"].content)

            

if __name__ ==  "__main__":


        # Streamlit UI
    st.title("Chatbot Interface")
    st.write("Ask any question, and I'll do my best to answer!")

    # Text input for user query
    topic = st.text_input("Topic :")
    tone = st.text_input("Tone :")
    wordcount = st.text_input("Word Count :")
    # print(topic +' '+tone+' '+wordcount)
    if topic:
        stream_graph_updates(topic,tone,wordcount)

    #------- For Terminal testing------------

    # while True:
    #     try:
    #         repeat = input("Do you wish to continue? ('q','quit','exit') : ")
    #         if repeat in ['q','quit','exit']:
    #             print("GoodBye")
    #             break
    #         topic = input("Topic :")
    #         tone = input("Tone :")
    #         wordcount = input("Word Count :")
            
    #         stream_graph_updates(topic,tone,wordcount)
            
    #         # topic,tone,word_count = extract_information(user_input)
    #     except:
    #         print("No input")
    #         break