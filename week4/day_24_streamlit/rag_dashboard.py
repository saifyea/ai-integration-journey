import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="RAG Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 RAG Knowledge Base Dashboard")
st.caption("Document upload করো — AI তোমার document থেকে উত্তর দেবে!")

# ✅ Embeddings setup
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

@st.cache_resource
def get_model():
    return ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

embeddings = get_embeddings()
model = get_model()

# Sidebar — Document Upload
with st.sidebar:
    st.header("📄 Documents")

    # File uploader
    uploaded_file = st.file_uploader(
        "TXT file upload করো:",
        type=["txt"]
    )

    if uploaded_file:
        # Save uploaded file
        with open("uploaded_doc.txt", "wb") as f:
            f.write(uploaded_file.getvalue())

        if st.button("📚 Process করো!", type="primary"):
            with st.spinner("Document processing..."):
                loader = TextLoader(
                    "uploaded_doc.txt",
                    encoding="utf-8"
                )
                docs = loader.load()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100
                )
                chunks = splitter.split_documents(docs)

                vectorstore = FAISS.from_documents(
                    chunks, embeddings
                )
                vectorstore.save_local("rag_vectorstore")

                st.success(f"✅ {len(chunks)} chunks processed!")
                st.session_state.rag_ready = True

    # Default store
    if os.path.exists("vectorstore"):
        st.info("✅ Kids Store knowledge base ready!")
        if st.button("Kids Store KB Load করো"):
            st.session_state.use_default = True

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Document upload করো")
    st.markdown("2. Process করো")
    st.markdown("3. প্রশ্ন করো!")

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("❓ প্রশ্ন করো")

    question = st.text_area(
        "তোমার প্রশ্ন লেখো:",
        height=100,
        placeholder="যেকোনো প্রশ্ন করো..."
    )

    if st.button("🔍 উত্তর খোঁজো!", type="primary"):
        if not question:
            st.warning("প্রশ্ন লেখো!")
        else:
            # Load vectorstore
            vs_path = None
            if os.path.exists("rag_vectorstore"):
                vs_path = "rag_vectorstore"
            elif os.path.exists("vectorstore"):
                vs_path = "vectorstore"

            if vs_path:
                with st.spinner("Knowledge base search করছি..."):
                    vectorstore = FAISS.load_local(
                        vs_path, embeddings,
                        allow_dangerous_deserialization=True
                    )

                    # Search
                    results = vectorstore.similarity_search_with_score(
                        question, k=3
                    )

                    context = "\n".join([
                        doc.page_content for doc, _ in results
                    ])

                    # AI answer
                    response = model.invoke(
                        f"""তথ্য:
{context}

প্রশ্ন: {question}
বাংলায় সংক্ষেপে উত্তর দাও:"""
                    )

                    st.success("✅ উত্তর পাওয়া গেছে!")
                    st.markdown("### 🤖 AI উত্তর:")
                    st.markdown(response.content)

                    # Sources
                    with st.expander("📄 Sources দেখো"):
                        for i, (doc, score) in enumerate(results):
                            st.markdown(f"**Source {i+1}** (Score: {score:.3f})")
                            st.text(doc.page_content[:200] + "...")
                            st.divider()
            else:
                st.error("❌ কোনো document নেই! আগে upload করো।")

with col2:
    st.header("📊 Stats")

    if os.path.exists("vectorstore"):
        st.metric("Kids Store KB", "✅ Ready")
    else:
        st.metric("Kids Store KB", "❌ Not Found")

    if os.path.exists("rag_vectorstore"):
        st.metric("Uploaded Doc", "✅ Ready")
    else:
        st.metric("Uploaded Doc", "❌ Not Found")

    st.divider()
    st.markdown("**Quick Questions:**")
    quick_questions = [
        "Flash Cards এর দাম কত?",
        "Delivery কতদিনে?",
        "Return policy কী?"
    ]

    for q in quick_questions:
        if st.button(q, key=q):
            st.session_state.quick_q = q