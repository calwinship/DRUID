import streamlit as st 
from openai import OpenAI

#st.title('Exam')

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

llm_model = "gpt-3.5-turbo"
# llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam21_2_Q1a.JPG')
st.image('Exam21_2_Q1c.JPG')


tags = {"probability", "bernoulli_trial"}

exam = {
    "questions": {
        "a": {
            "text": "In a particular population 15% of the people are left footed. A soccer team of 11 players, including 1 goalkeeper, is picked at random from the population. Find the probability that there is exactly one left footed player on the team. Give your answer correct to three decimal places."
        },
        "b": {
            "text": "Find the probability that less than three players on the team are left footed. Give your answer correct to two decimal places."
        },
        "c": {
            "text": "The goalkeeper is left footed. Find the probability that at least eight of the remainder of the team are right footed. Give your answer correct to two decimal places."
        }
    },
    "solutions": {
        "a": {
            "text": "11 x 0·15 x 0·85^10 = 0.3248 = 0.325 OR 11 x 3/20 x (17/20)^10 = 0.3848 = 0.325"
        },
        "b": {
            "text": "P(0 or 1 or 2 left-footed) = 0·85^10 + 11C1 x 0.15 x 0.85^10 + 11C2 x 0.15^2 x 0.85^9 = 0.1673 + 0.3248 + 0.2866 = 0.7787 = 0.78"
        },
        "c": {
            "text": "From 10, P(0 or 1 or 2 left-footed) = 0·85^10 + 10C1 x 0.15 x 0.85^9 + 10C2 x 0.15^2 x 0.85^8 = 0.1968 + 0.3474 + 0.2758 = 0.8200 = 0.82"
        }
    }
}


question_1 = exam['questions']["a"]
question_2 = exam['questions']["b"]
question_3 = exam['questions']["c"]

solution_1 = exam['solutions']["a"] 
solution_2 = exam['solutions']["b"] 
solution_3 = exam['solutions']["c"]

# Initialize chat history
if "exam5" not in st.session_state:
    st.session_state.exam5 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of multiple parts: 
        {question_1}, then {question_2}, then {question_3}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_1}, then {solution_2}, then {solution_3}. Be very careful when checking the student's answers and when explaining, work through your answers.
        Any answers you give with equations should be enclosed by two dollar signs like so $\binom..$
        '''}, 
        {"role": "assistant", "content": f"Try the question first and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam5:
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
    st.session_state.exam5.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam5
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam5.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')