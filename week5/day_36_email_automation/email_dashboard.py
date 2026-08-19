import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

st.set_page_config(
    page_title="Email AI Assistant",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI Email Assistant")
st.caption("Email categorize করো + AI reply বানাও!")

# ✅ Manual Email Input (Gmail API ছাড়া)
st.header("📨 Email Input")

col1, col2 = st.columns(2)

with col1:
    sender = st.text_input("From:", placeholder="customer@example.com")
    subject = st.text_input("Subject:", placeholder="Order inquiry...")
    body = st.text_area("Email Body:", height=200,
                        placeholder="Email content...")

with col2:
    st.info("""
    **Auto Features:**
    ✅ Email categorization
    ✅ AI reply generation
    ✅ Professional tone
    ✅ Store info included
    """)

if st.button("🤖 Process Email!", type="primary"):
    if not body:
        st.warning("Email body দাও!")
    else:
        email = {
            "sender": sender,
            "subject": subject,
            "body": body
        }

        col1, col2 = st.columns(2)

        with col1:
            with st.spinner("Categorizing..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=50,
                    system="Email category দাও: ORDER/COMPLAINT/INQUIRY/SPAM/OTHER",
                    messages=[{
                        "role": "user",
                        "content": f"Subject: {subject}\nBody: {body[:200]}"
                    }]
                )
                category = response.content[0].text.strip()

            # Category badge
            colors = {
                "ORDER": "🟢",
                "COMPLAINT": "🔴",
                "INQUIRY": "🔵",
                "SPAM": "⚫",
                "OTHER": "🟡"
            }
            emoji = colors.get(category, "🟡")
            st.metric("Category", f"{emoji} {category}")

        with col2:
            priority = "High" if category in ["ORDER", "COMPLAINT"] else "Normal"
            st.metric("Priority", priority)

        # Generate Reply
        with st.spinner("AI reply বানাচ্ছে..."):
            reply_response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
                system="""তুমি Saif's Kids Store customer service।
Professional email reply লেখো।
Products: Map Puzzle ৳450, Drawing Board ৳350, Flash Cards ৳250
Delivery: ঢাকায় ১-২ দিন, বাইরে ৩-৫ দিন""",
                messages=[{
                    "role": "user",
                    "content": f"""Reply দাও:
Subject: {subject}
From: {sender}
Body: {body}
Category: {category}"""
                }]
            )
            reply = reply_response.content[0].text

        st.divider()
        st.markdown("### 📤 AI Generated Reply:")
        st.markdown(reply)

        st.download_button(
            "📥 Reply Download করো",
            data=reply,
            file_name="email_reply.txt"
        )

# ✅ Bulk Email Templates
st.divider()
st.header("📋 Quick Templates")

template_type = st.selectbox(
    "Template Type:",
    [
        "Order Confirmation",
        "Delivery Update",
        "Return Request Response",
        "Product Inquiry Response"
    ]
)

customer_name = st.text_input("Customer Name:", value="ভাই/আপু")

if st.button("📝 Template Generate করো!"):
    with st.spinner("Template বানাচ্ছি..."):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system="তুমি professional email writer। বাংলায় email লেখো।",
            messages=[{
                "role": "user",
                "content": f"""
Template: {template_type}
Customer: {customer_name}
Store: Saif's Kids Store
Products: Map Puzzle ৳450, Drawing Board ৳350, Flash Cards ৳250

Professional email template লেখো:"""
            }]
        )

        st.markdown(response.content[0].text)

        st.download_button(
            "📥 Template Download",
            data=response.content[0].text,
            file_name=f"{template_type}.txt"
        )