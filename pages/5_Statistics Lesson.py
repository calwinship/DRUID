import streamlit as st 
from utils import initialise_openai_client, get_lesson_prompt_template
from config import CONFIG
import json



st.header(':blue[Statistics]')

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

topic = 'statistics2'
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
    st.write("After this week, you should be able to talk about each of the objectives below. You will first go through some interactive webpages and then answer questions. This time the chatbot doesn't have the answer so you need to articulate the information you need. Use the chatbot to ask any generic quesions from the interactive pages, objectives, and questions.")
    st.write("The objectives of this chapter are: ")
    for objective in objectives:
        st.success(f"{objectives[objective]}")
    # st.info()
    # st.write("This is a self-directed lesson meaning you need to extract the information to answer the question and understand the topic. Take notes!")
        # Display chat messages from history on app rerun


with st.expander('Links'):
    st.write("First, go through each of these pages. Some pages have toggle heading at the top. Go through these and think of how you can apply them to the questions later. Write down some interesting observations.")
    link1 = '[The Art of Statistics Home Page](https://artofstat.com/web-apps)'
    link2 = '[The Normal Distribution](https://istats.shinyapps.io/NormalDist/)'
    link3 = '[Binomial Distribution](https://istats.shinyapps.io/BinomialDist/)'
    link4 = '[Sampling Distribution of the Sample Mean](https://istats.shinyapps.io/SampDist_discrete/)'
    link5 = '[Inference for a Population Mean](https://istats.shinyapps.io/Inference_mean/)'
    link6 = '[Inference for a Population Proportion](https://istats.shinyapps.io/Inference_prop/)'   
    
    st.subheader('Two Types of Distributions - Remember the binomial?')
    st.info(link2)
    st.info(link3)
    st.subheader('Using the sample to make guesses about the population')
    st.info(link5)
    st.info(link6)
    st.subheader('The central limit theorem')
    st.info(link4)
    st.subheader('For more, see:')
    st.info(link1)

with st.expander("Q1"):
    st.image("images/Exam17_2_Q8a.png")
    st.image("images/Exam17_2_Q8b.png")

with st.expander("Q2"):
    st.image("images/Exam18_2_Q8.png")

with st.expander("Q3"):
    st.image("images/Exam18_2_Q2a.png")
    st.image("images/Exam18_2_Q2b.png")

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