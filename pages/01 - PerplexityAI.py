import streamlit as st
import requests
import datetime

# Set page config
st.set_page_config(page_title="Perplexity AI (Paid)", page_icon=":robot:")

# Define API endpoint and headers
url = "https://api.perplexity.ai/chat/completions"
headers = {"authorization": "Bearer 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"}

# Define models and descriptions
models = ["sonar-small-chat", "sonar-small-online", "sonar-medium-chat", "sonar-medium-online", "codellama-34b-instruct", "codellama-70b-instruct", "llama-2-70b-chat", "mistral-7b-instruct", "mixtral-8x7b-instruct", "pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online"]

# Set page title and icon
st.header("Perplexity AI (Paid)")

# Set initial session state
if "model" not in st.session_state:
    st.session_state["model"] = "pplx-7b-online"
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

# Create columns for input and messages
col1, col2 = st.beta_columns([1, 5])

# Display chat messages in a scrollable container
with col2:
    messages_container = st.beta_container()
    for i, message in enumerate(st.session_state["messages"]):
        with messages_container.chat_message(message["role"]):
            st.markdown(message["content"])

# Display user input and assistant response
with col1:
    user_input = st.text_input("Type your message here...", key="user_input")
    submit_button = st.button("Send", key="submit")

    if submit_button and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with messages_container.chat_message("assistant"):
            response_loading = st.spinner("Loading response...")
            try:
                # Send a POST request to the API and get the response
                api_response = requests.post(url, json={
                    "model": st.session_state["model"],
                    "messages": st.session_state["messages"],
                    "temperature": 0.5
                }, headers=headers).json()

                # Extract the content from the response
                response_content = api_response["choices"][0]["message"]["content"]

                # Append the response content to the messages in the session state
                st.session_state["messages"].append({"role": "assistant", "content": response_content})
            except Exception as e:
                st.error(f"Error fetching response from API: {str(e)}")
            finally:
                try:
                    response_loading.empty()
                except Exception as e:
                    st.error(f"Error when trying to remove the loading spinner: {str(e)}")

# Display message count and timestamp
message_count = len(st.session_state["messages"])
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**{message_count} messages** | {current_time}")

# Add clear chat button
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.session_state["system_prompt"] = ""
