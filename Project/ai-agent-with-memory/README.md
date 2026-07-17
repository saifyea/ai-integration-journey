# 🤖 RAG-powered AI Customer Support Agent with Memory

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-orange)
![RAG](https://img.shields.io/badge/RAG-Enabled-success)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

An intelligent AI customer support agent built with **Python**, **Anthropic Claude API**, **Retrieval-Augmented Generation (RAG)**, and **Conversational Memory**.

The agent answers customer questions by retrieving information from a custom knowledge base (product catalog, FAQs, and store policies) while remembering previous conversations to provide more natural and context-aware responses.

---

## 🚀 Project Overview

This project simulates a real-world AI customer support assistant for an online business.

Instead of relying only on an LLM, the agent:

- Retrieves relevant business information from a custom knowledge base.
- Maintains conversation history during the session.
- Generates accurate, context-aware responses using Claude.
- Reduces hallucinations by grounding responses in business data.
---

## ✨ Features

- 🤖 AI-powered customer support assistant
- 🧠 Conversational memory for multi-turn interactions
- 📚 Retrieval-Augmented Generation (RAG)
- 🛍️ Product catalog search
- ❓ FAQ retrieval
- 📜 Store policy lookup
- 💬 Context-aware responses using Claude API
- ⚡ Fast and interactive command-line interface
- 🔒 Secure API key management with `.env`

---

## 🏗️ System Architecture

```text
                User Question
                      │
                      ▼
        Load Conversation History
                      │
                      ▼
      Search Knowledge Base (RAG)
      ├── Product Catalog
      ├── FAQ
      └── Store Policy
                      │
                      ▼
      Build Context + Conversation
                      │
                      ▼
          Anthropic Claude API
                      │
                      ▼
            AI Generated Response
                      │
                      ▼
      Update Conversation Memory
```

---

## 📁 Project Structure

```text
ai-agent-with-memory/
│
├── README.md
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── knowledge_base/
│   ├── product_catalog.txt  BD Bangla
│   ├── faq.txt              BD Bangla
│   └── store_policy.txt     BD Bangla
│
└── assets/
    └── demo.png
```
---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/saifyea/ai-agent-with-memory.git
```

Navigate into the project folder:

```bash
cd ai-agent-with-memory
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Anthropic API key.

---

## ▶️ Run the Application

```bash
python main.py
```

## 🌐 Language Support

This AI Agent demonstrates RAG capabilities using Bengali business knowledge sources.

The knowledge base contains real-world business information written in Bengali:

- 🇧🇩 Product catalog
- 🇧🇩 Frequently Asked Questions (FAQ)
- 🇧🇩 Store policies

The agent can retrieve Bengali information and generate context-aware responses using an LLM.

---

## 💬 Example Conversation

The AI Agent can answer customer queries using information retrieved from the Bengali knowledge base while maintaining conversation context.

### 🛍️ Product Query

**User:**
```
Flash Cards এর দাম কত?
```

**AI Agent:**
```
Flash Cards এর দাম: ২৫০ টাকা

বৈশিষ্ট্য:
- বয়স: ৩-৬ বছর
- ৩০টি রঙিন কার্ড প্রতিটি সেটে
- বর্ণমালা, সংখ্যা, ফল, প্রাণী শেখায়
- টেকসই laminated কার্ড
```

---

### 🧠 Memory-based Follow-up Question

**User:**
```
৩টা কিনলে কত লাগবে?
```

**AI Agent:**
```
৩টা Flash Cards এর মোট দাম: ৭৫০ টাকা
(২৫০ টাকা × ৩ = ৭৫০ টাকা)
```

The agent understands the previous conversation context and answers based on the previous product discussion.

---

### 📦 Delivery Information

**User:**
```
সিলেটে delivery কতদিনে?
```

**AI Agent:**
```
সিলেটে ডেলিভারি: ৩-৫ দিনের মধ্যে।

আপনার Flash Cards অর্ডার করলে ৩-৫ দিনের মধ্যে পৌঁছে যাবে।
```

---

### 🔄 Policy Retrieval

**User:**
```
Return policy কী?
```

**AI Agent:**
```
Saif's Kids Store এর Return Policy:

- ৭ দিনের মধ্যে রিটার্ন করা যাবে
- পণ্য অবশ্যই অব্যবহৃত থাকতে হবে
- Original packaging এ থাকতে হবে
```

---

This demonstrates:

✅ RAG-based knowledge retrieval  
✅ Conversational memory  
✅ Bengali language support  
✅ Business-specific AI assistance

---

## 🎯 Learning Outcomes

Through this project, I gained practical experience in building AI-powered applications using modern Generative AI techniques.

Key learnings:

- Building AI Agents with LLM APIs
- Implementing Retrieval-Augmented Generation (RAG)
- Managing conversational memory
- Working with custom knowledge bases
- Designing business-focused AI solutions
- Prompt engineering for accurate responses
- Integrating AI into real-world workflows

---

## 🔮 Future Improvements

Planned improvements for this project:

- 🗄️ Add vector database integration (FAISS / ChromaDB)
- 🧠 Implement long-term persistent memory
- 🔧 Add tool calling capabilities
- 🌐 Build a web interface using Streamlit
- 📊 Add analytics for customer interactions
- 🎙️ Add voice-based interaction
- ☁️ Deploy as a cloud-based AI customer support service

---

## 👨‍💻 Author

**Saifuddin Yeahea**

AI Integration Specialist | Python | RAG | AI Agents

I combine 17+ years of enterprise IT experience with modern AI technologies to build practical automation and AI solutions.

🌐 LinkedIn:
https://www.linkedin.com/in/saifuddin-yeahea-b557a1109

🚀 Building AI solutions through my #100DaysOfAI journey

## 📸 Demo

![AI Agent Demo](assets/demo.png)
