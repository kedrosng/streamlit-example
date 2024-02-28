import streamlit as st
import requests
import datetime

# Set page config
st.set_page_config(page_title="Perplexity AI Chatbot", page_icon=":robot:")

# Define API endpoint and headers
url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": "Bearer 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"}

# Define models for selection
models = [
    "sonar-small-chat", "sonar-small-online", "sonar-medium-chat", "sonar-medium-online",
    "codellama-34b-instruct", "codellama-70b-instruct", "llama-2-70b-chat", "mistral-7b-instruct",
    "mixtral-8x7b-instruct", "pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online"
]

# Page title
st.header("Perplexity AI Chatbot")

# Model selection dropdown
selected_model = st.selectbox("Select Model", models)

# User message input
user_input = st.text_input("Type your message here...")

# Send button
submit_button = st.button("Send")

# Initialize session state for messages if not already done
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send message to API and get response
def send_message(model, user_message):
    try:
        response = requests.post(url, json={
            "model": model,
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.5
        }, headers=headers).json()
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Handle send button click
if submit_button and user_input:
    # Append user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Send message to API and get response
    response_content = send_message(selected_model, user_input)
    
    # Append response to session state
    st.session_state["messages"].append({"role": "assistant", "content": response_content})

# Display messages
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.text_area("You", value=message["content"], height=100, disabled=True)
    elif message["role"] == "assistant":
        st.text_area("Assistant", value=message["content"], height=100, disabled=True)

# Display message count and timestamp
message_count = len(st.session_state["messages"])
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**{message_count} messages** | {current_time}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state["messages"] = []