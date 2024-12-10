import streamlit as st
import requests


# st.set_page_config(layout="wide")

# st.markdown(
#     """
#     <style>
#     .stApp {
#         padding: 0rem;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


NUM_IMAGES_PER_ROW = 3

def display_chat_messages() -> None:
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for i in range(0, len(message["images"]), NUM_IMAGES_PER_ROW):
                    cols = st.columns(NUM_IMAGES_PER_ROW)
                    for j in range(NUM_IMAGES_PER_ROW):
                        if i + j < len(message["images"]):
                            cols[j].image(message["images"][i + j], width=200)

st.title("📝 Minute Mate")

# with st.sidebar:
    
#     # TODO add image to app assets to deploy
#     # st.sidebar.image("./../../assets/Fun_Logo.jpg", width=150)
#     st.subheader("Speeding up Municipal Communication")

#     st.header("Settings")
#     with st.form(key='api_keys_form'):
#         openai_key = st.text_input("Enter your OpenAI Key", type="password", help="Your OpenAI API key for accessing GPT models.")
#         weaviate_url = st.text_input("Enter Weaviate URL", help="The URL of your Weaviate instance.")
#         weaviate_api_key = st.text_input("Enter Weaviate API Key", type="password", help="API key for authenticating with Weaviate.")
#         submit_button = st.form_submit_button(label="Save Settings")
    
#     if submit_button:
#         st.success("Settings saved successfully!", icon="💚")
#         st.session_state['openai_key'] = openai_key
#         st.session_state['weaviate_url'] = weaviate_url
#         st.session_state['weaviate_api_key'] = weaviate_api_key



with st.expander("Built with Weaviate, OpenAI and Streamlit"):
    st.caption("MinuteMate improves how municipalities communicate with their citizens by simplifying the creation of meeting minutes. Upload your meeting audio and get formatted, ready-to-use minutes in less time. This ensures faster, clearer communication between local governments and their communities, providing key points, agenda items, and voting outcomes quickly and efficiently.")

col1, col2, col3 = st.columns([0.2, 0.5, 0.2])

tab1, tab2 = st.tabs(["Chat", "Summary"])

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False


display_chat_messages()

if not st.session_state.greetings:
    with st.chat_message("assistant"):
        intro = "Hey! I am Minute Mate, your assistant for finding everything related to your meetings. Let's get started!"
        st.markdown(intro)
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True

example_prompts = [
    "Summarize my last meeting with the town planner",
    "Retrieve the project proposal document from the recordings",
    "Find all the meetings with Q3 reports",
    "Check my agenda meeting with the Director",
    "Summarize the 'Budget Planning' document",
    "List all files shared with me in the last week",
]

example_prompts_help = [
    "Summarize a specific meeting based on team or subject",
    "Search and retrieve a specific document from your cloud storage",
    "Find all files related to a specific topic (e.g., Q3 sales)",
    "Check your calendar for upcoming meetings or events",
    "Summarize a specific document by name or topic",
    "List all files that were shared with you recently",
]

button_cols = st.columns(3)
button_cols_2 = st.columns(3)

button_pressed = ""

if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
    button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
    button_pressed = example_prompts[1]
elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2]):
    button_pressed = example_prompts[2]

elif button_cols_2[0].button(example_prompts[3], help=example_prompts_help[3]):
    button_pressed = example_prompts[3]
elif button_cols_2[1].button(example_prompts[4], help=example_prompts_help[4]):
    button_pressed = example_prompts[4]
elif button_cols_2[2].button(example_prompts[5], help=example_prompts_help[5]):
    button_pressed = example_prompts[5]


if prompt := (st.chat_input("Type your prompt") or button_pressed):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Make API call to backend
        response = requests.post(
            "http://host.docker.internal:8001/process-prompt",  # Adjust URL as needed
            json={"user_prompt_text": prompt}
        )
        
        # Check if request was successful
        if response.status_code == 200:
            # Extract the generated response
            generated_response = response.json().get('generated_response', 'No response generated')
            
            # Display the response
            with st.chat_message("assistant"):
                st.markdown(generated_response)
            
            # Add to message history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": generated_response
            })
        else:
            st.error(f"API Error: {response.text}")
    
    except requests.RequestException as e:
        st.error(f"Connection error: {e}")

