import streamlit as st


def user_message(message):

    with st.chat_message("user"):

        st.markdown(message)


def ai_message(message):

    with st.chat_message("assistant"):

        st.markdown(message)