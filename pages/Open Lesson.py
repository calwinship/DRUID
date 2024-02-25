import streamlit as st
import datetime
from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv() #

st.title('Open Lesson') 

name = 'Aidan'

# Get the current date and define the date after which the model should be set to "gpt-3.5-turbo"
current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
if current_date > target_date:
    llm_model = "gpt-4-turbo-preview"
else:
    llm_model = "gpt-3.5-turbo-0301"

if "api_key" not in st.session_state:
    st.session_state["api_key"] = 0

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

# client = ChatOpenAI(temperature=0.0, model=st.session_state["openai_model"], openai_api_key=st.session_state["api_key"])
client_a = OpenAI(api_key=st.session_state["api_key"])


# Initialize chat history
if "omessages" not in st.session_state:
    st.session_state.omessages = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are teaching {name} whatever he wants (as long as it's maths related). Be creative and engaging. 
        You must use accessible language and your messages should be short. 
        Rather than provide answers, you should ask questions to test {name}'s understanding. 
        When a student gives an answer to a question, especially a complex one, you should also try the question, explaining all of your workings. Be very meticulous when correcting the student's answers. 
        You should encourage the student to look for examples and to really think about practical applications. 
        '''
    }, 
        {"role": "assistant", "content": f"This section is all about asking questions about maths problems or topics that you'd like to know more about'. Type below to get started."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.omessages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input          
prompt = st.chat_input("Type here")  

if prompt:
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.omessages.append({"role": "user", "content": prompt})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_a.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.omessages
            ],
            stream=True, 
            temperature=0.2
        )
        response = st.write_stream(stream)
    st.session_state.omessages.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')

if len(st.session_state.omessages) >= 3:
    if st.button('Clear chat history'):
        st.session_state.omessages = [{
            'role': 'system',
            'content': f'''
            You are a high school math teacher, and today you are teaching {name} whatever he wants. Be creative and engaging. You must use accessible language and your messages should be short. Rather than provide answers, you should ask questions to test {name}'s understanding. Make sure to know if the student's answer is correct or not, even if the student gives it in a different format. 
            You should encourage the student to look for examples and to really think about practical applications. Summarise the lesson when complete. 
            '''
        }, 
            {"role": "assistant", "content": f"Hi {name}! What would you like to know more about: "}
        ]
