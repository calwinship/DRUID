import streamlit as st 
from utils import initialise_openai_client, get_lesson_prompt_template
from config import CONFIG
import json



st.header(':blue[Statistics 2]')

try :
    client = initialise_openai_client(st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

# st.divider()
# st.write('This lesson starts with questions')


with st.expander('Links'):
    st.write("First, go through each of these pages. Some pages have toggle heading at the top. Go through these and think of how you can apply them to the questions later. Write down some interesting observations.")
    link1 = '[The Art of Statistics Home Page](https://artofstat.com/web-apps)'
    link2 = '[The Normal Distribution](https://istats.shinyapps.io/NormalDist/)'
    link3 = '[Sampling from Any Distribution](https://istats.shinyapps.io/SampDist_discrete/)'
    st.info(link1)
    st.info(link2)
    st.info(link3)

with st.expander("Q1"):
    st.image("images/Exam17_2_Q8a.png")
    st.image("images/Exam17_2_Q8b.png")

with st.expander("Q2"):
    st.image("images/Exam18_2_Q8.png")

with st.expander("Q3"):
    st.image("images/Exam18_2_Q2a.png")
    st.image("images/Exam18_2_Q2b.png")


# config items
name = CONFIG["name"]
llm_model = CONFIG["llm_model"]
temperature = CONFIG["temperature"]

topic = 'statistics2'
objective = 'a'
id = f"{topic}{objective}"

# link to the questions database 
json_file_path = 'data/lessons_repo.json'
with open(json_file_path, 'r') as f:
    file = json.load(f)
objectives = file[topic]['objectives'][objective]
# images =  exam['images']

# for image in images:
#     st.image(image)


if id not in st.session_state:
    st.session_state[id] = get_lesson_prompt_template(id, name, objectives)
prompt_template = st.session_state[id]

prompt = st.chat_input("Type here")

with st.expander('Concept 1: Sampling Variability'):
    st.write("The objective is: ")
    st.success(f"{objectives}")
    # st.info()
    # st.write("This is a self-directed lesson meaning you need to extract the information to answer the question and understand the topic. Take notes!")
        # Display chat messages from history on app rerun
    
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
