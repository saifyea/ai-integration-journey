from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ✅ Base Agent Class
class Agent:
    def __init__(self, name, role, instructions):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.memory = []

    def run(self, task, context=""):
        print(f"\n🤖 {self.name} কাজ করছে...")

        messages = []
        if context:
            messages.append({
                "role": "user",
                "content": f"Context:\n{context}"
            })
            messages.append({
                "role": "assistant",
                "content": "Context বুঝেছি। কাজ শুরু করছি।"
            })

        messages.append({
            "role": "user",
            "content": task
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=f"""তুমি {self.name}।
Role: {self.role}
{self.instructions}
বাংলায় উত্তর দাও।""",
            messages=messages
        )

        result = response.content[0].text
        self.memory.append({
            "task": task,
            "result": result
        })

        print(f"✅ {self.name} সম্পন্ন!")
        return result

# ✅ Agent 1 — Market Researcher
researcher = Agent(
    name="Research Agent",
    role="Market Research Specialist",
    instructions="""
তুমি Bangladesh F-commerce market expert।
Product research করো এবং insights দাও।
Competitor analysis করো।
Target audience identify করো।
"""
)

# ✅ Agent 2 — Content Writer
writer = Agent(
    name="Content Agent",
    role="F-commerce Content Writer",
    instructions="""
তুমি Bangladesh এর F-commerce content expert।
Engaging বাংলা content লেখো।
Facebook caption, description, hashtags বানাও।
Emotional triggers ব্যবহার করো।
"""
)

# ✅ Agent 3 — Price Strategist
pricer = Agent(
    name="Pricing Agent",
    role="Pricing Strategy Expert",
    instructions="""
তুমি Bangladesh e-commerce pricing expert।
Competitive pricing strategy দাও।
Profit margin calculate করো।
Discount strategy বানাও।
"""
)

# ✅ Agent 4 — Quality Reviewer
reviewer = Agent(
    name="Review Agent",
    role="Quality Control Specialist",
    instructions="""
তুমি quality control expert।
অন্য agents এর কাজ review করো।
Improvements suggest করো।
Final approval দাও।
"""
)

class SupervisorAgent:
    def __init__(self, agents):
        self.agents = agents
        self.results = {}

    def run_pipeline(self, product_info):
        print("=" * 50)
        print("🎯 Multi-Agent Pipeline শুরু!")
        print("=" * 50)

        # Step 1 — Research
        research = self.agents["researcher"].run(
            task=f"""এই product research করো:
{product_info}

দাও:
1. Target audience
2. Competitor analysis
3. Market opportunity
4. Key selling points"""
        )
        self.results["research"] = research

        # Step 2 — Content (research context সহ)
        content = self.agents["writer"].run(
            task=f"""এই product এর জন্য content বানাও:
{product_info}

দাও:
1. Facebook Caption (৩ লাইন)
2. Product Description (৫ লাইন)
3. ৫টা Hashtag""",
            context=f"Research findings:\n{research}"
        )
        self.results["content"] = content

        # Step 3 — Pricing (research context সহ)
        pricing = self.agents["pricer"].run(
            task=f"""এই product এর pricing strategy দাও:
{product_info}

দাও:
1. Recommended price
2. Discount strategy
3. Bundle offers
4. Profit margin estimate""",
            context=f"Research findings:\n{research}"
        )
        self.results["pricing"] = pricing

        # Step 4 — Review (সব context সহ)
        all_context = f"""
Research: {research}
Content: {content}
Pricing: {pricing}
"""
        review = self.agents["reviewer"].run(
            task=f"""এই product launch plan review করো:
{product_info}

দাও:
1. Overall assessment (১-১০)
2. Content feedback
3. Pricing feedback
4. Improvements
5. Final recommendation""",
            context=all_context
        )
        self.results["review"] = review

        return self.results

    def generate_report(self):
        print("\n" + "=" * 50)
        print("📊 FINAL REPORT")
        print("=" * 50)

        for section, content in self.results.items():
            print(f"\n### {section.upper()} ###")
            print(content)
            print("─" * 40)

        # Save report
        with open("agent_report.json", "w",
                  encoding="utf-8") as f:
            json.dump(self.results, f,
                     ensure_ascii=False, indent=2)
        print("\n✅ Report saved: agent_report.json")


# ✅ Run Pipeline
supervisor = SupervisorAgent({
    "researcher": researcher,
    "writer": writer,
    "pricer": pricer,
    "reviewer": reviewer
})

# Product info
product = """
Product: Bangladesh Map Puzzle
Current Price: ৳450
Description: ৬৪ জেলার wooden educational puzzle
Target: শিশুদের অভিভাবক
"""

results = supervisor.run_pipeline(product)
supervisor.generate_report()