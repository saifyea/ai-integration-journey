import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Saif's Kids Store")
st.caption("AI Customer Support — ২৪/৭ সেবা")

# System prompt
SYSTEM = """তুমি Saif's Kids Store এর AI Assistant।
বাংলায় friendly ভাবে উত্তর দাও।

Products:
- Bangladesh Map Puzzle: ৪৫০ টাকা, ৫-১২ বছর
- Magic Drawing Board: ৩৫০ টাকা, ৩-১০ বছর
- Flash Cards: ২৫০ টাকা, ৩-৬ বছর

Delivery: ঢাকায় ১-২ দিন, বাইরে ৩-৫ দিন
Return: ৭ দিনের মধ্যে
Order: Facebook page এ message করুন"""

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Welcome message
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "আস্সালামু আলাইকুম! 👋 আমি Saif's Kids Store এর AI Assistant। কীভাবে সাহায্য করতে পারি?"
    })

# Show messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Quick buttons
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💰 দাম জানো"):
        st.session_state.quick = "সব products এর দাম বলো"
with col2:
    if st.button("🚚 Delivery"):
        st.session_state.quick = "Delivery সময় কতদিন?"
with col3:
    if st.button("📦 Products"):
        st.session_state.quick = "সব products দেখাও"

# Handle quick buttons
if "quick" in st.session_state and st.session_state.quick:
    prompt = st.session_state.quick
    st.session_state.quick = None

    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=SYSTEM,
        messages=st.session_state.chat_history
    )

    ai_response = response.content[0].text
    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_response}
    )
    st.rerun()

# Chat input
if prompt := st.chat_input("প্রশ্ন করো..."):
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("assistant"):
        with st.spinner("ভাবছি..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=SYSTEM,
                messages=st.session_state.chat_history
            )
            ai_response = response.content[0].text
            st.write(ai_response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_response}
    )
    st.rerun()

# Clear button
if st.button("🗑️ Chat Clear করো"):
    st.session_state.chat_history = []
    st.rerun()