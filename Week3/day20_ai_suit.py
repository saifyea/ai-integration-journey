import os
import sys
from dotenv import load_dotenv

load_dotenv()

def print_header():
    print("\n" + "=" * 50)
    print("🤖 Saif's Kids Store — Complete AI Suite")
    print("   Powered by Claude AI + LangChain")
    print("=" * 50)

def print_menu():
    print("\n📋 কী করতে চাও?")
    print("─" * 40)
    print("1. 📝 Product Content Generator")
    print("2. 💬 F-commerce Chatbot")
    print("3. 🔍 RAG Knowledge Base Q&A")
    print("4. 🤖 AI Agent Assistant")
    print("5. 🚪 Exit")
    print("Type quit to🚪 Exit progem in any stage")
    print("─" * 40)

# ✅ Module 1 — Product Content Generator
def run_content_generator():
    print("\n📝 Product Content Generator")
    print("─" * 40)

    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    products = [
        {"name": "Bangladesh Map Puzzle", "price": 450, "target": "শিশুদের অভিভাবক"},
        {"name": "Magic Drawing Board", "price": 350, "target": "৫-১০ বছরের শিশু"},
        {"name": "Flash Cards", "price": 250, "target": "৩-৬ বছরের শিশু"}
    ]

    for product in products:
        print(f"\n⏳ Generating: {product['name']}...")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system="তুমি F-commerce expert। বাংলায় ২-৩ লাইনের caption লেখো।",
            messages=[{
                "role": "user",
                "content": f"পণ্য: {product['name']}, দাম: {product['price']} টাকা"
            }]
        )
        print(f"✅ {response.content[0].text}")
        print("─" * 40)

# ✅ Module 2 — F-commerce Chatbot
def run_chatbot():
    print("\n💬 F-commerce Chatbot")
    print("'back' লিখলে menu তে ফিরবে")
    print("─" * 40)

    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    history = []

    while True:
        user_input = input("\nতুমি: ")
        if user_input.lower() == "back":
            break

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system="""তুমি Saif's Kids Store এর assistant। বাংলায় উত্তর দাও।

                আমাদের products:
                ১. Bangladesh Map Puzzle — ৪৫০ টাকা, বয়স ৫-১২ বছর
                ২. Magic Drawing Board — ৩৫০ টাকা, বয়স ৩-১০ বছর
                ৩. Flash Cards — ২৫০ টাকা, বয়স ৩-৬ বছর, ৩০টি কার্ড

                Delivery: ঢাকায় ১-২ দিন, বাইরে ৩-৫ দিন
                Return: ৭ দিনের মধ্যে
                Order: Facebook page এ message করুন""",
            messages=history
        )

        ai_response = response.content[0].text
        history.append({"role": "assistant", "content": ai_response})
        print(f"AI: {ai_response}")

# ✅ Module 3 — RAG Knowledge Base
def run_rag():
    print("\n🔍 RAG Knowledge Base Q&A")
    print("'back' লিখলে menu তে ফিরবে")
    print("─" * 40)

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain_anthropic import ChatAnthropic

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        if os.path.exists("vectorstore"):
            vectorstore = FAISS.load_local(
                "vectorstore", embeddings,
                allow_dangerous_deserialization=True
            )
            print("✅ Knowledge base loaded!")
        else:
            print("❌ vectorstore নেই! আগে RAG system run করো।")
            return

        model = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        while True:
            question = input("\n❓ প্রশ্ন: ")
            if question.lower() == "back":
                break

            docs = vectorstore.similarity_search(question, k=3)
            context = "\n".join([doc.page_content for doc in docs])

            response = model.invoke(
                f"তথ্য:\n{context}\n\nপ্রশ্ন: {question}\nবাংলায় উত্তর:"
            )
            print(f"✅ {response.content}")

    except ImportError:
        print("❌ LangChain install করো!")

# ✅ Module 4 — AI Agent
def run_agent():
    print("\n🤖 AI Agent Assistant")
    print("'back' লিখলে menu তে ফিরবে")
    print("─" * 40)

    try:
        from langchain_anthropic import ChatAnthropic
        from langchain_core.tools import tool
        from langchain_core.messages import HumanMessage, AIMessage

        model = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        @tool
        def price_calculator(product_name: str, quantity: int) -> str:
            """Calculate total price."""
            prices = {
                "bangladesh map puzzle": 450,
                "magic drawing board": 350,
                "flash cards": 250
            }
            price = prices.get(product_name.lower(), 0)
            if price == 0:
                return f"Product পাওয়া যায়নি!"
            return f"{product_name}: {price} × {quantity} = {price * quantity} টাকা"

        @tool
        def delivery_time(location: str) -> str:
            """Get delivery time."""
            if "ঢাকা" in location:
                return f"{location}: ১-২ দিন"
            return f"{location}: ৩-৫ দিন"

        tools = [price_calculator, delivery_time]
        model_with_tools = model.bind_tools(tools)
        history = []

        while True:
            user_input = input("\n❓ তোমার প্রশ্ন: ")
            if user_input.lower() == "back":
                break

            history.append(HumanMessage(content=user_input))
            messages = [
                {"role": "system",
                 "content": "তুমি Saif's Kids Store এর AI Assistant। বাংলায় উত্তর দাও।"}
            ] + [
                {"role": "human" if isinstance(m, HumanMessage) else "assistant",
                 "content": m.content}
                for m in history
            ]

            response = model_with_tools.invoke(messages)

            if response.tool_calls:
                tool_results = []
                for tc in response.tool_calls:
                    for t in tools:
                        if t.name == tc["name"]:
                            result = t.invoke(tc["args"])
                            tool_results.append(result)

                final = model.invoke(
                    messages + [
                        {"role": "assistant", "content": str(response.content)},
                        {"role": "user",
                         "content": f"Tool: {', '.join(tool_results)}\nউত্তর দাও।"}
                    ]
                )
                answer = final.content
            else:
                answer = response.content

            history.append(AIMessage(content=answer))
            print(f"✅ {answer}")

    except ImportError:
        print("❌ LangChain install করো!")

# ✅ Main Program
def main():
    print_header()

    while True:
        print_menu()
        choice = input("\n👉 তোমার choice (1-5): ").strip()

        if choice == "1":
            run_content_generator()
        elif choice == "2":
            run_chatbot()
        elif choice == "3":
            run_rag()
        elif choice == "4":
            run_agent()
        elif choice == "5":
            print("\n🙏 আল্লাহ হাফেজ! 👋")
            break
        elif choice.lower() == "quit":
            print("আল্লাহ হাফেজ! 👋")
            break
        else:
            print("❌ ১-৫ এর মধ্যে লেখো!")

main()
