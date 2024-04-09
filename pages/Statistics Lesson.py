import streamlit as st 
from utils import initialise_openai_client, get_lesson_prompt_template
from config import CONFIG
import json



st.header(':blue[Statistics 2]')
st.divider()
st.write('This lesson starts with questions')

link1 = '[The Art of Statistics Home Page](https://artofstat.com/web-apps)'
st.markdown('hello '+link1, unsafe_allow_html=True)
link2 = '[The Normal Distribution](https://istats.shinyapps.io/NormalDist/)'
st.markdown(link2, unsafe_allow_html=True)
link3 = '[Sampling from Any Distribution](https://istats.shinyapps.io/SampDist_discrete/)'
st.markdown(link3, unsafe_allow_html=True)
st.info('hello '+link1)

st.divider()


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

try :
    client = initialise_openai_client(st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')


if id not in st.session_state:
    st.session_state[id] = get_lesson_prompt_template(id, name, objectives)
prompt_template = st.session_state[id]

# Display chat messages from history on app rerun
for message in prompt_template:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with st.expander('concept 1'):
    # React to user input
    obj_button = st.button("Lesson Objectives")


    try:
        if obj_button:
            prompt = st.chat_input("Type here")
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            if prompt: 
                prompt_template.append({"role": "user", "content": prompt})
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
            else:
                prompt_template.append({"role": "user", "content": "Could you explain the objective briefly in simple language with a plan of how we will learn them"})
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
