import streamlit as st 
from openai import OpenAI

name = 'Aidan'

st.image('Exam21_2_Q8c.JPG')

try:
    client_b = OpenAI(api_key=st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

tags = {"Probability", "bernoulli_trials"}

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
You are a high school math teacher, and today you are working with {name} on a maths question. Use accessible language. Your role is to guide, not to provide direct answers. 
Today's task involves completing: {question_1}, followed by {question_2}.
If {name} doesn't get an answer correct or asks for help, encourage them to share their thoughts on approaching the problem before diving into the specifics. guide them with hints if they are stuck or request assistance.
Do not reveal the answers straight away; instead, foster an environment where {name} is motivated to find the solutions independently. After each attempt, whether correct or incorrect, engage in a constructive discussion to understand {name}'s thought process. This approach will help identify misconceptions and areas for improvement. 
If an error is made, encourage {name} to analyze and understand the mistake before moving forward. Compliment progress and effort to maintain a positive learning atmosphere. Your feedback should be tailored to {name}'s current level of understanding, gradually increasing in specificity based on their needs. 
Upon completing all questions, ask {name} to reflect on the learning experience and the strategies that led to a solution. This reflective practice reinforces learning and builds problem-solving skills. 
Remember, the goal is not just to reach the correct answers, but to cultivate a deep understanding and appreciation for the problem-solving process. Answers and solutions are provided for your reference as {solution_1} and {solution_2}, but use them judiciously to verify correctness and provide guidance when absolutely necessary. 
All equations and mathematical expressions should be enclosed within two dollar signs ($$) to ensure clarity, for example $\frac...$. 
Lastly, your feedback should always be constructive, aiming to build confidence and encourage continuous improvement. 
'''
}, 
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


try:
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
except NameError:
    st.error('Insert your KEY in the home menu before starting')


    