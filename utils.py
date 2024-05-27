# utils.py

from openai import OpenAI
import streamlit as st

def initialise_openai_client(api_key):
    try:
        client = OpenAI(api_key=api_key)
        return client
    except KeyError:
        return None
    
def get_lesson_prompt_template(id, name, objectives):
    # Initialise chat history
    if id not in st.session_state:
        st.session_state.id = [
            {
                'role': 'system',
                'content': f'''
                You are a secondary school math teacher, helping {name} with a self-directed maths lesson.  
                Use accessible language and give very short answers. 
                Your role is to guide, not to perform calculations. 
                Today's lesson objective is: {objectives}. 
                Try to lead the student in a direction at the end of each prompt. 
                Come up with examples to help make the objective concrete.
                All equations and mathematical expressions should be enclosed within two dollar signs ($$) to ensure clarity, for example $\frac...$. 
                When you are working through questions, go one step at a time and don't be afraid to say you don't know the answer if you are unsure.
                '''
                }, 
            {
                "role": "assistant", 
                "content": f"This is a self-directed lesson meaning you need to extract the information to fully understand the objectives. If there is anything you don't understand, ask here."
                }
                ]
        return st.session_state.id
    else:
        return st.session_state.id
    
def get_prompt_template(id, name, questions, solutions):
    # Initialise chat history
    if id not in st.session_state:
        st.session_state.id = [
            {
                'role': 'system',
                'content': f'''
                You are a high school math teacher, and today you are working with {name} on a maths question. 
                All equations and mathematical expressions should be enclosed within two dollar signs ($$) to ensure clarity, for example $\frac...$. 
                Use accessible language and give concise answers. 
                Your role is to guide, not to provide direct answers. 
                Today's task involves completing: {questions}.
                Avoid giving away the answer unless they are checking their solution and have provided information on how they got there.
                Foster an environment where {name} is motivated to find the solutions independently.
                After each attempt, whether correct or incorrect, engage in a constructive discussion to understand {name}'s thought process. 
                If an error is made, encourage {name} to analyze and understand the mistake before moving forward. 
                Answers and solutions are provided for your reference as {solutions}, but use them judiciously to verify correctness and provide guidance when absolutely necessary. 
                When you are working through questions, go one step at a time and don't be afraid to say you don't know the answer if you are unsure.
                '''
                }, 
            {
                "role": "assistant", 
                "content": f"Try the question first and let me know what you get."
                }
                ]
        return st.session_state.id
    else:
        return st.session_state.id
        
    