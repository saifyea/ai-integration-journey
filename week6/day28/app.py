import streamlit as st
from anthropic import Anthropic
import os

# ✅ Production config
def get_api_key():
    # Streamlit Cloud
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except:
        pass
    # Environment variable
    key = os.getenv("ANTHROPIC_API_KEY")
    if key:
        return key
    # Error
    st.error("❌ API Key পাওয়া যায়নি!")
    st.stop()

client = Anthropic(api_key=get_api_key())

st.set_page_config(
    page_title="Saif's Kids Store AI",
    page_icon="🛍️",
    layout="wide"
)

# ✅ Health check endpoint
if st.query_params.get("health") == "check":
    st.json({"status": "ok", "version": "1.0.0"})
    st.stop()

st.title("🛍️ Saif's Kids Store AI")
st.caption("Production Version — Powered by Claude AI")

# App content
page = st.sidebar.selectbox(
    "Menu:",
    ["💬 AI Chat", "📝 Content Generator",
     "💰 Price Checker", "🤖 Multi-Agent"]
)

if page == "💬 AI Chat":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("প্রশ্ন করো..."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ভাবছি..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=300,
                    system="""Saif's Kids Store AI Assistant।
বাংলায় উত্তর দাও।
Products: Map Puzzle ৳450, Drawing Board ৳350, Flash Cards ৳250""",
                    messages=st.session_state.messages
                )
                ai_resp = response.content[0].text
                st.write(ai_resp)

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_resp}
        )