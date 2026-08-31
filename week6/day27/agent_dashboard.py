import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import time

load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

st.set_page_config(
    page_title="Multi-Agent AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent AI System")
st.caption("Multiple AI agents একসাথে কাজ করে!")

# Product Input
st.header("📦 Product Information")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input(
        "Product Name:",
        value="Bangladesh Map Puzzle"
    )
    price = st.number_input("Price (৳):", value=450)
    description = st.text_area(
        "Description:",
        value="৬৪ জেলার wooden educational puzzle"
    )

with col2:
    target = st.text_input(
        "Target Audience:",
        value="শিশুদের অভিভাবক"
    )
    category = st.selectbox(
        "Category:",
        ["Educational", "Toy", "Book", "Art & Craft"]
    )

    st.info("""
    **Agents:**
    🔍 Research Agent
    ✍️ Content Agent
    💰 Pricing Agent
    ✅ Review Agent
    """)

if st.button("🚀 Launch Multi-Agent Pipeline!", type="primary"):
    product_info = f"""
Product: {product_name}
Price: ৳{price}
Description: {description}
Target: {target}
Category: {category}
"""

    # Progress bar
    progress = st.progress(0)
    status = st.empty()

    results = {}

    def run_agent(name, role, instructions, task, context=""):
        messages = []
        if context:
            messages.extend([
                {"role": "user", "content": f"Context:\n{context}"},
                {"role": "assistant", "content": "বুঝেছি।"}
            ])
        messages.append({"role": "user", "content": task})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=f"তুমি {name}। Role: {role}\n{instructions}\nবাংলায় উত্তর দাও।",
            messages=messages
        )
        return response.content[0].text

    # Agent 1 — Research
    status.info("🔍 Research Agent কাজ করছে...")
    progress.progress(25)
    results["research"] = run_agent(
        "Research Agent",
        "Market Research Specialist",
        "Bangladesh F-commerce market expert।",
        f"Product research করো:\n{product_info}\n\n1. Target audience\n2. Competitors\n3. Selling points"
    )

    # Agent 2 — Content
    status.info("✍️ Content Agent কাজ করছে...")
    progress.progress(50)
    results["content"] = run_agent(
        "Content Agent",
        "F-commerce Content Writer",
        "Engaging বাংলা content লেখো।",
        f"Content বানাও:\n{product_info}\n\n1. Caption\n2. Description\n3. Hashtags",
        context=results["research"]
    )

    # Agent 3 — Pricing
    status.info("💰 Pricing Agent কাজ করছে...")
    progress.progress(75)
    results["pricing"] = run_agent(
        "Pricing Agent",
        "Pricing Strategy Expert",
        "Competitive pricing strategy দাও।",
        f"Pricing strategy:\n{product_info}\n\n1. Price recommendation\n2. Discounts\n3. Bundle offers",
        context=results["research"]
    )

    # Agent 4 — Review
    status.info("✅ Review Agent কাজ করছে...")
    progress.progress(90)
    all_context = f"Research: {results['research']}\nContent: {results['content']}\nPricing: {results['pricing']}"
    results["review"] = run_agent(
        "Review Agent",
        "Quality Control Specialist",
        "সব agents এর কাজ review করো।",
        f"Review করো:\n{product_info}\n\n1. Score (১-১০)\n2. Feedback\n3. Recommendation",
        context=all_context
    )

    progress.progress(100)
    status.success("✅ সব Agents সম্পন্ন!")

    # Results দেখাও
    st.divider()
    st.header("📊 Agent Results")

    tabs = st.tabs([
        "🔍 Research",
        "✍️ Content",
        "💰 Pricing",
        "✅ Review"
    ])

    with tabs[0]:
        st.markdown(results["research"])
    with tabs[1]:
        st.markdown(results["content"])
    with tabs[2]:
        st.markdown(results["pricing"])
    with tabs[3]:
        st.markdown(results["review"])

    # Download
    import json
    st.download_button(
        "📥 Full Report Download",
        data=json.dumps(results, ensure_ascii=False, indent=2),
        file_name="agent_report.json",
        mime="application/json"
    )