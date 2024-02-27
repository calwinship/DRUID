import streamlit as st 
from openai import OpenAI

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

llm_model = "gpt-3.5-turbo"
# llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam22_2_Q8d.JPG')


tags = {"expected_value", "independent_events"}

exam = {
    "questions": { 
                "di": {"John bought a car a number of years ago. The table provided gives an estimate of the probability that each of the following three events happens to John's car in the next year: Head gasket blows (0.095), Timing belt goes (0.041), Air filters break (0.073). If the head gasket blows, John will have to replace his car, at an estimated cost of €20000. If the head gasket is replaced now, it will cost €1450, and the probability that it blows in the next year will be reduced to 0.005. Is it worth replacing the head gasket now?"
                },
                "dii": {
                    "question": "Calculate the expected cost of not replacing the head gasket now versus the cost of replacing it, taking into account the reduction in the probability of it blowing in the next year to 0.005."
                }
            },
    "solutions": {
        "di": {
            "solution": "Doesn't replace: Expected cost (E(X)) = 0.095(20,000) = 1900. Replaces: E(X) = 1450 + 0.005(20,000) = 1550. Conclusion: He should replace it now as the expected cost is less if he replaces it."
        },
        "dii": {
            "solution": "Probability (P) of at least 1 event happening = 1 - P(none) = 1 - (0.905 * 0.959 * 0.927) = 1 - 0.8045 = 0.19547 ≈ 0.195."
        }
    }
}




question_1 = exam['questions']["di"]
question_2 = exam['questions']["dii"]

solution_1 = exam['solutions']["di"] 
solution_2 = exam['solutions']["dii"] 



# Initialize chat history
if "exam4" not in st.session_state:
    st.session_state.exam4 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of multiple parts: 
        {question_1}, then {question_2}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_1}, then {solution_2}. Be very careful when checking the student's answers.
        Any answers you give with equations should be enclosed by two dollar signs like so $\binom..$
        '''}, 
        {"role": "assistant", "content": f"Try Q8(d) and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam4:
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
    st.session_state.exam4.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam4
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam4.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')