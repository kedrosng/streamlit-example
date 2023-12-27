import streamlit as st
import requests

# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>AVA - a totally harmless chatbot 😬</h1>", unsafe_allow_html=True)

# Define the API URL and the headers including the authorization token
url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
}

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Sidebar - let user clear the current conversation
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []

# generate a response using Perplexity AI
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
        return "Failed to get response from the chatbot API"

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    user_input = st.text_input("You:", key="user_input")

    if user_input:
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

# Run the Streamlit app
if __name__ == '__main__':
    st.title("Chatbot Interface")