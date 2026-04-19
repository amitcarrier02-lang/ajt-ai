import streamlit as st
import time
import os
from google import genai
from google.genai import types

# ==========================================
# 1. Page Config (Professional Look)
# ==========================================
st.set_page_config(
    page_title="AJT Live Support", 
    page_icon="🟢", 
    layout="centered"
)

# Custom spacing
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Header & Professional Branding
# ==========================================
st.markdown("### 🟢 AJT Live Support")
st.caption("We typically reply in seconds. Founder: Amit (Funnel AJT)")
st.divider()

# ==========================================
# 3. Data & API Setup (API Key Attached)
# ==========================================
# app.py ke andar key aise likhni hai (Taaki ye leak na ho)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# AI Instruction - Making it feel like a real person
system_instruction = """
You are a senior support member of 'Amit Ji Tech'. 
Never say you are an AI or a bot. You are part of Amit sir's expert team.
Amit sir is the Founder of Funnel AJT and a top affiliate marketing mentor.
Be professional, empathetic, and highly efficient in your replies.
"""

# Check for knowledge file locally
if os.path.exists("knowledge.txt"):
    with open("knowledge.txt", "r", encoding="utf-8") as f:
         system_instruction += "\n\nUse this context to help the user:\n" + f.read()

# Client Setup
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GEMINI_API_KEY)

# Chat Session Setup
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.client.chats.create(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(system_instruction=system_instruction)
    )
    # First greeting from the team
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am from Amit sir's team at Amit Ji Tech. How can I assist you with your business today?", "avatar": "🧑‍💼"}
    ]

# ==========================================
# 4. Chat Interface Logic
# ==========================================

# Clear Chat History Button
if st.button("🗑️ Clear Conversation"):
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    st.session_state.messages = [
         {"role": "assistant", "content": "Conversation cleared. Amit's team is ready to help again!", "avatar": "🧑‍💼"}
    ]
    st.rerun()

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Type your message here..."):
    
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Human-like Response with "Typing..."
    with st.chat_message("assistant", avatar="🧑‍💼"):
        with st.spinner("Amit's Team is typing..."):
            try:
                time.sleep(1.2) # Natural human delay
                response = st.session_state.chat_session.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "avatar": "🧑‍💼"})
            except Exception as e:
                st.error(f"Unable to connect. Please try again. Error: {e}")
