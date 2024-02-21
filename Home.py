import streamlit as st

st.image('logo.JPG')

st.write(''' \n\n\n\n\n
            
            
            DRUID is an AI-powered personal tutor.\n\nNow. Every student can have access to a personalised learning experience to help them fulfil their potential.
        
        '''
            
            )

openai_api_key = st.text_input('Enter your OpenAI API key to get started', key="chatbot_api_key", type="password")

  

if openai_api_key:
    st.session_state["api_key"] = openai_api_key
    st.info(' \nGreat - Now get started with one of the lessons or exam questions on the left.')




