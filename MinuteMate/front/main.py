import streamlit as st
import pandas as pd

# Set up the page layout
st.set_page_config(layout="wide")

# Sidebar with text and logo
st.sidebar.image("./../../assets/Fun_Logo.jpg", width=150)  # Replace with your logo URL or local path
st.sidebar.markdown("# Minute Mate")
st.sidebar.markdown("Welcome to the app!")

# Initialize chat history in session state if not already present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

col1, col2 = st.columns(2)

with col1:
    st.header("Chat Interface")

    # Add custom CSS for border box around the chat interface
    st.markdown(
        """
        <style>
        .chat-container {
            border: 2px solid #ccc;
            padding: 15px;
            border-radius: 10px;
            background-color: #f9f9f9;
            max-height: 500px;
            overflow-y: auto;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Function to display chat history with styled messages inside the bordered box
    def display_chat():
        for chat in st.session_state['chat_history']:
            if chat['is_user']:
                # User message (right-aligned, green bubble) with 🧑 emoji
                st.markdown(
                    f"""
                    <div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:10px 0; text-align:right;'>
                        <strong>🧑:</strong> {chat['message']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Bot message (left-aligned, grey bubble) with 🤖 emoji
                st.markdown(
                    f"""
                    <div style='background-color:#EAEAEA; padding:10px; border-radius:10px; margin:10px 0; text-align:left;'>
                        <strong>🤖:</strong> {chat['message']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Input for new message at the bottom (after displaying chat)
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Append user message to session state chat history before displaying chat again
        st.session_state['chat_history'].append({'message': user_input, 'is_user': True})

        # Placeholder bot response logic (you can replace this with actual chatbot logic)
        bot_response = f"Echo: {user_input}"

        # Append bot response to session state chat history
        st.session_state['chat_history'].append({'message': bot_response, 'is_user': False})

        # Rerun the app to display updated chat history immediately after adding new messages
        st.rerun()

    # Display chat after processing input (this happens on rerun)
    display_chat()

# Column 2: Tabs with different functionalities
with col2:
    st.header("Multi-Tab Section")
    
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    
    with tab1:
        st.subheader("Functionality 1")
        st.write("This is where you can add functionality for Tab 1.")
    
    with tab2:
        st.subheader("Functionality 2")
        data = {"A": [1, 2, 3], "B": [4, 5, 6]}
        df = pd.DataFrame(data)
        st.write("Displaying a DataFrame:")
        st.dataframe(df)
    
    with tab3:
        st.subheader("Functionality 3")
        number = st.slider("Pick a number", 0, 100)
        st.write(f"You selected: {number}")