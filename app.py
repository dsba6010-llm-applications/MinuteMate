import streamlit as st
from openai import OpenAI
import requests
import time
import toml

st.title("Modal Llama 3 Instruct Deployment")

api_url = st.secrets["MODAL_BASE_URL"] + "/v1"

# Set API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["DSBA_LLAMA3_KEY"], base_url=api_url)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "/models/NousResearch/Meta-Llama-3-8B-Instruct"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to check API health
def check_api_health():
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['DSBA_LLAMA3_KEY']}"
        }
        response = requests.get(f"{st.secrets['MODAL_BASE_URL']}/health", headers=headers, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Sidebar
st.sidebar.title("Chat Settings")

# Model parameters
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 50, 2000, 1000, 50)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0, 0.1)
presence_penalty = st.sidebar.slider("Presence Penalty", -2.0, 2.0, 0.0, 0.1)
frequency_penalty = st.sidebar.slider("Frequency Penalty", -2.0, 2.0, 0.0, 0.1)

# System prompt
system_prompt = st.sidebar.text_area("System Prompt", "You are a helpful assistant.")

# Reset button
if st.sidebar.button("Reset Chat"):
    st.session_state.messages = []
    st.sidebar.success("Chat session reset!")

# Check API health and display warning if not healthy
api_healthy = check_api_health()
if not api_healthy:
    st.warning("Warning: The API endpoint is currently unavailable. Some features may not work properly.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    start_time = time.time()
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            )
            for chunk in stream:
                full_response += chunk.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            # Add latency print statement
            end_time = time.time()
            latency = end_time - start_time
            tokens = len(full_response.split()) + 1
            st.info(f"Latency: {tokens / latency:.2f} tokens per seconds")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            full_response = "I apologize, but I encountered an error while processing your request."
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})