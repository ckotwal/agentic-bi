import streamlit as st
import uuid
from core.gen_bi_react_agent import GenBIReactAgent
from ui.ui_helper import StreamlitBIMessageRenderer


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="BI Assistant", layout="wide")

st.title("🧠 Conversational Business Intelligence Assistant")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = GenBIReactAgent()

# Display chat history
renderer = StreamlitBIMessageRenderer(False)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
       renderer.process_message(msg["content"], msg["type"])

# Chat input
prompt = st.chat_input("Ask me a question...")
if prompt:
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate or retrieve session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    st.session_state.agent_executor.stream(prompt, st.session_state.session_id, StreamlitBIMessageRenderer(True))

