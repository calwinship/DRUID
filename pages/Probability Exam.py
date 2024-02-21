import streamlit as st 
from openai import OpenAI
# from dotenv import load_dotenv
import datetime

st.title('Probability Exam')

name = 'Callum'
interests = ['football', 'cars', 'planes']

# load_dotenv()

client_b = OpenAI(api_key=st.session_state["api_key"])

current_date = datetime.datetime.now().date()
# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-4"
else:
    llm_model = "gpt-3.5-turbo-0301"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('ProbExamQ1.JPG')
st.image('ProbExamQ1b.JPG')
st.image('ProbExamQ1c.JPG')


exam = {
    "questions": {
        "1": {
            "text": "A circular spinner has 12 sectors, as follows: 5 sectors are labelled €6, 3 sectors are labelled €9, the rest are labelled €0. In a game, the spinner is spun once. The spinner is equally likely to land on each sector. The player gets the amount of money shown on the sector that the spinner lands on.",
            "parts": {
                "a": "Fiona plays the game a number of times. Work out the probability that Fiona gets €6, then €9, then €6 the first three times she plays. Give your answer correct to 4 decimal places.",
                "b": "Rohan also plays the game a number of times. Find the probability that Rohan gets €9 for the 3rd time, on the 8th time that he plays the game. Give your answer correct to 4 decimal places.",
                "c": "Olga plays the game 2 times. Find the probability that Olga gets less than €16 in total from playing the game. Give your answer correct to 4 decimal places."
            }
        }
    },
    "solutions": {
        "1": {
            "a": {
                "answer": "0.0434",
                "calculation": "P(€6, €9, €6) = (5/12) * (3/12) * (5/12) = 0.0434 to 4 decimal places."
            },
            "b": {
                "answer": "0.0779",
                "calculation": "2 successes in first 7 spins and then success = ((7 choose 2) * (1/4)^3 * (3/4)^4) * 1/4 = 0.0779 to 4 decimal places."
            }, 
            "c": {
                "answer": "0 ∙ 9375",
                "calculation": "Will get less than €16 unless 9, 9, so: 1 - P(9,9) = 1 - 1/4 * 1/4 = 135/144 or 15/16"
            }
        }
    },
    "marking_scheme": {
        "1": {
            "a": {
                "scale": [0, 4, 7, 10],
                "criteria": {
                    "low_partial_credit": "Any correct relevant probability stated.",
                    "high_partial_credit": "P(€6) = 5/12 and P(€9) = 3/12 and some multiplication indicated.",
                    "full_credit_minus_one": "Incorrect rounding or no rounding."
                }
            },
            "b": {
                "scale": [0, 3, 5, 8, 10],
                "criteria": {
                    "low_partial_credit": "P(success) = 1/4, P(failure) = 3/4, and correct use of binomial coefficient for the last success.",
                    "mid_partial_credit": "Product of two or three correct terms evaluated.",
                    "high_partial_credit": "Correct calculation involving the product of all four terms: binomial coefficient, P(success) for the 3rd success, and P(failure) for the other spins.",
                    "full_credit_minus_one": "Incorrect rounding or no rounding."
                }
            }, 
            "c": {
                "scale": [0, 3, 5, 8, 10],
                "criteria": {
                    ### not complete
                }
            }
        }
    }
}


question_a = exam['questions']['1']['text'] + exam['questions']['1']['parts']['a']
solution_a = exam['solutions']['1']['a'] 
marking_scheme_a = exam['marking_scheme']['1']['a'] 
question_b = exam['questions']['1']['parts']['b']
solution_b = exam['solutions']['1']['b'] 
question_c = exam['questions']['1']['parts']['c']
solution_c = exam['solutions']['1']['c'] 

# Initialize chat history
if "exams" not in st.session_state:
    st.session_state.exams = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a probability question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of three parts: 
        {question_a}, then {question_b}, then {question_c}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. The respective solutions are {solution_a}, then {solution_b}, then {solution_c}. Be very careful when checking the student's answers. Take it one part of the question at a time and then summarise once all are complete.  
        '''}, 
        {"role": "assistant", "content": f"Try Q1(a) and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exams:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Enter your answer here")  

if prompt and prompt.lower() == 'solution a':
    st.text(solution_a)

if prompt and prompt.lower() == 'solution b':
    st.text(solution_a)

if prompt and prompt.lower() == 'solution c':
    st.text(solution_a)


elif prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.exams.append({"role": "user", "content": prompt})

    
    # Display assistant response in chat message container
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exams
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exams.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')