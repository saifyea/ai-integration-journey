from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from anthropic import Anthropic
import os
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()


print("📄 Document loading...")


loader = TextLoader("product.txt", encoding="utf-8")
documents = loader.load()


splitter=RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=50)
chunks = splitter.split_documents(documents)


embading=HuggingFaceEmbeddings( model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore=FAISS.from_documents(chunks,embading)
print("vector Store ready")

model=ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
def calculator(name:str,price:int)->str:

    return calculator("flash card",450)
tools=[calculator]
agent=create_agent(
    model=model,
    tools=tools,
    system_prompt="""তুমি বাংলায় উত্তর দাও। সঠিক tool ব্যবহার করে প্রশ্নের উত্তর দাও।"""
    
)

while True:
    user_input = input("\n❓ আপনার প্রশ্ন লিখুন (বা 'exit' লিখে বের হয়ে যান): ")
    if user_input.lower() == "exit":
        print("AI Agent থেকে বিদায়! 👋")
        break

    docs = vectorstore.similarity_search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in docs])  
    prompt = f"""তুমি একজন সহায়ক AI।

    শুধুমাত্র নিচের তথ্য ব্যবহার করে উত্তর দাও।
    যদি তথ্যে উত্তর না থাকে, তাহলে বলো:
    "প্রদত্ত তথ্যে এর উত্তর নেই।"
    বাংলায় উত্তর দাও।
    
    তথ্য:
    {context}
    
    প্রশ্ন: {user_input}
    উত্তর:"""

    try:
        response = agent.invoke(prompt)
        print(response.content)
    except Exception as e:
        print("Error:", e)

