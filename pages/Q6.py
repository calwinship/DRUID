import streamlit as st 
from openai import OpenAI

name = 'Aidan'

client_b = OpenAI(api_key=st.session_state["api_key"])

llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model

st.image('Exam22_2_Q8ai.JPG')
st.image('Exam22_2_Q8aii.JPG')


tags = {"scatter_plot", "correlation_coefficient"}

mpg_data = {
            "A": {"City (m/g)": 22, "Motorway (m/g)": 34},
            "B": {"City (m/g)": 27, "Motorway (m/g)": 38},
            "C": {"City (m/g)": 24, "Motorway (m/g)": 34},
            "D": {"City (m/g)": 16, "Motorway (m/g)": 27},
            "E": {"City (m/g)": 15, "Motorway (m/g)": 24},
            "F": {"City (m/g)": 21, "Motorway (m/g)": 30},
            "G": {"City (m/g)": 30, "Motorway (m/g)": 40},
            "H": {"City (m/g)": 17, "Motorway (m/g)": 30}}

exam = {
    "questions": { 
                "ai": {"Jena is researching fuel consumption in cars. She finds the data (not given to you as an LLM but available to the student) for the number of miles per gallon (m/g) for eight different cars, labelled A to H, when driving in the city and on the motorway. The scatterplot provided to the student shows this data for cars A to F. Using the data in the table, plot and label points to represent cars G and H on the scatterplot."
                },
                "aii": {
                    "question": "On the scatterplot, draw the line of best fit for the data, by eye. "
                }, 
                "aiii": {
                    "question": "Two other cars, K and L, have the miles per gallon values given in the following table (not given to you as an LLM but available to the student). Use your line of best fit on the scatterplot to fill in an estimate for each of the two missing values in the table below. Show your work on the scatterplot."
                }, 
                "aiv": {
                    "question": "Based on the data given, would you be more confident in the value you estimated for K or for L? Give a reason for your answer"
                },
                "av": {
                    "question": "Find the value of r, the correlation coefficient between city and motorway miles per gallon. Use only the values for the 8 cars A to H in the table. Give your answer correct to 3 decimal places."
                } 
            },
    "solutions": { 
                "ai": {"G and H plotted and labelled correctly"
                },
                "aii": {
                    "question": "Reasonable line of best fit drawn"
                }, 
                "aiii": {
                    "question": "Answers consistent with candidate’s line of best fit - K should be between 25-40, L should be between 35-55"
                }, 
                "aiv": {
                    "question": "Answer: K, Reason: L is well beyond all of the given data points"
                },
                "av": {
                    "question": "0∙9659 … = 0∙966 "
                } 
            }
}




question_1 = exam['questions']["ai"]
question_2 = exam['questions']["aii"]
question_3 = exam['questions']["aiii"]
question_4 = exam['questions']["aiv"]
question_5 = exam['questions']["av"]

solution_1 = exam['solutions']["ai"] 
solution_2 = exam['solutions']["aii"] 
solution_3 = exam['solutions']["aiii"]
solution_4 = exam['solutions']["aiv"]
solution_5 = exam['solutions']["av"]


# Initialize chat history
if "exam2" not in st.session_state:
    st.session_state.exam2 = [{
        'role': 'system',
        'content': f'''
        You are a high school math teacher, and today you are examining {name} on a maths question. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Today, you must ask the student to complete the following question which is made up of multiple parts: 
        {question_1}, then {question_2}, then {question_3}, then {question_4}, then {question_5}. Don't give the student the answer and solution straight away. Instead encourage {name} to find the answer on their own. Take it one part of the question at a time and then summarise once all are complete. The answers are {solution_1}, then {solution_2}, then {solution_3}, then {solution_4}, then {solution_5} Be very careful when checking the student's answers.
        '''}, 
        {"role": "assistant", "content": f"Try Q1(a) and let me know what you get."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.exam2:
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
    st.session_state.exam2.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client_b.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.exam2
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.exam2.append({"role": "assistant", "content": response})


if st.session_state["api_key"] == 0:
    st.error('Insert your API KEY in the home menu before starting')