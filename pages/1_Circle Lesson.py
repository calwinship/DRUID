import streamlit as st 
from utils import initialise_openai_client, get_lesson_prompt_template
from config import CONFIG
import json



st.header(':blue[The Circle]')

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

topic = 'circle1'
objective = 'a'
id = f"{topic}{objective}"

# link to the questions database 
json_file_path = 'data/lessons_repo.json'
with open(json_file_path, 'r') as f:
    file = json.load(f)
objectives = file[topic]['objectives']#[objective]
# images =  exam['images']

# for image in images:
#     st.image(image)


if id not in st.session_state:
    st.session_state[id] = get_lesson_prompt_template(id, name, objectives)
prompt_template = st.session_state[id]

prompt = st.chat_input("Type here")

with st.expander('Objectives'):
    st.write("After this week, you should be able to talk about each of the objectives below. Read them now and come back to make sure you understand them at the end. Use the chatbot to guide your learning through each objective.")
    st.write("The objectives of this chapter are: ")
    for objective in objectives:
        st.success(f"{objectives[objective]}")
    # st.info()
    # st.write("This is a self-directed lesson meaning you need to extract the information to answer the question and understand the topic. Take notes!")
        # Display chat messages from history on app rerun


with st.expander('Tasks'):
    st.info("Task 1: Go through [The Circle Lesson](https://thirdspacelearning.com/gcse-maths/geometry-and-measure/equation-of-a-circle/). Write down the answers for each question.")
    st.info("Task 2: Reproduce the images below with [Geogebra](https://www.geogebra.org/calculator). Write down the answers for each question.")
    st.image("images/circle1.png")
    st.image("images/circle2.png")
    st.image("images/circle3.png")
    st.image("images/circle4.png")
    st.image("images/circle5.png")
    st.image("images/circle6.png")



with st.expander("Q1"):
    st.write("Give this question a go if you have time. Send all work, including from the questions above.")
    st.image("images/Exam23_2_Q4a.png")
    st.image("images/Exam23_2_Q4b.png")

with st.expander("Q2"):
    st.write("Give this question a go if you have time. Send all work, including from the questions above.")
    st.image("images/Exam22_2_Q3a")
    st.image("images/Exam22_2_Q3b")

# with st.expander("Q2"):
#     st.image("images/Exam18_2_Q8.png")

# with st.expander("Q3"):
#     st.image("images/Exam18_2_Q2a.png")
#     st.image("images/Exam18_2_Q2b.png")

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