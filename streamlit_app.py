import streamlit as st
import requests

st.set_page_config(page_title="Intelligent Chat", page_icon=":robot:")

st.title("Intelligent Chat")

url = "https://api.perplexity.ai/chat/completions" 
headers = {
  "authorization": "Bearer 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"
}

models = ["pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online",
          "llama-2-70b-chat", "codellama-34b-instruct", "mistral-7b-instruct",
          "mixtral-8x7b-instruct"]

selected_model = st.sidebar.selectbox("Select Model", models)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
def get_response(prompt):
    payload = {"model": selected_model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers).json()
    return response["choices"][0]["message"]["content"]

chat_id = 1
for msg in st.session_state.chat_history:
    st.markdown(f"**#{chat_id} You:** {msg['user']}")
    st.markdown(f"**#{chat_id} PPLX:** {msg['PPLX']}")
    chat_id += 1
    
st.markdown("")

user_input = st.text_input("You:", placeholder="Enter message...")

if st.button("Send"):
    response = get_response(user_input)
    st.session_state.chat_history.append({"user": user_input, "PPLX": response})
    st.experimental_rerun()

st.text("")
st.text(f"You are chatting with the {selected_model} model.")