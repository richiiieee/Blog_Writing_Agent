from agents import graph





# def stream_graph_updates(user_input: str):
#     for event in graph.stream({'question':user_input}) :
#         for value in event.values():
#           if "response" in value:
#             # print(type(value['response']))
#             print("Assistant:", value["response"].content)

def stream_graph_updates(topic: str, tine : str, wordcount : int):
    for event in graph.stream({'topic': topic , 'tone': tone , 'word_count' : wordcount}) :
        for value in event.values():
          if "response" in value:
            # print(type(value['response']))
            print("Assistant:", value["response"].content)




# if __name__ ==  "__main__":
#     while True:
#         try:
#             user_input = input("User :")
#             if user_input in ['q','quit','exit']:
#                 print("GoodBye")
#                 break
#             stream_graph_updates(user_input)
            
#             # topic,tone,word_count = extract_information(user_input)
#         except:
#             print("No input")
#             break


if __name__ ==  "__main__":
    topic = input("Topic :")
    tone = input("Tone :")
    wordcount = input("Word Count :")
    stream_graph_updates(topic,tone,wordcount)
    while True:
        try:
            repeat = input("Do you wish to continue? ('q','quit','exit') : ")
            if repeat in ['q','quit','exit']:
                print("GoodBye")
                break
            topic = input("Topic :")
            tone = input("Tone :")
            wordcount = input("Word Count :")
            stream_graph_updates(topic,tone,wordcount)
            
            # topic,tone,word_count = extract_information(user_input)
        except:
            print("No input")
            break
