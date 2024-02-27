import streamlit as st 
from openai import OpenAI

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

llm_model = "gpt-3.5-turbo"
# llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam22_2_Q1ai.JPG')
st.image('Exam22_2_Q1aii.JPG')
st.image('Exam22_2_Q1b.JPG')
st.image('Exam22_2_Q1c.JPG')


tags = {"probability", "independent_events"}

exam = {
    "questions": { 
        "ai": { "question":
         '''(a) The table below gives some details on the number of different types of student in a university. There are 22714 students in the university in total.
            
                {
                    "table": {
                        "Age_Years": {
                            "Total": 22714,
                            "23_or_younger": None,
                            "24_or_older": 8576
                        },
                        "Students": {
                            "Undergraduate": {
                                "23_or_younger": 12785,
                                "24_or_older": 2922,
                                "Total": 15707
                            },
                            "Postgraduate": {
                                "23_or_younger": 1353,
                                "24_or_older": None,
                                "Total": None
                            }
                        }
                    }
                    
                    question: Fill in the three missing values to complete the table.
                '''
                },
                "aii": {
                    "question": "One student is picked at random from the students in the university. Let O be the event that the student is 24 years old, or older. Let U be the event that the student is an undergraduate. Are the events O and U independent? Justify your answer."
                }, 
                "b": {
                    "question": "Three people are picked at random from a class. Find the probability that all three were born on the same day of the week. Assume that the probability of being born on each day is the same."
                }, 
                "c": {
                    "question": "There are b boys and g girls in a class, where b and g are natural numbers. 3/5 of the students in the class are girls. 4 boys and 4 girls join the class. One student is then picked at random from the whole class. The probability that this student is a girl is now 4/7. Find the value of b and the value of g."
                } 
            },
    "solutions": {
            "ai": {
                "answer": {
                    "23_or_younger": 14138,
                    "24_or_older": 5654,
                    "Total": 7007
                }, 
            },
            "aii": {
                "answer": "They are not independent"
            }, 
            "b": {
                "answer": "1/49 = 0.0204"
            }, 
            "c": {
                "answer": "b = 8, g=12"
            }
        }
}


question_ai = exam['questions']["ai"]
question_aii = exam['questions']["aii"]
question_b = exam['questions']["b"]
question_c = exam['questions']["c"]

solution_ai = exam['solutions']["ai"] 
solution_aii = exam['solutions']["aii"] 
solution_b = exam['solutions']["b"]
solution_c = exam['solutions']["c"]


# Initialize chat history
if "exam1" not in st.session_state:
    st.session_state.exam1 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of three parts: 
        {question_ai}, then {question_aii}, then {question_b}, then {question_c}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_ai}, then {solution_aii}, then {solution_b}, then {solution_c} Be very careful when checking the student's answers.
        Any answers you give with equations should be enclosed by two dollar signs like so $\binom..$
        '''}, 
        {"role": "assistant", "content": f"Try Q1(a) and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam1:
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
    st.session_state.exam1.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam1
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam1.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')