import streamlit as st
import requests

st.set_page_config(page_title="Smart Talk with PPLX", page_icon=":robot:")

st.title("Smart Chat with PPLX")

url = "https://api.perplexity.ai/chat/completions" 
headers = {
    "authorization": "Bearer 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"
}

models = ["pplx-7b-chat (input $0.07, output $0.28)",
          "pplx-70b-chat (input $0.70, output $2.80)",  
          "pplx-7b-online (requests $5, output $0.28)",
          "pplx-70b-online (requests $5, output $2.80)",
          "llama-2-70b-chat (input $0.70, output $2.80)",
          "codellama-34b-instruct (input $0.35, output $1.40)",
          "mistral-7b-instruct (input $0.07, output $0.28)",
          "mixtral-8x7b-instruct (input $0.14, output $0.56)"]

selected_model = st.sidebar.selectbox("Select Model", models)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_response(prompt):
    payload = {"model": selected_model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers).json()
    return response["choices"][0]["message"]["content"]

def send_message():
    user_input = st.session_state.user_input
    if user_input:  # Check if the input is not empty
        response = get_response(user_input)
        st.session_state.chat_history.append({"user": user_input, "PPLX": response})
        st.session_state.user_input = ""  # Clear the input field
        st.experimental_rerun()

chat_id = 1
for msg in st.session_state.chat_history:
    st.markdown(f"**#{chat_id} You:** {msg['user']}")
    st.markdown(f"**#{chat_id} PPLX:** {msg['PPLX']}")
    chat_id += 1

st.markdown("")

# Using the `on_change` parameter with `send_message` as the callback function
user_input = st.text_input("You:", value="", on_change=send_message, key="user_input")

st.text("")
st.text(f"You are chatting with the {selected_model} model.")