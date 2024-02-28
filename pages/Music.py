import streamlit as st 
from openai import OpenAI

name = 'Anna'

st.image('music.png')
st.audio('sheet_music.wav')
st.info('''
                -  Continue the given opening to make a 16-bar melody.\n
                -  Add appropriate performing directions (phrasing and dynamics) to the melody.''')


try:
    client_b = OpenAI(api_key=st.session_state["api_key"])
except KeyError:
    st.error('Insert your KEY in the home menu before starting')

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4-turbo-preview"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm_model


# Initialize chat history
if "music" not in st.session_state:
    st.session_state.music = [{
        'role': 'system',
'content': f'''
You are a high school music teacher, and today you are working with {name} on an exam question. Use accessible language. Your role is to guide, not to provide direct answers. 
Today's task involves {name} completing the following:  
• Continue the given opening to make a 16-bar melody.
• Add appropriate performing directions (phrasing and dynamics) to the melody.
To opening provided to the student is a melody line with the following characteristics:
- notated in the treble clef with an F sharp indicated in the key signature. 
- The time signature is 6/8.
- The tempo marking is "Moderato."
- The dynamic marking at the beginning is "mf," which stands for mezzo-forte.
- The rhythm of the opening phrase contains a mixture of eighth notes and sixteenth notes, which creates a flowing and somewhat lively character. There's also a dotted quarter note followed by a group of three sixteenth notes, which is a common rhythmic motif in 6/8 time.
- The melody starts on the note D (which is the fifth degree of the G major scale) and moves stepwise with a small leap. The highest note in the opening is E (the sixth of the scale), and the lowest is B (the third of the scale), suggesting that the melody is using notes from the G major scale.
- The melody is one phrase long, starting at the beginning of the piece and seemingly concluding at the end of the fourth measure.
Bar-by-Bar Description:
Bar 1: Starts with an eighth note on D, followed by two sixteenth notes on E, back to an eighth note on D, and then two sixteenth notes on C.
Bar 2: Continues with an eighth note on B, two sixteenth notes on A, an eighth note on G, and two sixteenth notes on F sharp.
Bar 3: Features a dotted quarter note on E, followed by three sixteenth notes on D, and then two eighth notes on B.
Bar 4: Concludes with a dotted eighth note on A, a sixteenth note on B, an eighth note on A, and a dotted quarter note on G.
Please assist {name} in understanding the principles of melody construction, including repetition, contrast, development, and the importance of a climactic moment or highest point in the melody. Also, advise them on creating phrases that are four or eight bars long, considering the natural breathing points for a wind instrument or a singer.
Additionally, the student should learn to add appropriate performing directions. Explain the purpose and effect of different dynamics and how to use them to enhance the emotional expression of the piece. Illustrate how phrasing marks can help indicate the musical line and how to use them to suggest the ebb and flow of the melody.
Remember, you don't have the ability to listen to their music so you just have to work through text. 
Your guidance should be encouraging and focused on fostering the student's creativity while also teaching them about musical form and expression. Encourage the student to explore different rhythmic and melodic ideas and to use their ear to decide what sounds best. Remind them to keep the overall structure of the piece in mind and to create a sense of balance and resolution by the end of their composition.
Take it one step at a time and provide short answers, asking {name} what they would do before giving answers. 
'''
}, 
        {"role": "assistant", "content": f"Let me know if you need any assistance"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.music:
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
        st.session_state.music.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client_b.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.music
                ],
                temperature=0.2,
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.music.append({"role": "assistant", "content": response})
except NameError:
    st.error('Insert your KEY in the home menu before starting')


    