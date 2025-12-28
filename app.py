import streamlit as st
from config.settings import Settings
from core.gemini_engine import GeminiEngine
from core.prompt_controller import PromptController
from core.memory import Memory
from core.assistant import PersonalAssistant
import os
import logging

# Logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)
logging.basicConfig(
    filename=log_path,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Page config
st.set_page_config(page_title="Personal AI Assistant", layout="centered")

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = Memory()
    logging.info("Memory initialize success")

if "cleared" not in st.session_state:
    st.session_state.cleared = False

# Keep role in session_state with a stable key
if "role" not in st.session_state:
    st.session_state.role = "Tutor"

memory: Memory = st.session_state.memory

# Sidebar controls
st.sidebar.title("Personal AI Assistant Controls")
st.session_state.role = st.sidebar.selectbox(
    "Assistant Role",
    ["Tutor", "Coding Assistant", "Career helper"],
    index=["Tutor", "Coding Assistant", "Career helper"].index(st.session_state.role),
    key="role_selectbox"
)

# Clear memory button
if st.sidebar.button("Clear Memory"):
    memory.clear()
    st.session_state.cleared = True
    logging.info("User clear memory successfully")
    st.rerun()

# One-shot cleared message
if st.session_state.cleared:
    st.success("Memory cleared.")
    st.session_state.cleared = False

# Assistant setup
settings = Settings()
try:
    api_key = settings.load_api_key()
    engine = GeminiEngine(api_key=api_key)
    prompt_controller = PromptController(st.session_state.role)
    assistant = PersonalAssistant(engine, prompt_controller, memory)
except EnvironmentError as e:
    st.error(
        "⚠️ API key not found. Please set your GEMINI_API_KEY in the .env file "
        "to use this assistant."
    )
    logging.info("API key not found.")
    st.stop()

# Main UI
st.title("🤖 Personal AI Assistant")

# Add default greeting message if memory is empty
if not memory.history:
    greeting = f"Hey! I am your Personal AI Assistant. I can help you as a {st.session_state.role}."
    memory.history.append({"role": "assistant", "message": greeting})

# chat_input returns string when user submits
user_input = st.chat_input("Ask Personal AI Assistant...")

if user_input:
    assistant.respond(user_input)

# Render chat history
def normalize_role(role: str) -> str:
    r = (role or "").lower()
    if r in ("user", "human"):
        return "user"
    if r in ("tutor", "Coding Assistant", "Career helper", "assistant"):
        return "assistant"
    return "assistant"

for item in memory.history:
    role = normalize_role(item.get("role"))
    with st.chat_message(role):
        st.write(item.get("message"))