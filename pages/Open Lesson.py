import streamlit as st
import datetime
from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv() #

st.title('Open Lesson') 


name = 'Aidan'
# interests = ['hurling', 'rugby', 'electrician']

# Get the current date and define the date after which the model should be set to "gpt-3.5-turbo"
current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

if "api_key" not in st.session_state:
    st.session_state["api_key"] = 0

if st.session_state["api_key"] == 0:
    st.text('Insert your API KEY in the home menu before starting')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

# client = ChatOpenAI(temperature=0.0, model=st.session_state["openai_model"], openai_api_key=st.session_state["api_key"])
client = OpenAI(api_key=st.session_state["api_key"])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are teaching {name} whatever he wants. Be creative and engaging. You must use accessible language and your messages should be short. Rather than provide answers, you should ask questions to test {name}'s understanding. Make sure to know if the student's answer is correct or not, even if the student gives it in a different format. 
        You should encourage the student to look for examples and to really think about practical applications. Summarise the lesson when complete. 
        '''
    }, 
        {"role": "assistant", "content": f"Hi {name}! What would you like to know more about: "}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input          
prompt = st.chat_input(" ")  

if prompt:
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True, 
            temperature=0.2
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})






