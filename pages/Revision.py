import streamlit as st 
from utils import initialise_openai_client, get_lesson_prompt_template
from config import CONFIG
import json



st.header(':blue[Revision]')

try :
    client = initialise_openai_client(st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

# st.divider()
# st.write('This lesson starts with questions')


# config items
name = CONFIG["name"]
llm_model = CONFIG["llm_model"]
temperature = CONFIG["temperature"]

topic = 'revision'
objective = 'a'
id = f"{topic}{objective}"

# link to the questions database 
# json_file_path = 'data/lessons_repo.json'
# with open(json_file_path, 'r') as f:
#     file = json.load(f)
objectives = ['algebra 1', 'algebra 2']
# images =  exam['images']

# for image in images:
#     st.image(image)


if id not in st.session_state:
    st.session_state[id] = get_lesson_prompt_template(id, name, objectives)
prompt_template = st.session_state[id]

prompt = st.chat_input("Type here")



st.info('This revision lesson covers Algebra 1,2, 3 and Complex Numbers. Revise the topics as you go through the questions. Use the chatbot below for assistance. ')


with st.expander("Q1"):
    st.image("images/Exam19_1_Q5a.png")
    st.image("images/Exam19_1_Q5b.png")
    st.image("images/Exam19_1_Q5c.png")

with st.expander("Q1 - Marking Scheme"):
    st.image("images/MS19_1_Q5a.png")
    st.image("images/MS19_1_Q5b.png")

with st.expander("Q2"):
    st.image("images/Exam19_1_Q6a.png")

with st.expander("Q2 - Marking Scheme"):
    st.image("images/MS19_1_Q6a.png")
    st.image("images/MS19_1_Q6b.png")

with st.expander("Q3"):
    st.image("images/Exam19_1_Q1a.png")
    st.image("images/Exam19_1_Q1b.png")

with st.expander("Q3 - Marking Scheme"):
    st.image("images/MS19_1_Q1a.png")
    st.image("images/MS19_1_Q1b.png")

with st.expander("Q4"):
    st.image("images/Exam18_1_Q1a.png")
    st.image("images/Exam18_1_Q1b.png")

with st.expander("Q4 - Marking Scheme"):
    st.image("images/MS18_1_Q1a.png")

with st.expander("Q5"):
    st.image("images/Exam23_1_Q1.png")

with st.expander("Q5 - Marking Scheme"):
    st.image("images/MS23_1_Q1a.png")
    st.image("images/MS23_1_Q1b.png")

with st.expander("Q6"):
    st.image("images/Exam23_1_Q4a.png")
    st.image("images/Exam23_1_Q4b.png")

with st.expander("Q6 - Marking Scheme"):
    st.image("images/MS23_1_Q4a.png")
    st.image("images/MS23_1_Q4b.png")
    st.image("images/MS23_1_Q4c.png")

with st.expander("Q7"):
    st.image("images/Exam17_1_Q5.png")

with st.expander("Q7 - Marking Scheme"):
    st.image("images/MS17_1_Q5a.png")

with st.expander("Q8"):
    st.image("images/Exam17_1_Q2.png")

with st.expander("Q8 - Marking Scheme"):
    st.image("images/MS17_1_Q2a.png")
    st.image("images/MS17_1_Q2b.png")


# with st.expander("Q2 - Marking Scheme"):
#     st.image("images/MS19_1_Q6a.png")




for message in prompt_template:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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