from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

#embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

VECTOR_STORE_PATH = "vectorstore"

#to build vector store with single document
"""
def build_vectorstore():
    print("📄 Building vector store...")
    
    # Step 1 — Document Load
    loader = TextLoader("product_catalog.txt", encoding="utf-8")
    documents = loader.load()
  

    # Step 2 — Text Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=10
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Chunks: {len(chunks)}")


    # Step 3 — Vector Store
    vectorstore = FAISS.from_documents(chunks, embeddings)

     # ✅ Disk এ Save করো
    vectorstore.save_local(VECTOR_STORE_PATH)
    print(f"✅ Saved to: {VECTOR_STORE_PATH}")
    return vectorstore
"""
def build_vectorstore():
    print("📄 Building vector store...")

    # ✅ দুটো file একসাথে load করো
    all_docs = []
    files = ["product_catalog.txt", "store_policy.txt"]

    for file in files:
        if os.path.exists(file):
            loader = TextLoader(file, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"✅ Loaded: {file}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(all_docs)
    print(f"✅ Total Chunks: {len(chunks)}")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_STORE_PATH)
    print(f"✅ Saved to: {VECTOR_STORE_PATH}")
    return vectorstore


def load_vector_store():
      # ✅ Disk থেকে Load করো
    print("📄 Loading vector store...")
    vectorstore = FAISS.load_local(VECTOR_STORE_PATH, embeddings,allow_dangerous_deserialization=True)
    print(f"✅ Loaded from: {VECTOR_STORE_PATH}")
    return vectorstore 
  
    

if os.path.exists(VECTOR_STORE_PATH):
    vectorstore=load_vector_store()    
else:
    vectorstore = build_vectorstore()

def ask_with_score(question):
    # Score সহ search করো
    results = vectorstore.similarity_search_with_score(
        question, k=3
    )

    print(f"\n❓ {question}")
    print("📊 Relevant chunks found:")

    context = ""
    for doc, score in results:
        print(f"   Score: {score:.3f} | {doc.page_content[:60]}...")
        context += doc.page_content + "\n"

    # AI কে জিজ্ঞেস করো
    model = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    prompt = f"""নিচের তথ্য দিয়ে প্রশ্নের উত্তর দাও।
বাংলায় সংক্ষেপে উত্তর দাও।

তথ্য:
{context}

প্রশ্ন: {question}
উত্তর:"""

    response = model.invoke(prompt)
    print(f"✅ উত্তর: {response.content}")
    print("─" * 50)


def load_multiple_docs():
    # একাধিক file load করো
    files = [
        "product_catalog.txt",
        "store_policy.txt",    # নতুন file বানাবো
    ]

    all_docs = []
    for file in files:
        if os.path.exists(file):
            loader = TextLoader(file, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"✅ Loaded: {file}")

    return all_docs


# Test questions with score
questions = [
    "Bangladesh Map Puzzle এর দাম কত?",
    "Flash Cards কত বছরের জন্য?",
    "ডেলিভারি কোথায় পাওয়া যায়?"
]

for q in questions:
    ask_with_score(q)