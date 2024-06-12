import streamlit as st
import hmac

st.image('logos/logo_trans_2.png')

st.write(''' \n\n\n\n\n
            
            
            DRUID is an AI-powered personal tutor.\n\nNow. Every student can have access to a personalised learning experience to help them fulfil their potential.
        
        '''
            
            )

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            st.session_state["api_key"] = st.secrets["openai_api_key"]
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.
else:
    st.info(' \nPassword Correct - Now get started with one of the lessons or exam questions on the left.')




# openai_api_key = st.text_input('Enter your key to get started', key="chatbot_api_key", type="password")

  

# if openai_api_key:
#     st.session_state["api_key"] = openai_api_key
#     st.info(' \nGreat - Now get started with one of the lessons or exam questions on the left.')




