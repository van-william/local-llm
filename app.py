import streamlit as st
import subprocess

# Title and Description
st.title("Local LLM Chat App using Ollama")
st.write("This app uses Ollama locally to provide a pseudo-ChatGPT experience.")

# Set up session state to store the conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to interact with Ollama
def query_ollama(prompt):
    try:
        # Pass the prompt directly as a positional argument
        result = subprocess.run(
            ["ollama", "run", "llama3.2 ", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: Ollama is not installed or not found in PATH."

# Input form for user interaction
with st.form(key="chat_form"):
    user_input = st.text_input("Type your question here:", placeholder="Ask me anything...")
    submit_button = st.form_submit_button("Send")

# Handle form submission
if submit_button:
    if user_input:
        # Append user's question to the conversation
        st.session_state.conversation.append(("User", user_input))

        # Query Ollama with the user's input
        response = query_ollama(user_input)

        # Append the response to the conversation
        st.session_state.conversation.append(("Ollama", response))
    else:
        st.warning("Please type a question before sending.")

# Display the conversation
if st.session_state.conversation:
    for speaker, message in st.session_state.conversation:
        if speaker == "User":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"*{speaker}:* {message}")

# Instructions for setup
with st.expander("Instructions for Setting Up Ollama"):
    st.write("1. Download and install Ollama from [ollama.com](https://ollama.com).")
    st.write("2. Make sure you have a compatible model downloaded, such as 'llama'.")
    st.write("3. Ensure Ollama is available in your PATH environment variable.")
    st.write("4. Launch this Streamlit app and start chatting!")
