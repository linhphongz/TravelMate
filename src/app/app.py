import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from domain.Main import Main
import time
import os

def sent_input():
    st.session_state.send_input = True

def respone_when_use_image(image_file):
    return "Image processed and response generated."

def main():
    st.set_page_config(
        page_title="Aizen_chatbot",
        page_icon="🐺",
        layout="centered",
    )
    st.title("🤖 Integrated chatbots")
    
    chat_container = st.container()
    
    if 'send_input' not in st.session_state:
        st.session_state['send_input'] = False
        st.session_state["user_question"] = ""
        st.session_state["user_input"] = ""
        st.session_state["flag_img_file"] = False

    st.sidebar.title("Upload your file!")
    Image_file = st.sidebar.file_uploader("Upload Image File", type=["jpg", "jpeg", "png"])

    st.session_state.user_question = st.chat_input("Enter your question", on_submit=sent_input)
    
    chat_history = StreamlitChatMessageHistory(key="history")
    if "chat" not in st.session_state:
        st.session_state.chat = Main(chat_history=chat_history)
    
    with chat_container:
        for message in chat_history.messages:
            with st.chat_message(message.type):
                st.markdown(message.content)
    
    if st.session_state.send_input:
        if Image_file and st.session_state.flag_img_file == False:
            st.session_state.flag_img_file = True
            with chat_container:
                with st.chat_message("human"):
                    st.markdown(st.session_state.user_question)
            respone_img = respone_when_use_image(Image_file)
            with chat_container:
                chat_history.add_user_message(st.session_state.user_question)
                chat_history.add_ai_message(respone_img)
                with st.chat_message("ai"):
                    typing_placeholder = st.empty()
                    tmp_str = ""
                    for char in respone_img:
                        tmp_str += char
                        time.sleep(0.01)
                        typing_placeholder.markdown(tmp_str)
                st.session_state.user_question = ""
                st.session_state.send_input = False
        
        elif st.session_state.user_question != "":
            with chat_container:
                with st.chat_message("human"):
                    st.markdown(st.session_state.user_question)
                llm_response = st.session_state.chat.handle_user_question(question=st.session_state.user_question)
                tmp_str = ""
                with st.chat_message("ai"):
                    typing_placeholder = st.empty()
                    for char in llm_response["response"]:
                        tmp_str += char
                        time.sleep(0.01)
                        typing_placeholder.markdown(tmp_str)
                st.session_state.send_input = False

if __name__ == "__main__":
    main()
