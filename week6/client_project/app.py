# app.py
import streamlit as st
from anthropic import Anthropic
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import *
import os

# ✅ API Setup
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = ANTHROPIC_API_KEY

client = Anthropic(api_key=api_key)

# ✅ Page Config
st.set_page_config(
    page_title=f"{BUSINESS_NAME} AI",
    page_icon="🤖",
    layout="wide"
)

# ✅ RAG Setup
@st.cache_resource
def setup_rag():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists("vectorstore"):
        return FAISS.load_local(
            "vectorstore", embeddings,
            allow_dangerous_deserialization=True
        )

    all_docs = []
    for file in ["data/products.txt",
                 "data/faq.txt",
                 "data/policy.txt"]:
        if os.path.exists(file):
            loader = TextLoader(file, encoding="utf-8")
            all_docs.extend(loader.load())

    if all_docs:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )
        chunks = splitter.split_documents(all_docs)
        vs = FAISS.from_documents(chunks, embeddings)
        vs.save_local("vectorstore")
        return vs
    return None

vectorstore = setup_rag()

# ✅ UI
st.title(f"🤖 {BUSINESS_NAME}")
st.caption(f"AI Customer Service — {APP_VERSION}")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(f"**{BUSINESS_NAME}**")
    st.markdown(f"📞 {BUSINESS_CONTACT}")
    st.divider()

    st.header("🛍️ Products")
    for name, info in PRODUCTS.items():
        status = "✅" if info["stock"] else "❌"
        st.markdown(
            f"{status} **{name.title()}**\n"
            f"৳{info['price']} | {info['age']}"
        )

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat
st.header("💬 Chat with AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"আস্সালামু আলাইকুম! 👋 আমি {BUSINESS_NAME} এর AI Assistant। কীভাবে সাহায্য করতে পারি?"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Quick buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("💰 দাম জানো"):
        st.session_state.quick = "সব products এর দাম বলো"
with col2:
    if st.button("🚚 Delivery"):
        st.session_state.quick = "Delivery কতদিনে?"
with col3:
    if st.button("📦 Products"):
        st.session_state.quick = "সব products দেখাও"
with col4:
    if st.button("↩️ Return"):
        st.session_state.quick = "Return policy কী?"

if "quick" in st.session_state and st.session_state.quick:
    user_msg = st.session_state.quick
    st.session_state.quick = None

    # Get context from RAG
    context = ""
    if vectorstore:
        docs = vectorstore.similarity_search(user_msg, k=3)
        context = "\n".join([d.page_content for d in docs])

    # Products info
    products_info = "\n".join([
        f"- {n.title()}: ৳{i['price']}, {i['age']}"
        for n, i in PRODUCTS.items()
    ])

    st.session_state.messages.append(
        {"role": "user", "content": user_msg}
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=f"""তুমি {BUSINESS_NAME} এর AI Assistant।
বাংলায় friendly ভাবে উত্তর দাও।

Products:
{products_info}

Knowledge Base:
{context}

Contact: {BUSINESS_CONTACT}""",
        messages=st.session_state.messages
    )

    ai_resp = response.content[0].text
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_resp}
    )
    st.rerun()

# Chat input
if prompt := st.chat_input("প্রশ্ন করো..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

    # RAG context
    context = ""
    if vectorstore:
        docs = vectorstore.similarity_search(prompt, k=3)
        context = "\n".join([d.page_content for d in docs])

    products_info = "\n".join([
        f"- {n.title()}: ৳{i['price']}, {i['age']}"
        for n, i in PRODUCTS.items()
    ])

    with st.chat_message("assistant"):
        with st.spinner("ভাবছি..."):
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=f"""তুমি {BUSINESS_NAME} এর AI Assistant।
বাংলায় উত্তর দাও।

Products:
{products_info}

Knowledge Base:
{context}

Contact: {BUSINESS_CONTACT}""",
                messages=st.session_state.messages
            )
            ai_resp = response.content[0].text
            st.write(ai_resp)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_resp}
    )