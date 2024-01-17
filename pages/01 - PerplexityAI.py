import streamlit as st
import requests
import datetime

# Set page config
st.set_page_config(page_title="Perplexity AI (Paid)", page_icon=":robot:")

# Define API endpoint and headers
url = "https://api.perplexity.ai/chat/completions"
headers = {"authorization": "Bearer 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"}

# Define models and descriptions
models = [
    {"name": "pplx-7b-online", "description": "7B parameter model trained on a diverse range of internet text."},
    {"name": "pplx-70b-chat", "description": "70B parameter model fine-tuned for chat."},
    {"name": "pplx-7b-chat", "description": "7B parameter model fine-tuned for chat."},
    {"name": "pplx-70b-online", "description": "70B parameter model trained on a diverse range of internet text."},
    {"name": "llama-2-70b-chat", "description": "70B parameter model fine-tuned for chat by Mistral AI."},
    {"name": "codellama-34b-instruct", "description": "34B parameter model fine-tuned for instruction following by Mistral AI."},
    {"name": "mistral-7b-instruct", "description": "7B parameter model fine-tuned for instruction following by Mistral AI."},
    {"name": "mixtral-8x7b-instruct", "description": "8x7B parameter model ensemble fine-tuned for instruction following by Mistral AI."}
]

# Set page title and icon
st.header("Perplexity AI (Paid)")

# Set initial session state
if "model" not in st.session_state:
    st.session_state["model"] = models[0]["name"]
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""

# Display model selection dropdown and description
selected_model = st.selectbox("Select Model", [m["name"] for m in models], index=0)
model_description = models[models.index({"name": selected_model})]["description"]
st.markdown(f"**{selected_model}** - {model_description}")

# Display system prompt input
system_prompt = st.text_input("System Prompt (optional)", value=st.session_state["system_prompt"], key="system_prompt")

# Add system prompt to messages if it's not already there
if system_prompt and not any(m["role"] == "system" for m in st.session_state["messages"]):
    st.session_state["messages"].insert(0, {"role": "system", "content": system_prompt})

# Display chat messages
for i, message in enumerate(st.session_state["messages"]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display user input and assistant response
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        response_loading = st.spinner("Loading response...")
        try:
            response = requests.post(url, json={
                "model": st.session_state["model"],
                "messages": st.session_state["messages"],
                "temperature": 0.5
            }, headers=headers).json()["choices"][0]["message"]["content"]
            st.session_state["messages"].append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error fetching response from API: {str(e)}")
        finally:
            response_loading.empty()

# Display message count and timestamp
message_count = len(st.session_state["messages"])
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**{message_count} messages** | {current_time}")

# Add clear chat button
if st.button("Clear Chat"):
    st.session_state["messages"] = []