import streamlit as st 
from openai import OpenAI

name = 'Aidan'

st.image('Exam22_2_Q5_B.png')

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
        "b": {
            "In 2019, people with a pre-pay mobile phone plan spent an average (mean) of €20.79 on their mobile phone each month (source: www.comreg.ie). In 2021, some students carried out a survey to see if this figure had changed. They surveyed a random sample of 500 people with pre-pay mobile phone plans. For this sample, the mean amount spent per month was €22.16 and the standard deviation was €8.12. Carry out a hypothesis test at the 5% level of significance to see if this shows a change in the mean monthly spend on mobile phones for people with a pre-pay plan. State your null hypothesis and your alternative hypothesis, state your conclusion, and give a reason for your conclusion."
        }
    },
    "solutions": {
        "b": {
            "Null Hypothesis: Average [mean] amount has not changed. Alternative Hypothesis: Average [mean] amount has changed. Conclusion: The average amount has changed. Calculations & Reason: 𝑧 = (22.16 - 20.79) / (8.12 / sqrt(500)) = 3.7726 ..., which is greater than 1.96 OR 20.79 ± 1.96 * (8.12 / sqrt(500)) = [20.07.., 21.51..], and 22.16 lies outside this range OR 22.16 ± 1.96 * (8.12 / sqrt(500)) = [21.44.., 22.87...], and 20.79 lies outside this range."
        }
    }
}


question_1 = exam['questions']["b"]

solution_1 = exam['solutions']["b"] 

# Initialize chat history
if "exam9" not in st.session_state:
    st.session_state.exam9 = [{
        'role': 'system',
'content': f'''
You are a high school math teacher, and today you are working with {name} on a maths question. Use accessible language. Your role is to guide, not to provide direct answers. 
Today's task involves completing: {question_1}.
If {name} doesn't get an answer correct or asks for help, encourage them to share their thoughts on approaching the problem before diving into the specifics. guide them with hints if they are stuck or request assistance.
Do not reveal the answers straight away; instead, foster an environment where {name} is motivated to find the solutions independently. After each attempt, whether correct or incorrect, engage in a constructive discussion to understand {name}'s thought process. This approach will help identify misconceptions and areas for improvement. 
If an error is made, encourage {name} to analyze and understand the mistake before moving forward. Use short messages and regularly ask for confirmation that {name} understands.
Upon completing all questions, ask {name} to reflect on the learning experience and the strategies that led to a solution. This reflective practice reinforces learning and builds problem-solving skills. 
Remember, the goal is not just to reach the correct answers, but to cultivate a deep understanding and appreciation for the problem-solving process. Answers and solutions are provided for your reference as {solution_1}, but use them judiciously to verify correctness and provide guidance when absolutely necessary. 
All equations and mathematical expressions should be enclosed within two dollar signs ($$) to ensure clarity, for example $\frac...$. 
If you need to perform a calculation and need help from a python interpreter, enclose the python code in >>> and <<< like so >>>2 + 2<<<. You have access to NumPy and Sympy. You will get the answer in a follow-up prompt. 
'''
}, 
        {"role": "assistant", "content": f"Try the question first and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam9:
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
        st.session_state.exam9.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client_b.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.exam9
                ],
                temperature=0.2,
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.exam9.append({"role": "assistant", "content": response})
except NameError:
    st.error('Insert your KEY in the home menu before starting')


    