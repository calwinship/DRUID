import streamlit as st 
from openai import OpenAI

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam20_2_Q5.JPG')

tags = {"probability", "conditional_probability"}

exam = {
    "questions": {
        "ai": {
            "Two events A and B are such that P(A) = 3/4 and P(A ∩ B) (Probability of A intersection B) = 1/2. Find 𝑃(𝐵|𝐴) (Probability of B given A). Give your answer as a fraction in its simplest form."
        },
        "aii": {
            "𝑃(𝐴∪𝐵) (Probability of A union B) = 11/12. Investigate if the events 𝐴 and 𝐵 are independent. "
        }
    },
    "solutions": {
        "ai": {
            "𝑃(𝐵|𝐴) (Probability of B given A) = P(A ∩ B) (Probability of A intersection B)/by P(A) = 2/3"
        },
        "aii": {
            "𝑃(𝐴∪𝐵) = P(A) + P(B) -  P(A ∩ B); 11/12 = (3/4) + P(B) -1/2; P(B) = 2/3; Check if P(A)*P(B)=P(A ∩ B); it does so they are independent."
        }
    }
}





question_1 = exam['questions']["ai"]
question_2 = exam['questions']["aii"]

solution_1 = exam['solutions']["ai"] 
solution_2 = exam['solutions']["aii"] 

# Initialize chat history
if "exam7" not in st.session_state:
    st.session_state.exam7 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of multiple parts: 
        {question_1}, then {question_2}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_1}, then {solution_2}. Be very careful when checking the student's answers and when explaining, work through your answers.
        '''}, 
        {"role": "assistant", "content": f"Try Q5(a) and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam7:
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
    st.session_state.exam7.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam7
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam7.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')