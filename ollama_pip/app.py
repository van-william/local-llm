import streamlit as st
import ollama

# Title and Description
st.title("Local LLM Chat App using Ollama")
st.write("This app uses Ollama locally to provide a local LLM experience.")

# Set up session state to store the conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to get a list of available Ollama models
def get_ollama_models():
    try:
        models = ollama.list()  # Get models using Python API
        return [model["model"] for model in models["models"]]
    except Exception as e:
        return [f"Error: {str(e)}"]


# Function to stream output from Ollama
def query_ollama_stream(prompt, model):
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=True)
        for chunk in response:
            yield chunk["message"]["content"]
    except Exception as e:
        yield f"Error: {str(e)}"


# Get list of available models
available_models = get_ollama_models()

# Display available models
st.sidebar.title("Available Models")
if available_models:
    if "Error" in available_models[0]:
        st.sidebar.error(available_models[0])
    else:
        selected_model = st.sidebar.selectbox("Choose a model", available_models)
else:
    st.sidebar.warning("No models available.")
    selected_model = None

# Input form for user interaction
with st.form(key="chat_form"):
    user_input = st.text_input("Type your question here:", placeholder="Ask me anything...")
    submit_button = st.form_submit_button("Send")

# Handle form submission
if submit_button:
    if not selected_model:
        st.error("Please select a model from the sidebar.")
    elif user_input:
        # Append user's question to the conversation
        st.session_state.conversation.append(("User", user_input))

        # Display a status message while the model is running
        with st.spinner(f"Generating response from {selected_model}..."):
            # Query Ollama with the user's input and stream the response
            response_placeholder = st.empty()
            response_text = ""
            for chunk in query_ollama_stream(user_input, selected_model):
                response_text += chunk
                # response_placeholder.markdown(f"**{selected_model}:**\n\n```{response_text}```")
                response_placeholder.markdown(f"**{selected_model}:**\n\n```{response_text}```", unsafe_allow_html=True)



        # Append the final response to the conversation without re-displaying it
        st.session_state.conversation.append((selected_model, response_text.strip()))
        response_placeholder.empty()  # Clear the live display after completion

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
    st.write("2. Make sure you have a compatible model downloaded.")
    st.write("3. Ensure Ollama is available in your PATH environment variable.")
    st.write("4. Launch this Streamlit app and start chatting!")
