from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
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

# ✅ Tools (Day 18 থেকে)
@tool
def price_calculator(product_name: str, quantity: int) -> str:
    """Calculate total price for a product and quantity."""
    prices = {
        "bangladesh map puzzle": 450,
        "magic drawing board": 350,
        "flash cards": 250
    }
    price = prices.get(product_name.lower())
    if price is None:
        return f"Product '{product_name}' পাওয়া যায়নি!"
    total = price * quantity
    return f"{product_name}: {price} × {quantity} = {total} টাকা"

@tool
def delivery_time(location: str) -> str:
    """Get delivery time for a location."""
    if "ঢাকা" in location or "dhaka" in location.lower():
        return f"{location}: ১-২ দিনের মধ্যে ডেলিভারি"
    else:
        return f"{location}: ৩-৫ দিনের মধ্যে ডেলিভারি"

# ✅ RAG Setup
VECTOR_STORE_PATH = "vectorstore"
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_or_build():
    if os.path.exists(VECTOR_STORE_PATH):
        print("📂 Loading vector store...")
        return FAISS.load_local(
            VECTOR_STORE_PATH, embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("📄 Building vector store...")
        all_docs = []
        folder_name = "knowledge_base"
        files = ["product_catalog.txt", "store_policy.txt", "faq.txt"]
        
        # FIX 1: Properly loop through the files list
        for file in files:
            # FIX 2: Create a single combined file path string
            file_path = os.path.join(folder_name, file)
            
            if os.path.exists(file_path):
                # FIX 3: Pass the single path string to TextLoader
                loader = TextLoader(file_path, encoding="utf-8")
                all_docs.extend(loader.load())
            else:
                print(f"⚠️ Warning: File not found at {file_path}")
                
        if not all_docs:
            raise FileNotFoundError("Error: No documents were successfully loaded!")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )
        chunks = splitter.split_documents(all_docs)
        vs = FAISS.from_documents(chunks, embeddings)
        vs.save_local(VECTOR_STORE_PATH)
        return vs


vectorstore = load_or_build()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def search_knowledge(query: str) -> str:
    """Search product catalog, store policy and FAQ."""
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)

tools = [price_calculator, delivery_time, search_knowledge]
model_with_tools = model.bind_tools(tools)

# ✅ Memory — Conversation History
chat_history = []

SYSTEM_PROMPT = """তুমি Saif's Kids Store এর AI Assistant।
বাংলায় উত্তর দাও। সংক্ষিপ্ত ও সঠিক উত্তর দাও।

Tools ব্যবহারের নিয়ম:
- দাম জানতে বা হিসাব করতে → price_calculator
- ডেলিভারি জানতে → delivery_time
- বাকি সব প্রশ্নে → search_knowledge"""

def run_agent(user_input: str) -> str:
    # User message history তে যোগ করো
    chat_history.append(HumanMessage(content=user_input))

    # System + History + নতুন message
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + [
        {"role": "human" if isinstance(m, HumanMessage) else "assistant",
         "content": m.content}
        for m in chat_history
    ]

    try:
        # Agent call করো
        response = model_with_tools.invoke(messages)

        # Tool call আছে কিনা দেখো
        if response.tool_calls:
            tool_results = []

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # সঠিক tool খুঁজে run করো
                for t in tools:
                    if t.name == tool_name:
                        result = t.invoke(tool_args)
                        tool_results.append(
                            f"[{tool_name}]: {result}"
                        )
                        break

            # Tool results দিয়ে final response নাও
            tool_context = "\n".join(tool_results)
            final_messages = messages + [
                {"role": "assistant", "content": str(response.content)},
                {"role": "user",
                 "content": f"Tool results:\n{tool_context}\n\nএখন উত্তর দাও।"}
            ]

            final_response = model.invoke(final_messages)
            answer = final_response.content
        else:
            answer = response.content

        # AI response history তে যোগ করো
        chat_history.append(AIMessage(content=answer))
        return answer

    except Exception as e:
        return f"❌ Error: {e}"


# ✅ Interactive Loop
print("🤖 Saif's Kids Store — AI Assistant (with Memory!)")
print("'quit' লিখলে বন্ধ হবে")
print("─" * 50)

while True:
    user_input = input("\n❓ তোমার প্রশ্ন: ")

    if user_input.lower() == "quit":
        print("আল্লাহ হাফেজ! 👋")
        break

    if user_input.strip() == "":
        print("কিছু লেখো!")
        continue

    response = run_agent(user_input)
    print(f"✅ {response}")
    print("─" * 50)