import streamlit as st


def initialize_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = []


def add_user_message(message):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )


def add_ai_message(message):

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message
        }
    )


def display_chat_history():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


def clear_chat():

    st.session_state.messages = []