#custom ai agent for Saif's Kids Store

from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver #for conversation memory
import os
import math

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ✅ Tool 1 - Calculator with docstring
@tool
def Calculator(expression: str) -> str:
    """Calculate mathematical expressions. Takes a mathematical expression as string and returns the result."""
    try:
        allowed = {__builtins__: None}
        allowed.update({name: getattr(math, name) for name in dir(math) if not name.startswith("_")})
        result = eval(expression, allowed)
        return f"Result: {result}"
    except:
        return "Invalid expression."

# Tool 2 - Bangla Info with docstring
@tool
def bangla_info(query: str) -> str:
    """Get information about Bangladesh related topics. Takes a query string and returns relevant information from the database."""
    info_db = {
        "ঢাকা": "ঢাকা বাংলাদেশের রাজধানী",
        "বাংলাদেশ": "বাংলাদেশ দক্ষিণ এশিয়ার একটি ছোট দেশ, যা 1971 সালে স্বাধীন হয়",
        "পাইথন": "পাইথন একটি জনপ্রিয় প্রোগ্রামিং ভাষা"
    }
    return info_db.get(query, f"{query} সম্পর্কে ডাটাবেজে তথ্য নেই")



#for rag
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

#to save
VECTOR_STORE_PATH = "vectorstore"
embedding=HuggingFaceEmbeddings( model_name="sentence-transformers/all-MiniLM-L6-v2")
def load_or_build():
    if os.path.exists(VECTOR_STORE_PATH):
        print("📂 Loading vector store...")
        return FAISS.load_local(
            VECTOR_STORE_PATH, embedding,
            allow_dangerous_deserialization=True
        )
    else:
        print("📄 Document loading...")
        loader=TextLoader("product.txt",encoding="utf-8")
        documents=loader.load()
        splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        chunk=splitter.split_documents(documents)
        
        vectorstore=FAISS.from_documents(chunk,embedding)
        vectorstore.save_local(VECTOR_STORE_PATH)
        print("vectorstore saved")
vectorstore=load_or_build()
# ============ RAG Function ============
def get_all_product_info():
    """সব পণ্যের তথ্য একসাথে নেওয়া"""
    docs = vectorstore.similarity_search("সব পণ্য", k=10)  # সব পণ্য পেতে
    if not docs:
        return "পণ্যের তথ্য পাওয়া যায়নি"
    
    # ডুপ্লিকেট রিমুভ করে ইউনিক পণ্য দেখানো
    seen = set()
    unique_products = []
    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_products.append(doc.page_content)
    
    return "\n\n".join(unique_products[:5])  # প্রথম ৫টি পণ্য
all_products_info=get_all_product_info()

def get_product_info_by_query(query):
    """নির্দিষ্ট প্রশ্নের জন্য পণ্য খোঁজা"""
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return None
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def product_search(query: str) -> str:
    """Search products from Saif's Kids Store."""
    result = get_product_info_by_query(query)
    if result:
        return f"প্রাসঙ্গিক পণ্য:\n\n{result}"
    return "এই সম্পর্কে কোনো পণ্য পাওয়া যায়নি"

#for google search
# Try importing Google search (handle if not installed)
try:
    from googlesearch import search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False
    print("⚠️ googlesearch-python not installed. Install with: pip install googlesearch-python")


from tavily import TavilyClient
@tool
def google_search(query: str) -> str:
    """Search the internet for real-time information using Tavily."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query, max_results=3)
        
        results = response.get("results", [])
        if not results:
            return "কোনো ফলাফল পাওয়া যায়নি"
        
        output = []
        for i, result in enumerate(results[:3], 1):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            output.append(f"{i}. {title}\n   {content}\n   {url}")
        
        return "\n\n".join(output)
    except Exception as e:
        return f"সার্চ করা সম্ভব হয়নি: {str(e)}"
    
tools = [Calculator, bangla_info, product_search,google_search]

system_prompt = f"""তুমি Saif's Kids Store এর AI Assistant। 

আমাদের স্টোরের পণ্য সম্পর্কে তথ্য:
{all_products_info}

রিটার্ন পলিসি:
পণ্য পাওয়ার ৭ দিনের মধ্যে return করা যাবে।
পণ্য অবশ্যই অব্যবহৃত এবং original packaging এ থাকতে হবে।

ওয়ারেন্টি পলিসি:
সব পণ্যে ৩০ দিনের ওয়ারেন্টি আছে।
পণ্য নষ্ট হলে বিনামূল্যে replace করা হবে।

পেমেন্ট পদ্ধতি:
bKash, Nagad, রকেট এবং ক্যাশ অন ডেলিভারি।

ডেলিভারি সময়:
ঢাকায়: ১-২ দিন
ঢাকার বাইরে: ৩-৫ দিন

যোগাযোগ:
Facebook: Saif's Kids Store
Phone: 01XXXXXXXXX

তোমার কাজ:
1. পণ্য সম্পর্কিত প্রশ্নের জন্য product_search tool ব্যবহার করো
2. অংক করার জন্য Calculator tool ব্যবহার করো
3. বাংলা তথ্যের জন্য bangla_info tool ব্যবহার করো
4. বাস্তব সময়ের তথ্য, খবর বা স্টোরে না থাকা বিষয়ের জন্য google_search tool ব্যবহার করো
5. সব সময় বাংলায় উত্তর দাও
6. বাচ্চাদের মতো সহজ ভাষায় উত্তর দাও

যদি কোনো পণ্যের বিস্তারিত জানতে চাও, product_search tool ব্যবহার করো।
যদি স্টোরের বাইরের কোনো তথ্য জানতে চাও, google_search tool ব্যবহার করো।"""

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    
])
# Simple conversation memory
memory = MemorySaver() # This stores conversation history

# Create the agent
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt,
    checkpointer=memory,  # This enables memory
)



# Direct user input
print("─" * 50)
print("\n🤖 AI Agent Interactive Mode:")
print("─" * 50)

# ✅ Create a thread ID to maintain conversation
thread_id = "saif_store_chat"
config = {"configurable": {"thread_id": thread_id}}


while True:
    user_input = input("\n❓ আপনার প্রশ্ন লিখুন (বা 'exit' লিখে বের হয়ে যান): ")
    if user_input.lower() == "exit":
        print("AI Agent থেকে বিদায়! 👋")
        break

    try:
        result = agent.invoke(
            {"messages": [ ("user", user_input)]},
            config=config  # ✅ Always pass the config with thread_id
        )
        print(f"✅ {result['messages'][-1].content}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("─" * 50)