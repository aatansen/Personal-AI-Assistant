import streamlit as st
from config.settings import Settings
from core.gemini_engine import GeminiEngine
from core.prompt_controller import PromptController
from core.memory import Memory
from core.assistant import PersonalAssistant
import os
import logging
import json
from datetime import datetime

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

# Chat storage directory
CHAT_STORAGE_DIR = "chat_histories"
os.makedirs(CHAT_STORAGE_DIR, exist_ok=True)

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = Memory()
    logging.info("Memory initialize success")

if "cleared" not in st.session_state:
    st.session_state.cleared = False

if "role" not in st.session_state:
    st.session_state.role = "Tutor"

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

memory: Memory = st.session_state.memory

# Helper functions for chat management
def save_chat(chat_id, title, role, history):
    """Save current chat to file"""
    chat_data = {
        "id": chat_id,
        "title": title,
        "role": role,
        "history": history,
        "timestamp": datetime.now().isoformat()
    }
    filepath = os.path.join(CHAT_STORAGE_DIR, f"{chat_id}.json")
    with open(filepath, 'w') as f:
        json.dump(chat_data, f, indent=2)
    logging.info(f"Chat saved: {chat_id}")

def load_chat(chat_id):
    """Load chat from file"""
    filepath = os.path.join(CHAT_STORAGE_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def list_saved_chats():
    """Get list of all saved chats"""
    chats = []
    for filename in os.listdir(CHAT_STORAGE_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(CHAT_STORAGE_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    chat_data = json.load(f)
                    chats.append({
                        "id": chat_data["id"],
                        "title": chat_data.get("title", "Untitled Chat"),
                        "timestamp": chat_data.get("timestamp", "")
                    })
            except:
                continue
    # Sort by timestamp, newest first
    chats.sort(key=lambda x: x["timestamp"], reverse=True)
    return chats

def delete_chat(chat_id):
    """Delete a saved chat"""
    filepath = os.path.join(CHAT_STORAGE_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        logging.info(f"Chat deleted: {chat_id}")

def export_chat_to_text(history, role):
    """Export chat history to text format"""
    lines = [f"Personal AI Assistant Chat Export", 
             f"Role: {role}",
             f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             "=" * 50,
             ""]
    
    for item in history:
        role_label = item.get("role", "unknown").upper()
        message = item.get("message", "")
        lines.append(f"{role_label}:")
        lines.append(message)
        lines.append("-" * 50)
        lines.append("")
    
    return "\n".join(lines)

def export_chat_to_json(history, role, title):
    """Export chat history to JSON format"""
    return json.dumps({
        "title": title,
        "role": role,
        "exported_at": datetime.now().isoformat(),
        "history": history
    }, indent=2)

# Auto-save current chat periodically
def auto_save_current_chat():
    if len(memory.history) > 1:  # Only save if there's actual conversation
        save_chat(
            st.session_state.current_chat_id,
            st.session_state.chat_title,
            st.session_state.role,
            memory.history
        )

# Sidebar controls
st.sidebar.title("🤖 AI Assistant Controls")

# Chat History Section
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Chat History")

# New Chat Button
if st.sidebar.button("➕ New Chat", use_container_width=True):
    # Save current chat before starting new one
    if len(memory.history) > 1:
        auto_save_current_chat()
    
    # Reset to new chat
    memory.clear()
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chat_title = "New Chat"
    st.session_state.cleared = True
    logging.info("New chat started")
    st.rerun()

# List saved chats
saved_chats = list_saved_chats()
if saved_chats:
    st.sidebar.markdown("**Saved Chats:**")
    for chat in saved_chats:
        col1, col2 = st.sidebar.columns([4, 1])
        
        with col1:
            # Button to load chat
            if st.button(
                f"📝 {chat['title'][:25]}...",
                key=f"load_{chat['id']}",
                use_container_width=True
            ):
                # Save current chat first
                if len(memory.history) > 1:
                    auto_save_current_chat()
                
                # Load selected chat
                chat_data = load_chat(chat['id'])
                if chat_data:
                    memory.history = chat_data['history']
                    st.session_state.role = chat_data.get('role', 'Tutor')
                    st.session_state.current_chat_id = chat_data['id']
                    st.session_state.chat_title = chat_data['title']
                    logging.info(f"Chat loaded: {chat['id']}")
                    st.rerun()
        
        with col2:
            # Delete button
            if st.button("🗑️", key=f"delete_{chat['id']}"):
                delete_chat(chat['id'])
                if st.session_state.current_chat_id == chat['id']:
                    memory.clear()
                    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.session_state.chat_title = "New Chat"
                st.rerun()
else:
    st.sidebar.info("No saved chats yet")

st.sidebar.markdown("---")

# Role Selection
st.session_state.role = st.sidebar.selectbox(
    "Assistant Role",
    ["Tutor", "Coding Assistant", "Career helper"],
    index=["Tutor", "Coding Assistant", "Career helper"].index(st.session_state.role),
    key="role_selectbox"
)

# Export Options
st.sidebar.markdown("---")
st.sidebar.subheader("📤 Export Chat")

if len(memory.history) > 1:
    # Export as Text
    text_export = export_chat_to_text(memory.history, st.session_state.role)
    st.sidebar.download_button(
        label="Download as TXT",
        data=text_export,
        file_name=f"chat_{st.session_state.current_chat_id}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Export as JSON
    json_export = export_chat_to_json(
        memory.history, 
        st.session_state.role,
        st.session_state.chat_title
    )
    st.sidebar.download_button(
        label="Download as JSON",
        data=json_export,
        file_name=f"chat_{st.session_state.current_chat_id}.json",
        mime="application/json",
        use_container_width=True
    )
else:
    st.sidebar.info("Start chatting to enable export")

# Clear Memory button
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Memory", use_container_width=True):
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
st.caption(f"Current Role: {st.session_state.role} | Chat: {st.session_state.chat_title}")

# Add default greeting message if memory is empty
if not memory.history:
    greeting = f"Hey! I am your Personal AI Assistant. I can help you as a {st.session_state.role}."
    memory.history.append({"role": "assistant", "message": greeting})

# Chat input
user_input = st.chat_input("Ask Personal AI Assistant...")
if user_input:
    # Update chat title based on first user message
    if st.session_state.chat_title == "New Chat":
        # Use first 30 chars of first message as title
        st.session_state.chat_title = user_input[:30] + ("..." if len(user_input) > 30 else "")
    
    assistant.respond(user_input)
    
    # Auto-save after response
    auto_save_current_chat()
    st.rerun()

# Render chat history
def normalize_role(role: str) -> str:
    r = (role or "").lower()
    if r in ("user", "human"):
        return "user"
    if r in ("tutor", "coding assistant", "career helper"):
        return "assistant"
    return "assistant"

for item in memory.history:
    role = normalize_role(item.get("role"))
    with st.chat_message(role):
        st.write(item.get("message"))