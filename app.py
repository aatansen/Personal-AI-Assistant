import streamlit as st
from config.settings import Settings
from core.gemini_engine import GeminiEngine
from core.prompt_controller import PromptController
from core.memory import Memory
from core.assistant import PersonalAssistant

# Page config
st.set_page_config(page_title="Personal AI Assistant", layout="centered")

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = Memory()

if "cleared" not in st.session_state:
    st.session_state.cleared = False

# keep role in session_state with a stable key
if "role" not in st.session_state:
    st.session_state.role = "Tutor"

memory: Memory = st.session_state.memory

# Sidebar controls
st.sidebar.title("Personal AI Assistant Controls")
st.session_state.role = st.sidebar.selectbox(
    "Assistant Role",
    ["Tutor", "Coder", "Mentor"],
    index=["Tutor", "Coder", "Mentor"].index(st.session_state.role),
    key="role_selectbox"  # stable key so widget is persistent across reruns
)

# Clear memory button (uses st.rerun() instead of experimental_rerun)
if st.sidebar.button("Clear Memory"):
    # - clear persistent store + in-memory history
    memory.clear()                # implement this to empty JSON/storage and memory.history
    # - one-shot UI flag
    st.session_state.cleared = True
    # - programmatic rerun (use modern API)
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
    st.stop()

# Main UI
st.title("🤖 Personal AI Assistant")

# chat_input returns string when user submits
user_input = st.chat_input("Ask Personal AI Assistant...")

if user_input:
    # respond should append to memory.history (as in your original code)
    assistant.respond(user_input)

# Render chat history
def normalize_role(role: str) -> str:
    r = (role or "").lower()
    if r in ("user", "human"):
        return "user"
    if r in ("tutor", "coder", "mentor"):
        return "assistant"
    return "assistant"

for item in memory.history:
    role = normalize_role(item.get("role"))
    with st.chat_message(role):
        st.write(item.get("message"))
