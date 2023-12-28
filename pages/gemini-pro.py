import streamlit as st
import json
import google.generativeai as genai

def initialize_session_state():
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = "AIzaSyBwibYDUMg8gFiKBvRRJjvJCiLTi6_Er3Q"
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'chat_placeholder' not in st.session_state:
        st.session_state['chat_placeholder'] = st.empty()

def configure_ai_model():
    api_key = st.session_state.api_key
    genai.configure(api_key=api_key)

    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.6, 0.1)
    top_p = st.sidebar.number_input("Top P", 0.0, 1.0, 1.0, 0.1)
    top_k = st.sidebar.number_input("Top K", 1, 100, 1)
    max_output_tokens = st.sidebar.number_input("Max Output Tokens", 1, 10000, 2048)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
    }

    safety_settings = "{}"
    safety_settings = json.loads(safety_settings)

    gemini = genai.GenerativeModel(model_name="gemini-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)
    
    return gemini

def get_response(user_input):
    gemini = configure_ai_model()
    prompt_parts = [user_input]
    
    try:
        response = gemini.generate_content(prompt_parts)
        return response.text if response.text else "No output from Gemini."
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred while communicating with Gemini Pro."

def send_message():
    user_input = st.session_state.user_input
    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append({"user": user_input, "PPLX": response})
        st.session_state.chat_placeholder.markdown(chat_history_to_md(st.session_state.chat_history), unsafe_allow_html=True)
        st.session_state.user_input = ""

def chat_history_to_md(chat_history):
    markdown_text = ""
    chat_id = 1
    for msg in chat_history:
        markdown_text += f"**#{chat_id} You:** {msg['user']}\n\n"
        markdown_text += f"**#{chat_id} Gemini Pro:** {msg['PPLX']}\n\n"
        chat_id += 1
    return markdown_text

def text_page():
    st.title("Gemini Pro 🤖")
    initialize_session_state()
    chat_placeholder = st.empty()
    chat_placeholder.markdown(chat_history_to_md(st.session_state.chat_history), unsafe_allow_html=True)
    st.text_input("You:", value="", on_change=send_message, key="user_input")

    if st.button('Clear Chat'):
        st.session_state.chat_history = []
        chat_placeholder.empty()

if __name__ == "__main__":
    text_page()