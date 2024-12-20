import os
import logging
from typing import Optional, List, Dict
import streamlit as st
import requests
import weaviate
from weaviate.auth import AuthApiKey
from openai import OpenAI
from pydantic import BaseModel, Field

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="Minute Mate", layout="wide")

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def initialize_weaviate_client(municipality):
    """
    Initialize the Weaviate client for a selected municipality using credentials from secrets.toml.
    """
    try:
        client = weaviate.Client(
            url=st.secrets[municipality]["WEAVIATE_URL"],
            auth_client_secret=AuthApiKey(api_key=st.secrets[municipality]["WEAVIATE_API_KEY"]),
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize Weaviate client for {municipality}: {e}")
        return None

def are_api_keys_set():
    """
    Check if the OpenAI API key is configured.
    """
    return "OPENAI_API_KEY" in st.session_state and st.session_state["OPENAI_API_KEY"]

def fetch_documents_from_weaviate(client):
    """
    Fetch all meeting documents grouped by date and meeting type from Weaviate.
    """
    query = """
    {
      Get {
        MeetingDocument {
          meeting_date
          meeting_type
          file_type
          chunk_index
          content
          source_document
        }
      }
    }
    """
    try:
        response = client.query.raw(query)
        documents = response.get("data", {}).get("Get", {}).get("MeetingDocument", [])
        grouped_documents = {}

        for doc in documents:
            date_key = doc.get("meeting_date", "Unknown Date")
            meeting_type = doc.get("meeting_type", "Unknown Type")
            metadata = {
                "meeting_date": date_key,
                "meeting_type": meeting_type,
                "file_type": doc.get("file_type", "N/A"),
                "source_document": doc.get("source_document", "N/A"),
            }
            chunk = {
                "chunk_index": doc.get("chunk_index", "N/A"),
                "content": doc.get("content", "")[:150],
            }
            if date_key not in grouped_documents:
                grouped_documents[date_key] = {"metadata": metadata, "chunks": []}
            grouped_documents[date_key]["chunks"].append(chunk)

        return grouped_documents
    except Exception as e:
        st.error(f"Error fetching documents from Weaviate: {e}")
        return {}

# ---------------------------
# PAGES
# ---------------------------

def home_page():
    st.markdown(
        """
        <h1 style="text-align: center;">Welcome to Minute Mate</h1>
        <p style="text-align: center;">
            Your interactive assistant for exploring municipal meetings. Effortlessly navigate meeting records,
            extract insights, and simplify your workflows with our AI-powered chatbot.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar for API key and municipality selection
    with st.sidebar:
        st.markdown(
            """
            <h2 style="text-align: center;">API Setup</h2>
            <p style="text-align: center;">
                Choose the municipality you're interested in and set your OpenAI API key.
                <br>
                You can obtain an API key <a href="https://platform.openai.com/api-keys" style="color: #6bb2a4;">here</a>.
            </p>
            """,
            unsafe_allow_html=True,
        )

        # Dynamically load municipalities from secrets
        municipalities = list(st.secrets.keys())
        if not municipalities:
            st.error("No municipalities found in secrets.toml")

        openai_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API Key.")
        municipality = st.selectbox("Select Municipality", options=municipalities, help="Choose your municipality.")

        if st.button("Save Settings"):
            st.session_state["OPENAI_API_KEY"] = openai_key
            st.session_state["municipality"] = municipality
            if openai_key:
                st.session_state["openai_client"] = OpenAI(api_key=openai_key)
            st.success("Settings saved successfully!")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if are_api_keys_set():
            st.button("Go to Chat", on_click=lambda: st.session_state.update(page="chat"))
        else:
            st.button("Go to Chat", disabled=True)

    with col2:
        if are_api_keys_set():
            st.button("View Documents", on_click=lambda: st.session_state.update(page="view"))
        else:
            st.button("View Documents", disabled=True)

def chat_page():
    st.title("💬 Chat with Minute Mate")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.greetings = False
    if "retrieved_chunks" not in st.session_state:
        st.session_state["retrieved_chunks"] = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Initial greeting if needed
    if not st.session_state.greetings:
        with st.chat_message("assistant"):
            intro = "Hello! How can I assist you with your municipal meetings today?"
            st.markdown(intro)
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.greetings = True

    # Example prompts
    example_prompts = [
        "Generate a list of all Board of Commissioner Meetings held in 2023",
        "List the Agenda from the 7/16/2024 Board of Commissioner Meeting",
        "Generate a list of all Rezoning cases in 2024.",
        "Summarize the Board of Commissioner Meeting Audio Transcript from 7/16/2024.",
        "List any Meetings with Budget discussions from 2023.",
        "When was the Tripointe Home Development off of Wilkinson Approved?"
    ]

    st.markdown("**Try these example prompts:**")
    prompt_cols = st.columns(3)
    for i, ep in enumerate(example_prompts[:3]):
        if prompt_cols[i].button(ep):
            st.session_state.user_picked_prompt = ep
    prompt_cols_2 = st.columns(3)
    for i, ep in enumerate(example_prompts[3:]):
        if prompt_cols_2[i].button(ep):
            st.session_state.user_picked_prompt = ep

    # If user picked a prompt via button, set prompt from that
    if "user_picked_prompt" in st.session_state:
        prompt = st.session_state.user_picked_prompt
        del st.session_state["user_picked_prompt"]
    else:
        # Prompt input
        prompt = st.chat_input("Type your prompt")

    # Sidebar: Show processing indicator if needed
    with st.sidebar:
        st.header("Retrieved Context Segments")
        # Processing indicator
        if st.session_state.get("processing", False):
            st.info("Processing your request...")

        if st.session_state["retrieved_chunks"]:
            for idx, chunk in enumerate(st.session_state["retrieved_chunks"][:5]):
                with st.expander(f"Chunk {idx + 1}", expanded=False):
                    st.write(f"**Chunk ID:** {chunk.get('chunk_id', 'N/A')}")
                    st.write(f"**Score:** {chunk.get('score', 'N/A')}")
                    st.write(f"**Content:** {chunk.get('content', 'N/A')}")
                    metadata = chunk.get('metadata', {})
                    st.write("**Metadata:**")
                    st.write(f"- Meeting Date: {metadata.get('meeting_date', 'N/A')}")
                    st.write(f"- Meeting Type: {metadata.get('meeting_type', 'N/A')}")
                    st.write(f"- File Type: {metadata.get('file_type', 'N/A')}")
                    st.write(f"- Chunk Index: {metadata.get('chunk_index', 'N/A')}")
                    st.write(f"- Source Document: {metadata.get('source_document', 'N/A')}")
        else:
            st.info("No context segments retrieved yet.")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Set processing state
        st.session_state["processing"] = True
        # Rerun so that sidebar updates with processing info immediately
        st.experimental_rerun()

    # If we were processing a prompt, handle that now
    if st.session_state.get("processing", False) and not st.session_state.get("just_processed", False):
        with st.spinner("Processing your request..."):
            try:
                response = requests.post(
                    "http://host.docker.internal:8000/process-prompt",  # Adjust URL as needed
                    json={"user_prompt_text": prompt}
                )
                if response.status_code == 200:
                    response_data = response.json()
                    generated_response = response_data.get('generated_response', 'No response generated')
                    context_segments = response_data.get('context_segments', [])
                    st.session_state['retrieved_chunks'] = context_segments

                    with st.chat_message("assistant"):
                        st.markdown(generated_response)
                    st.session_state.messages.append({"role": "assistant", "content": generated_response})
                else:
                    st.error(f"API Error: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {e}")

        # Set a flag to indicate we've just processed a prompt to avoid re-processing on rerun
        st.session_state["just_processed"] = True
        # Turn off processing state
        st.session_state["processing"] = False
        # Rerun to update sidebar and clear processing indicators
        st.experimental_rerun()

    # If we just processed, reset the flag
    if st.session_state.get("just_processed", False):
        del st.session_state["just_processed"]

    # Navigation
    st.button("Go Home", on_click=lambda: st.session_state.update(page="home"))
    st.button("View Documents", on_click=lambda: st.session_state.update(page="view"))

def view_documents_page():
    st.title("\U0001F4C4 Meeting Documents List")
    st.caption("View all available meeting dates, metadata, and document chunks (ordered by date).")

    municipality = st.session_state.get("municipality")
    if not municipality:
        st.warning("Please set a municipality on the home page first.")
        return

    client = initialize_weaviate_client(municipality)
    if not client:
        st.warning("Could not initialize Weaviate client. Check your settings.")
        return

    grouped_documents = fetch_documents_from_weaviate(client)

    # Sort documents by date if possible (assuming meeting_date in YYYY-MM-DD format)
    sorted_dates = sorted(grouped_documents.keys())

    for date_key in sorted_dates:
        data = grouped_documents[date_key]
        with st.expander(f"{data['metadata']['meeting_date']} - {data['metadata']['meeting_type']}"):
            st.markdown("### Metadata")
            for key, value in data["metadata"].items():
                st.markdown(f"**{key.capitalize().replace('_', ' ')}:** {value}")

            st.markdown("### Document Chunks")
            for chunk in data["chunks"]:
                st.markdown(f"- **Chunk Index:** {chunk['chunk_index']}")
                st.markdown(f"  - **Content:** {chunk['content']}")

    # Navigation
    st.button("Go Home", on_click=lambda: st.session_state.update(page="home"))
    st.button("Go to Chat", on_click=lambda: st.session_state.update(page="chat"))

# ---------------------------
# MAIN APP LOGIC
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "chat":
    if are_api_keys_set():
        chat_page()
    else:
        st.warning("Please set your API keys and municipality in Home page first.")
        if st.button("Go Home"):
            st.session_state.page = "home"
            st.experimental_rerun()
elif st.session_state.page == "view":
    if are_api_keys_set():
        view_documents_page()
    else:
        st.warning("Please set your API keys and municipality in Home page first.")
        if st.button("Go Home"):
            st.session_state.page = "home"
            st.experimental_rerun()
