import streamlit as st 
from openai import OpenAI

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam21_2_Q8c.JPG')

tags = {"probability", "bernoulli_trials"}


exam = {
    "questions": { 
                "ci": {"The school caretaker has a box with 23 room keys in it. 12 of the keys are for general classrooms, 6 for science labs and 5 for offices. Four keys are drawn at random from the box. What is the probability that the 4th key drawn is the first office key drawn? Give your answer correct to 4 decimal places."
                },
                "cii": {
                    "question": "All the keys are returned to the box. Then 3 keys are drawn at random from the box one after the other, without replacement. What is the probability that one of them is for a general classroom, one is for a science lab and one is for an office? Give your answer correct to 4 decimal places."
                }
            },
    "solutions": {
        "ci": {
            "solution": "Assuming no replacement: (18/23) * (17/22) * (16/21) * (5/20) = 0.11518... = 0.1152 OR Assuming replacement: (18/23)^3 * (5/23) = 0.10420... = 0.1042"
        },
        "cii": {
            "solution": "((12/23) * (6/22) * (5/21)) * 3! = 0.20327... = 0.2033"
        }
    }
}

question_1 = exam['questions']["ci"]
question_2 = exam['questions']["cii"]

solution_1 = exam['solutions']["ci"] 
solution_2 = exam['solutions']["cii"] 


# Initialize chat history
if "exam6" not in st.session_state:
    st.session_state.exam6 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly pause for {name} to do the work. You are not supposed to give the whole answer or solution away without the student trying first. Instead, get the student to think for themselves. Today, you must ask the student to complete the following question which is made up of multiple parts: 
        {question_1}, then {question_2}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_1}, then {solution_2}. Be very careful when checking the student's answers - always show your work and use the provided solutions to tell if you are right or not. 
        Any answers you give with equations should be enclosed by two dollar signs like so $\binom..$
        '''}, 
        {"role": "assistant", "content": f"Try the question first and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam6:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Enter your answer here")  

# implement logic to cut down input size 


if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.exam6.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam6
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam6.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')