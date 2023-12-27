import streamlit as st
import requests
from streamlit_chat import message  # Make sure this import is correct

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
    
# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>AVA - a totally harmless chatbot 😬</h1>", unsafe_allow_html=True)

# Define the API URL and the headers including the authorization token
url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    # Please make sure to use environment variables or other secure methods to store your API tokens.
    "authorization": "Bearer 668db6b5250a5633e61a031c07aa68f82936234acf0ae677"
}

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Sidebar - let user clear the current conversation
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation")

# Clear the conversation
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []

# Function to generate a response using Perplexity AI
def generate_response(prompt):
    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        st.error("Failed to get response from the chatbot API")
        return ""

# Chat input and button
with st.form(key='chat_form'):
    user_input = st.text_input("You:", key="user_input")
    submit_button = st.form_submit_button(label='Send')

# Handle the chat
if submit_button and user_input:
    output = generate_response(user_input)
    if output:
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

# Display the chat history
if 'generated' in st.session_state and st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

# Always keep the title at the bottom of the code
st.title("Chatbot Interface")