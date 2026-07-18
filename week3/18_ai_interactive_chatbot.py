#Interactive ai agent for Saif's Kids Store

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


import os

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ✅ Tool 1 — Price Calculator
@tool
def price_calculator(product_name: str,quantity:int) -> str:
    """Calculate total price for a product and quantity."""
    prices={
        "bangladesh map puzzle": 450,
        "magic drawing board": 350,
        "flash cards": 250
    }
    price = prices.get(product_name.lower())
    if price is None:
        return f"Product '{product_name}' পাওয়া যায়নি!"

    total = price * quantity
    return f"{product_name}: {price} × {quantity} = {total} টাকা"

# ✅ Tool 2 — Delivery Time
@tool
def delivery_time(location: str) -> str:
    """Get delivery time for a location."""
    if "ঢাকা" in location or "Dhaka" in location:
        return f"{location}: ১-২ দিনের মধ্যে ডেলিভারি"
    else:
        return f"{location}: ৩-৫ দিনের মধ্যে ডেলিভারি"





VECTOR_STORE_PATH="vectorstore"
embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
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

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
# ✅ Tool 3 — Product Info
@tool
def search_products(query: str) -> str:
    """Search the product catalog."""

    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)
# ✅ Tools List

tools = [price_calculator, delivery_time, search_products]


# Agent বানাও
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""তুমি Saif's Kids Store এর AI Assistant। বাংলায় উত্তর দাও।
                সঠিক tool ব্যবহার করে প্রশ্নের উত্তর দাও।
                
                যদি পণ্যের তথ্য, FAQ বা Store Policy সম্পর্কে প্রশ্ন হয়,
                search_products tool ব্যবহার করবে।
                
                যদি দাম হিসাব করতে হয়,
                price_calculator tool ব্যবহার করবে।

                যদি ডেলিভারি সম্পর্কে প্রশ্ন হয়,
                delivery_time tool ব্যবহার করবে।

                উত্তর সংক্ষিপ্ত, ভদ্র ও সঠিক হবে।
            """
)


# Step 3 — Interactive Loop
print("🤖 RAG Interactive Chatbot চালু!")
while True:
    user_input = input("\n❓ আপনার প্রশ্ন লিখুন (বা 'exit' লিখে বের হয়ে যান): ")
    if user_input.lower() == "exit":
        print("AI Agent থেকে বিদায়! 👋")
        break

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    print(f"✅ {result['messages'][-1].content}")
    print("─" * 50)


