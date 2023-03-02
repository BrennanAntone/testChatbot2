# To run in terminal:
# streamlit run chatbot.py
# To close: control C
# right click in terminal window

# V3: adding

# Example use of parameters embedded through url
# https://brennanantone-testchatbot2-chatbot2-aqz2vq.streamlit.app/?username=Noshir&userid=789
# username is for display on the webpage
# userid is for storage of messages in a database


# Import the libraries
import openai
import streamlit as st
# import streamlit_chat
from streamlit_chat import message
import calendar
# core python module
from datetime import datetime # core python module
import database as db # local import

openai.api_key = st.secrets['OPENAI_SECRET']
#openai.api_key = OPENAI_SECRET

# -------------- SETTINGS --------------
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
currency = "USD"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


def get_param(param_name):
    # Get parameter from a url
    query_params = st.experimental_get_query_params()
    try:
        return query_params[param_name][0]
    except:
        st.write('Parameter is missing')
        return False


def generate_response(prompt):
    # Get OpenAI response to prompt
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    ai_message = completions.choices[0].text
    return ai_message


# Creating the chatbot interface
username = get_param('username')
userid = get_param('userid') # Get from url
my_title = "Vero: An AI teammate for " + str(username)
st.title(my_title)
st.write('This version of Vero has been personalized with knowledge and speech patterns designed to assist you on ' +
         'brainstorming and creative thinking tasks.')

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    # Gets text input by the user
    input_text = st.text_input("You: ", "Hello Vero, are you ready to collaborate?", key="input")
    return input_text


user_input = get_text()

if user_input:
    output = generate_response(user_input)
    # store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
