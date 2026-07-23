import os
import streamlit as st
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

#=====setup========#
load_dotenv()

st.set_page_config(
    page_title="বাংলা AI চ্যাটবট",
    page_icon="🤖",
    layout="centered"
)

#CSS
# CSS-এ আরও কিছু স্টাইল যোগ করুন
st.markdown("""
    <style>
        .stChatMessage{border-radius:15px; padding:10px}
        .user-msg{background-color:#e3f2fd}
        .bot-msg{background-color:#f3e5f5}
        .stButton button {
            width: 100%;
            border-radius: 10px;
        }
        .uploaded-files {
            background-color: #f0f8ff;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("বাংলা RAG চ্যাটবট")
st.markdown("**আপনার নিজের ডকুমেন্ট দিয়ে এআই উত্তর দেবে**")
st.divider()

#Sidebar: to upload document
with st.sidebar:
   
    st.header("ডকুমেন্ট আপলোড")
    
    
    uploaded_files = st.file_uploader(
            "PDF/TXT ফাইল আপলোড করুন", type=["pdf","txt"], accept_multiple_files=True,max_upload_size=10
            )
    # ফাইল আপলোডের সময় সাইজ চেক করুন
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    for file in uploaded_files:
        if file.size > MAX_FILE_SIZE:
            st.warning(f"⚠️ {file.name} খুব বড় (সর্বোচ্চ 10MB)")
            continue

    st.divider()
    st.markdown("""
        **কিভাবে কাজ করে**
        1. PDF/TXT ফাইল আপলোড করুন
        2. AI ফাইল পড়ে বুঝবে
        3. প্রশ্ন করুন- ফাইল থেকে উত্তর দেবে
    """)

    if st.button("সব মুছুন"):
        for key in ["messages", "vectorstore", "qa_chain"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    


# memory (বানান সংশোধন করা হয়েছে)
if "messages" not in st.session_state:
    st.session_state.messages = []


# file processing
@st.cache_resource
def process_documents(files):
    """ফাইল পড়ে ভেক্টর ডাটাবেস তৈরি করে"""
    documents = []

    for file in files:
        # ফাইল সেভ করুন
        file_path = f"temp_{file.name}"
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        
        # ফাইল টাইপ অনুযায়ী লোডার
        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        documents.extend(docs)

        # টেম্প ফাইল মুছুন
        os.remove(file_path)
           
    # ছোট chunk-এ ভাগ করুন (লুপের বাইরে নিয়ে আসা হয়েছে ইন্ডেন্টেশন ঠিক করার জন্য)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # প্রতি chunk 500 অক্ষর
        chunk_overlap=50     # 50 অক্ষর ওভারল্যাপ
    )
    chunks = text_splitter.split_documents(documents)
    
    # এমবেডিং (টেক্সট → ভেক্টর)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # ভেক্টর ডাটাবেস তৈরি
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


# ========== QA Chain তৈরি ==========
def create_qa_chain(vectorstore):
    """Claude + RAG চেইন তৈরি"""
    model = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    # ১. প্রম্পট ডিফাইন
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant. Answer the following question based only on the provided context.

    If the question is in Bengali, respond in Bengali. If in English, respond in English.

    <context>
    {context}
    </context>

    Question: {input}
    """)

    # ২. Stuff Documents Chain তৈরি করুন
    question_answer_chain = create_stuff_documents_chain(model, prompt)

    # ৩. ফাইনাল Retrieval Chain তৈরি করুন
    qa_chain = create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k": 3}), 
        question_answer_chain
    )
   
    return qa_chain


# ========== মেইন অ্যাপ ==========
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} টি ফাইল আপলোড হয়েছে!")
    
    # প্রসেসিং
    with st.spinner("📖 ফাইল পড়ছি... এমবেডিং তৈরি করছি..."):
        try:
            if "vectorstore" not in st.session_state:
                vectorstore = process_documents(uploaded_files)
                st.session_state.vectorstore = vectorstore
                st.session_state.qa_chain = create_qa_chain(vectorstore)
                st.success("✅ প্রস্তুত! এখন প্রশ্ন করুন!")
        except Exception as e:
            st.error(f"❌ ভুল: {str(e)}")
            st.stop()
    
    # চ্যাট ইন্টারফেস হিস্ট্রি দেখানো
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # ইনপুট
    prompt = st.chat_input("আপনার ফাইল সম্পর্কে প্রশ্ন করুন...")
    
    if prompt:
        # ইউজার মেসেজ স্ক্রিনে দেখানো
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # AI উত্তর তৈরি
        with st.chat_message("assistant"):
            with st.spinner("🔍 তথ্য খুঁজছি..."):
                try:
                    # নতুন চেইন ইনভোক করার নিয়ম
                    result = st.session_state.qa_chain.invoke({"input": prompt}) 
                    
                    # গুরুত্বপূর্ণ পরিবর্তন: ফলাফল এবং সোর্স ডকুমেন্ট নেওয়ার নতুন নিয়ম
                    answer = result["answer"]
                    sources = result.get("context", [])
                    
                    st.write(answer)
                    
                    # সোর্স বা তথ্যের উৎস দেখান
                    if sources:
                        with st.expander("📄 তথ্যের উৎস (Source Documents)"):
                            for i, doc in enumerate(sources, 1):
                                st.markdown(f"**উৎস {i}:**")
                                st.text(doc.page_content[:300] + "...")
                    
                except Exception as e:
                    st.error(f"❌ ভুল: {str(e)}")
                    answer = "দুঃখিত, উত্তর দিতে পারছি না।"
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer
        })

else:
    st.info("👈 বাম পাশ থেকে PDF বা TXT ফাইল আপলোড করুন!")
    
    # ডেমো দেখান
    st.divider()
    st.subheader("🎯 উদাহরণ:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **আপনার ফাইল:**
        - কোম্পানির পলিসি PDF
        - বইয়ের TXT ফাইল
        - রিপোর্ট/নথি
        """)
    with col2:
        st.markdown("""
        **প্রশ্ন করতে পারেন:**
        - "রিফান্ড পলিসি কী?"
        - "৩য় অধ্যায়ের সারাংশ দাও"
        - "CEO কে?"
        """)
