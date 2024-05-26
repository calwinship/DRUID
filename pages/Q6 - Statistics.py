import streamlit as st 
from utils import initialise_openai_client, get_prompt_template
from config import CONFIG
import json

# config items
name = CONFIG["name"]
llm_model = CONFIG["llm_model"]
temperature = CONFIG["temperature"]

year = '2022'
paper = '2'
q = '8'
id = f"{year}_{paper}_{q}"

# link to the questions database 
json_file_path = 'data/questions_repo.json'
with open(json_file_path, 'r') as f:
    file = json.load(f)
exam = file[year][paper][q]
images =  exam['images']

for image in images:
    st.image(image)

try :
    client = initialise_openai_client(st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

questions = exam['parts']
solutions = exam['solutions']

if id not in st.session_state:
    st.session_state[id] = get_prompt_template(id, name, questions, solutions)
prompt_template = st.session_state[id]

# Display chat messages from history on app rerun
for message in prompt_template:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Enter your answer here")  

try:
    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        prompt_template.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in prompt_template
                ],
                temperature=temperature,
                stream=True
            )
            response = st.write_stream(stream)
        prompt_template.append({"role": "assistant", "content": response})
except NameError:
    st.error('Insert your KEY in the home menu before starting')
