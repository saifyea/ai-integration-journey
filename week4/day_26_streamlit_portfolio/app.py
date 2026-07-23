import streamlit as st

# Page Config
st.set_page_config(
    page_title="Saifuddin — AI Portfolio",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.hero-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.project-card {
    background: #1e1e2e;
    border: 1px solid #6366f1;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.skill-badge {
    background: #6366f1;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ✅ Hero Section
st.markdown('<p class="hero-title">Saifuddin Yeahea</p>',
            unsafe_allow_html=True)
st.markdown("### 🤖 IT Manager → AI Integration Specialist")
st.markdown("**17+ years RMG Sector** | **Python • LangChain • RAG • AI Agents**")
st.markdown("I help businesses build AI-powered chatbots, RAG systems, automation tools and deploy them as production-ready applications.")
st.markdown("")
col1, col2, col3 = st.columns(3)
with col1:
    st.link_button(
        "🔗 GitHub",
        "https://github.com/saifyea/ai-integration-journey"
    )
with col2:
    st.link_button(
        "💼 LinkedIn",
        "www.linkedin.com/in/saifuddin-yeahea-b557a1109"
    )
with col3:
    st.link_button(
        "🤖 Live Demo",
        "https://ai-store-dashboard.streamlit.app/"
    )

st.divider()
# about
st.subheader("👋 About Me")
st.markdown("I'***m an IT Manager with 17+ years of experience in the RMG industry, currently transitioning into AI Integration.***")
st.markdown("I'***m building AI applications using Python, LangChain, Claude AI, RAG, FastAPI, and Streamlit while documenting my learning journey publicly.***")
st.markdown("My goal is to help businesses automate workflows using practical AI solutions.")

st.divider()
# ✅ Stats
st.markdown("## 📊 Journey Stats")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Days Learning", "26+")
s2.metric("Projects Built", "15+")
s3.metric("AI Tools", "5+")
s4.metric("Lines of Code", "2000+")

st.divider()

# ✅ Projects
st.markdown("## 🛠️ Projects")

projects = [
    {
        "name": "🤖 Complete AI Suite",
        "desc": "An all-in-one AI business dashboard featuring Product Content Generation, Customer Support Chatbot, RAG Knowledge Base and AI Agent in one application.",
        "tech": ["Python", "Claude AI", "LangChain", "Streamlit"],
        "live": "https://ai-store-dashboard.streamlit.app/",
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "🟢 Live"
    },
    {
        "name": "🔍 RAG Knowledge Base",
        "desc": "Built a Retrieval-Augmented Generation (RAG) system using FAISS vector database and HuggingFace embeddings for document-based intelligent question answering.",
        "tech": ["LangChain", "FAISS", "HuggingFace", "Claude AI"],
        "live": None,
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "✅ Complete"
    },
    {
        "name": "🤖 AI Agent with Memory",
        "desc": "Developed an autonomous AI Agent with conversation memory capable of selecting tools automatically for pricing, delivery information and knowledge retrieval.",
        "tech": ["LangChain", "AI Agent", "Tools", "Memory"],
        "live": None,
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "✅ Complete"
    },
    {
        "name": "📱 Telegram Bot",
        "desc": "AI-powered Telegram assistant that provides product information, pricing, delivery support and customer service through natural language conversations.",
        "tech": ["python-telegram-bot", "Claude AI", "Commands"],
        "live": None,
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "✅ Complete"
    },
    {
        "name": "⚡ FastAPI + AI",
        "desc": "Developed REST API endpoints for AI-powered applications including chat, product generation and pricing services using FastAPI.",
        "tech": ["FastAPI", "Pydantic", "Claude AI", "REST API"],
        "live": None,
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "✅ Complete"
    },
    {
        "name": "📝 Product Content Generator",
        "desc": "AI tool for generating product descriptions, Facebook captions and marketing content for e-commerce businesses.",
        "tech": ["Python", "Claude AI", "Prompt Engineering"],
        "live": None,
        "github": "https://github.com/saifyea/ai-integration-journey",
        "status": "✅ Complete"
    }
]


# Project Cards
for i in range(0, len(projects), 2):
    col1, col2 = st.columns(2)

    for j, col in enumerate([col1, col2]):
        if i + j < len(projects):
            p = projects[i + j]
            with col:
                with st.container(border=True):
                    st.markdown(f"### {p['name']}")
                    st.markdown(f"**{p['status']}**")
                    st.markdown(p['desc'])

                    # Tech badges
                    badges = " ".join([
                        f"`{t}`" for t in p['tech']
                    ])
                    st.markdown(badges)

                    # Buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        st.link_button(
                            "GitHub",
                            p['github'],
                            use_container_width=True
                        )
                    with btn_col2:
                        if p['live']:
                            st.link_button(
                                "🔗 Live Demo",
                                p['live'],
                                use_container_width=True
                            )
                        else:
                            st.button(
                                "🚧 Coming Soon",
                                disabled=True,
                                use_container_width=True,
                                key=f"coming_soon_{p['name']}"
                            )

st.divider()


# ✅ Tech Skills
st.markdown("## 🛠 Technology Stack")

skill_col1, skill_col2, skill_col3 = st.columns(3)

with skill_col1:
    st.markdown("**🤖 AI & LLM**")
    st.markdown(":green-badge[Claude AI] :green-badge[LangChain] :green-badge[RAG]" )
    st.markdown(":green-badge[AI Agents] :green-badge[Prompt Engineering] :green-badge[HuggingFace]")

with skill_col2:
    st.markdown("**🐍 Development**")
    st.markdown(":green-badge[Python] :green-badge[FastAPI] :green-badge[Streamlit]" )
    st.markdown(":green-badge[REST API] :green-badge[BeautifulSoup] :green-badge[Telegram Bot]")

with skill_col3:
    st.markdown("**🗄 Data & Infrastructure**")
    st.markdown(":green-badge[QL Server] :green-badge[FAISS] :green-badge[Git]:green-badge[GitHub]" )
    st.markdown(" :green-badge[ERP Systems] :green-badge[Network Design]:green-badge[Active Directory]")
    #st.markdown(":green-badge[Active Directory] ")


st.divider()
# ✅ Contact
st.markdown("## 📬 Let's Build Something Together")

st.write(
    """
Have an AI automation idea, chatbot requirement,
or RAG system project?

I'm open to:
- 🤖 AI Integration Projects
- 💬 Chatbot Development
- 🔍 RAG Applications
- ⚡ Business Automation
- 🏭 RMG Sector AI Solutions
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "💻 GitHub",
        "https://github.com/saifyea",
        use_container_width=True
    )

with col2:
    st.link_button(
        "💼 LinkedIn",
        "www.linkedin.com/in/saifuddin-yeahea-b557a1109",
        use_container_width=True
    )

with col3:
    st.link_button(
        "📧 Email",
        "mailto:saifyea@gmail.com",
        use_container_width=True
    )

st.divider()

# Contact Form
with st.form("contact_form"):
    name = st.text_input("নাম:")
    email = st.text_input("Email:")
    message = st.text_area("Message:")

    if st.form_submit_button("📨 Send করো!", type="primary"):
        if name and email and message:
            st.success(f"✅ ধন্যবাদ {name}! শীঘ্রই যোগাযোগ করব।")
        else:
            st.warning("সব field পূরণ করো!")



st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**© 2026 Saifuddin Yeahea**")  

with col2:
    st.markdown("**Built with Python • Streamlit • Claude AI**")
    
with col3:
    st.markdown("**Always Learning • Always Building 🚀**")
   




