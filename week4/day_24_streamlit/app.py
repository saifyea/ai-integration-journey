import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Page Config
st.set_page_config(
    page_title="Saif's Kids Store AI",
    page_icon="🛍️",
    layout="wide"
)

# Header
st.title("🛍️ Saif's Kids Store")
st.subheader("All-in-One AI Dashboard for Product, Pricing & Customer Support")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Menu")
    page = st.selectbox(
        "কী করতে চাও?",
        ["💬 AI Chat", "📝 Content Generator", "💰 Price Checker"]
    )
    st.divider()
    st.markdown("**📦 Available Products:**")
    st.markdown("🧩  Bangladesh Map Puzzle — ৳450")
    st.markdown("🎨 Magic Drawing Board — ৳350")
    st.markdown("🧠 Flash Cards — ৳250")

# ✅ Page 1 — AI Chat
if page == "💬 AI Chat":
    st.header("💬 AI Chat Assistant")
    #initial Response
    st.markdown("💡 Try asking:")
    
    with st.chat_message("user"):
        st.write("Flash Card এর দাম কত?")

    with st.chat_message("assistant"):
         st.write("Flash Cards এর দাম **২৫০ টাকা।**")
         st.write("এটি বাচ্চাদের জন্য একটি দুর্দান্ত পণ্য যা শেখার প্রক্রিয়াকে আরও মজাদার করে তোলে। আপনি কি এটি অর্ডার করতে আগ্রহী? 😊")   

   

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input
    if prompt := st.chat_input("প্রশ্ন করো..."):
        #initial Response

        # User message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.write(prompt)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("ভাবছি..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=300,
                    system="""তুমি Saif's Kids Store এর AI Assistant।
                    বাংলায় উত্তর দাও।
                    Products:
                    - Bangladesh Map Puzzle: ৪৫০ টাকা
                    - Magic Drawing Board: ৩৫০ টাকা
                    - Flash Cards: ২৫০ টাকা""",
                    messages=st.session_state.messages
                )
                ai_response = response.content[0].text
                st.write(ai_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )

# ✅ Page 2 — Content Generator
elif page == "📝 Content Generator":
    st.header("📝 Product Content Generator")

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.selectbox(
            "Product বেছে নাও:",
            ["Bangladesh Map Puzzle", "Magic Drawing Board", "Flash Cards"]
        )
        price = st.number_input("দাম (টাকা):", min_value=0, value=450)
        target = st.text_input(
            "Target Customer:",
            value="শিশুদের অভিভাবক"
        )

    with col2:
        content_type = st.multiselect(
            "কী বানাবে?",
            ["Facebook Caption", "Product Description", "Hashtags"],
            default=["Facebook Caption", "Product Description"]
        )

    if st.button("🚀 Generate করো!", type="primary"):
        with st.spinner("AI content বানাচ্ছে..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system="তুমি F-commerce marketing expert। বাংলায় লেখো।",
                messages=[{
                    "role": "user",
                    "content": f"""
পণ্য: {product_name}
দাম: {price} টাকা
টার্গেট: {target}

বানাও: {', '.join(content_type)}
"""
                }]
            )

            st.success("✅ Content তৈরি হয়েছে!")
            st.markdown(response.content[0].text)

            # Download button
            st.download_button(
                label="📥 Download করো",
                data=response.content[0].text,
                file_name=f"{product_name}_content.txt",
                mime="text/plain"
            )

# ✅ Page 3 — Price Checker
elif page == "💰 Price Checker":
    st.header("💰 AI Price Checker")

    col1, col2 = st.columns(2)

    with col1:
        check_product = st.text_input(
            "Product নাম:",
            value="Flash Cards"
        )
        my_price = st.number_input(
            "তোমার দাম (টাকা):",
            min_value=0,
            value=250
        )

    with col2:
        st.info("💡 AI তোমার দাম analyze করবে এবং suggestion দেবে!")

    if st.button("🔍 Check করো!", type="primary"):
        with st.spinner("Analyzing..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system="তুমি Bangladesh e-commerce pricing expert। বাংলায় advice দাও।",
                messages=[{
                    "role": "user",
                    "content": f"""
Product: {check_product}
আমার দাম: {my_price} টাকা

Competitor দাম:
- Bangladesh Map Puzzle: ৪০০-৫০০ টাকা
- Magic Drawing Board: ৩০০-৪০০ টাকা
- Flash Cards: ২০০-৩০০ টাকা

বলো:
1. দাম ঠিক আছে?
2. Suggestion কী?
"""
                }]
            )

            # Show result with metrics
            st.divider()
            m1, m2, m3 = st.columns(3)
            m1.metric("Product", check_product)
            m2.metric("তোমার দাম", f"৳{my_price}")
            m3.metric("Market Range", "৳200-500")

            st.markdown("### 🤖 AI Analysis:")
            st.markdown(response.content[0].text)