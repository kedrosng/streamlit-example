import streamlit as st
import requests
import datetime

# Set page config
st.set_page_config(page_title="Perplexity AI (Paid)", page_icon=":robot:")

# Define API endpoint and headers
url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": "Bearer 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"}

# Define models
models = [
    "sonar-small-chat", "sonar-small-online", "sonar-medium-chat", "sonar-medium-online",
    "codellama-34b-instruct", "codellama-70b-instruct", "llama-2-70b-chat", "mistral-7b-instruct",
    "mixtral-8x7b-instruct", "pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online"
]

# Set page title and icon
st.header("Perplexity AI (Paid)")

# Set initial session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""

# Display model selection dropdown and description
selected_model = st.selectbox("Select Model", models)

# Display system prompt input
system_prompt = st.text_input("System Prompt (optional)", value=st.session_state["system_prompt"], key="system_prompt")

# Add system prompt to messages if it's not already there
if system_prompt and not any(m["role"] == "system" for m in st.session_state["messages"]):
    st.session_state["messages"].insert(0, {"role": "system", "content": system_prompt})

# Display chat messages
for i, message in enumerate(st.session_state["messages"]):
    if message["role"] == "user":
        st.text_area("You", value=message["content"], height=100, key=f"user_{i}")
    elif message["role"] == "assistant":
        st.text_area("Assistant", value=message["content"], height=100, key=f"assistant_{i}")

# Display user input and assistant response
user_input = st.text_input("Type your message here...", key="user_input")
submit_button = st.button("Send", key="submit")

if submit_button and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    try:
        # Send a POST request to the API and get the response
        api_response = requests.post(url, json={
            "model": selected_model,
            "messages": st.session_state["messages"],
            "temperature": 0.5
        }, headers=headers).json()

        # Extract the content from the response
        response_content = api_response["choices"][0]["message"]["content"]

        # Append the response content to the messages in the session state
        st.session_state["messages"].append({"role": "assistant", "content": response_content})
    except Exception as e:
        st.error(f"Error fetching response from API: {str(e)}")

# Display message count and timestamp
message_count = len(st.session_state["messages"])
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**{message_count} messages** | {current_time}")

# Add clear chat button
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.session_state["system_prompt"] = ""
