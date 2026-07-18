from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()
embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

VECTOR_STORE_PATH="vectorstore"
def build_vectorstore():
    print("📄 Building vector store...")

    # ✅ দুটো file একসাথে load করো
    all_docs = []
    files = ["product_catalog.txt", "store_policy.txt","faq.txt"]

    for file in files:
        if os.path.exists(file):
            loader = TextLoader(file, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"✅ Loaded: {file}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=10
    )
    chunks = splitter.split_documents(all_docs)
    print(f"✅ Chunks: {len(chunks)}")

    # Step 3 — Vector Store
   
    vectorstore = FAISS.from_documents(chunks, embeddings)

     # ✅ Disk এ Save করো
    vectorstore.save_local(VECTOR_STORE_PATH)
    print(f"✅ Saved to: {VECTOR_STORE_PATH}")
    return vectorstore



#load vector store from disk
def load_vectorstore():
    vectorstore = FAISS.load_local(VECTOR_STORE_PATH, embeddings,allow_dangerous_deserialization=True)
    print(f"✅ Loaded vector store from: {VECTOR_STORE_PATH}")
    return vectorstore

if os.path.exists(VECTOR_STORE_PATH):
    vectorstore = load_vectorstore()
else:
    vectorstore = build_vectorstore()

# Step 3 — Interactive Loop
print("🤖 RAG Chatbot চালু!")
model = ChatAnthropic(  model="claude-haiku-4-5-20251001", api_key=os.getenv("ANTHROPIC_API_KEY"))
while True:
    
    question = input("তোমার প্রশ্ন: ")
    if question.lower() == "quit":
        print("Chatbot বন্ধ হচ্ছে! আল্লাহ হাফেজ 👋")
        break
    
    # Search করো
    docs = vectorstore.similarity_search(question, k=3)
    context=""
    sources= []
    for doc in docs:
        context+=doc.page_content+"\n"
        source=doc.metadata.get("source", "unknown")
        sources.append(source)
       
    
    prompt = f"""বাংলায় সংক্ষেপে নিচের তথ্য দিয়ে প্রশ্নের উত্তর দাও।
            তথ্য: {context}
            প্রশ্ন: {question}
            উত্তর:"""
    
    response = model.invoke(prompt)
    print(f"✅ উত্তর: {response.content}")
    print(f"📂 Source: {', '.join(set(sources))}")
    print("─" * 50)

