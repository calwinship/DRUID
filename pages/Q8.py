import streamlit as st 
from openai import OpenAI

name = 'Aidan'

st.image('Exam22_2_Q10_A.png')
st.image('Exam22_2_Q10_B.png')
st.image('Exam22_2_Q10_C.png')
st.image('Exam22_2_Q10_D.png')

try:
    client_b = OpenAI(api_key=st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

tags = {"Probability", "Statistics"}

exam = {
    "questions": { 
        "ai": {
            "question": "In an athletics competition, there were a number of heats of the 1500 m race. In the heats, the times that it took the runners to complete the 1500 m were approximately normally distributed, with a mean time of 225 seconds and a standard deviation of 12 seconds. Find the percentage of runners in these heats who took more than 240 seconds to run the 1500 m."
        },
        "aii": {
            "question": "The 20% of runners with the fastest times qualified for the final. Assuming the race times were normally distributed as described above, work out the time needed to qualify for the final, correct to the nearest second."
        },
        "b": {
            "question": "Sally takes part in a number of different races in the competition. The probability that she makes a false start in any given race is 5%. Find the probability that she makes her first false start in her fourth race. Give your answer correct to 4 decimal places."
        },
        "c": {
            "question": "20 relay teams took part in the competition. For any particular team, the probability that they drop the baton at some point during the competition is 0.1. Find the probability that at most 2 teams drop the baton during the competition. Give your answer correct to 4 decimal places."
        },
        "d": {
            "question": "300 runners take part in a road race. Each runner has a number, from 1 to 300 inclusive. No two runners have the same number. Two runners are picked at random from the runners in this race. Work out the probability that the sum of their numbers is 101. Give your answer as a fraction in its simplest form."
        }
    },
    "solutions": {
        "ai": {
            "solution": "𝑧 = (240-225) / 12 = 15 / 12 = 1.25, 𝑃(𝑥 > 240) = 𝑃(𝑧 > 1.25) = 1 − 𝑃(𝑧 < 1.25) = 1 − 0.8944 = 0.1056. Answer: 10.56%"
        },
        "aii": {
            "solution": "Look up 𝑃=0.8: 𝑧=0.84 or 0.85. Time=(225 - x)/12 = 0.84. So Time= 225 − 0.84(12) = 214.92. Or Time = 225 − 0.85(12) = 214.8. Accept time = 214 [secs] or 215 [secs]."
        },
        "b": {
            "solution": "1 − 0.05 = 0.95. 𝑃 = 0.95 × 0.95 × 0.95 × 0.05 = 0.04286 ... = 0.0429 [4 D.P.]"
        },
        "c": {
            "solution": "𝑃(at most 2) = 𝑃(0 or 1 or 2) = 𝑃(0) + 𝑃(1) + 𝑃(2) = 0.9^20 + 20C1 * 0.1 * 0.9^19 + 20C2 * 0.1^2 * 0.9^18 = 0.12157 ... + 0.27017 ... + 0.28517 ... = 0.67692 ... = 0.6769 [4 D.P.]"
        },
        "d": {
            "solution": "50 possible pairs of numbers add to 101: 1+100, 2+99, ..., 50+51. 300C2 = 44850 pairs in total. So 𝑃 = 50/44850 = 1/897. OR 100 different 1st numbers could be picked; for each, only one 2nd number will give 101: 𝑃 = (100/300) * (1/299) = 1/897."
        }
    }
}


question_1 = exam['questions']["ai"]
question_2 = exam['questions']["aii"]
question_3 = exam['questions']["b"]
question_4 = exam['questions']["c"]
question_5 = exam['questions']["d"]

solution_1 = exam['solutions']["ai"] 
solution_2 = exam['solutions']["aii"] 
solution_3 = exam['solutions']["b"]
solution_4 = exam['solutions']["c"]
solution_5 = exam['solutions']["d"]


# Initialize chat history
if "exam6" not in st.session_state:
    st.session_state.exam6 = [{
        'role': 'system',
'content': f'''
You are a high school math teacher, and today you are working with {name} on a maths question. Use accessible language. Your role is to guide, not to provide direct answers. 
Today's task involves completing: {question_1}, followed by {question_2}, , followed by {question_3}, , followed by {question_4}, , followed by {question_5}.
If {name} doesn't get an answer correct or asks for help, encourage them to share their thoughts on approaching the problem before diving into the specifics. guide them with hints if they are stuck or request assistance.
Do not reveal the answers straight away; instead, foster an environment where {name} is motivated to find the solutions independently. After each attempt, whether correct or incorrect, engage in a constructive discussion to understand {name}'s thought process. This approach will help identify misconceptions and areas for improvement. 
If an error is made, encourage {name} to analyze and understand the mistake before moving forward. Use short messages and regularly ask for confirmation that {name} understands.
Upon completing all questions, ask {name} to reflect on the learning experience and the strategies that led to a solution. This reflective practice reinforces learning and builds problem-solving skills. 
Remember, the goal is not just to reach the correct answers, but to cultivate a deep understanding and appreciation for the problem-solving process. Answers and solutions are provided for your reference as {solution_1} and {solution_2} and {solution_3} and {solution_4} and {solution_5}. Use them judiciously to verify correctness and provide guidance when absolutely necessary. 
All equations and mathematical expressions should be enclosed within two dollar signs ($$) to ensure clarity, for example $\frac...$. 
If you need to perform a calculation and need help from a python interpreter, enclose the python code in >>> and <<< like so >>>2 + 2<<<. You have access to NumPy and Sympy. You will get the answer in a follow-up prompt. 
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


    