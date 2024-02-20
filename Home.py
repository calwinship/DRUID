import streamlit as st

st.image('logo.JPG')

st.text(''' \n\n\n\n\n
            
            
            DRUID is an advanced personal tutor.\n\nNow. Every student can have access to personalised learning experiences to help \nthem fulfil their potential.
        
        '''
            
            )

openai_api_key = st.text_input('', placeholder="Enter your OpenAI API key to get started", key="chatbot_api_key", type="password")

  

if openai_api_key:
    st.session_state["api_key"] = openai_api_key
    st.text(' \nGreat - Now get started with one of the lessons or exam questions on the left.')




