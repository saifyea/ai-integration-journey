import os
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

# ========== সেটআপ ==========
load_dotenv()

# API Key চেক
if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("❌ ANTHROPIC_API_KEY সেট করুন .env ফাইলে!")
    st.stop()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ========== পেজ কনফিগারেশন ==========
st.set_page_config(
    page_title="বাংলা AI চ্যাটবট",
    page_icon="🤖",
    layout="centered"
)

# ========== CSS স্টাইলিং ==========
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .bot-message {
        background-color: #f3e5f5;
        text-align: left;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)



# ========== মেমোরি (Session State) ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# ========== চ্যাট হিস্টরি দেখান ==========
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg["content"])

# ========== ইনপুট বক্স ==========
user_input = st.chat_input("আপনার মেসেজ লিখুন...")

if user_input:
    # 👤 ব্যবহারকারীর মেসেজ দেখান
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # মেমোরিতে যোগ করুন
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_history.append({
        "role": "user", 
        "content": user_input
    })
    
    # 🤖 AI উত্তর তৈরি করুন
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("ভাবছি..."):
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1000,
                    system="""তুমি একজন বাংলা ভাষার সহায়ক। 
                    সবসময় বাংলায় উত্তর দাও। 
                    সহজ ও বোধগম্য ভাষায় কথা বলো।""",
                    messages=st.session_state.conversation_history
                )
                
                assistant_reply = response.content[0].text
                st.write(assistant_reply)
                
                # মেমোরিতে যোগ করুন
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_reply
                })
                st.session_state.conversation_history.append({
                    "role": "assistant", 
                    "content": assistant_reply
                })
                
            except Exception as e:
                st.error(f"❌ ভুল: {str(e)}")

# ========== সাইডবার ==========
with st.sidebar:
    st.header("⚙️ সেটিংস")
    
    if st.button("🗑️ কথোপকথন মুছুন"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()
    
    st.divider()
    st.markdown(f"**মেসেজ সংখ্যা:** {len(st.session_state.messages)}")
     
    st.divider()
    st.markdown("""
    **কীভাবে ব্যবহার করবেন:**
    1. নিচের বক্সে লিখুন
    2. Enter চাপুন
    3. AI উত্তর দেবে!
    
    ***কমান্ড:***
    - 'বাই' বললে বিদায়
    """)


    page=st.selectbox("তুমি কি করতে চাও",["💬 AI Chat", "📝 Content Generator", "💰 Price Checker"])

   # ========== হেডার ==========
if page=="💰 Price Checker":
    st.title("💰 বাংলা Price Checker")
    st.markdown("**Anthropic Claude দিয়ে তৈরি** | ")
    st.divider()
elif page=="📝 Content Generator":
    st.title("📝 বাংলা AI Content Generator")
    st.markdown("**Anthropic Claude দিয়ে তৈরি** | আপনার প্রডাকডের জন্য কন্টেন্ট তৈরি করে দেব")
    st.divider()
else:
    st.title("🤖 বাংলা AI চ্যাটবট")
    st.markdown("**Anthropic Claude দিয়ে তৈরি** | আগের কথা মনে রাখে 🧠")
    st.divider()