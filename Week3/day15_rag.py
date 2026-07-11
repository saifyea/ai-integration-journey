from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1 — Document Load
print("📄 Document loading...")
loader = TextLoader("product_catalog.txt", encoding="utf-8")
documents = loader.load()
print(f"✅ Loaded: {len(documents)} document")

# Step 2 — Text Split
print("✂️ Splitting text...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"✅ Chunks: {len(chunks)}")

# Step 3 — Embeddings
print("🔢 Creating embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 4 — Vector Store
print("🗄️ Creating vector store...")
vectorstore = FAISS.from_documents(chunks, embeddings)
print("✅ Vector store ready!")

# Step 5 — Model
model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Step 6 — RAG Function
def ask(question):
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""নিচের তথ্য দিয়ে প্রশ্নের উত্তর দাও।
বাংলায় উত্তর দাও।

তথ্য:
{context}

প্রশ্ন: {question}
উত্তর:"""

    response = model.invoke(prompt)
    return response.content

# Step 7 — Test
print("\n🤖 Saif's Kids Store AI Assistant")
print("─" * 40)

questions = [
    "Bangladesh Map Puzzle এর দাম কত?",
    "কোন product টা ৩-৬ বছরের শিশুদের জন্য?",
    "Magic Drawing Board এর বিশেষত্ব কী?",
    "ডেলিভারি কোথায় পাওয়া যায়?"
]

for question in questions:
    print(f"\n❓ {question}")
    answer = ask(question)
    print(f"✅ {answer}")
    print("─" * 40)
