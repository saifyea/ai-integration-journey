import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
try:
    api_key=st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key=os.getenv("ANTHROPIC_API_KEY")

client=Anthropic(api_key=api_key)

st.set_page_config(
    page_title="Proposal Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Freelance Proposal Generator")
st.caption("Winningg Proposals-AI দিয়ে")

#sidebar
with st.sidebar:
    st.header("👤 তোমার Profile")
    your_name=st.text_input("নাম:", value="Saifuddin")
    experience=st.text_input(
        "Experience:",
        value="17+ years IT Manager, AI Integration Specialist"
    )
    skills=st.text_area(
        "Skills:",
        value="Python, LangChain, RAG, AI Agents, Claude AI, FastAPI, Streamlit"
    )
    portfolio=st.text_input(
        "Portfolio URL:",
        value="https://saifyea.streamlit.app"
    )
    github=st.text_input(
        "GitHub:",
        value="github.com/saifyea"
    )

st.divider()

#main job details
st.header("📋 Job Details")
col1,col2=st.columns(2)
with col1:
    job_title=st.text_input(
        "Job Title:",
        placeholder="AI Chatbot Developer needed..."
    )
    job_description=st.text_area(
        "Job Description paste করো:",
        height=200,
        placeholder="Client এর job post এখানে paste করো..."
    )
with col2:
    budget = st.text_input(
        "Budget:",
        placeholder="$100-500"
    )
    proposal_type = st.selectbox(
        "Proposal Type:",
        [
            "AI Chatbot Development",
            "RAG System",
            "AI Agent",
            "FastAPI + AI",
            "Streamlit Dashboard",
            "General AI Integration"
        ]
    )
    tone = st.selectbox(
        "Tone:",
        ["Professional", "Friendly", "Concise"]
    )
st.divider()

if st.button("🚀 Proposal Generate করো!", type="primary"):
    if not job_description:
        st.warning("Job description দাও")
    else:
        with st.spinner("AI proposal লিখছে..."):
            response=client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=800,
                system=f"""তুমি একজন expert freelance proposal writer।
                Upwork এর জন্য winning proposals লেখো।
                
                Freelancer profile:
                Name:{your_name}
                Experience:{experience}
                Skills: {skills}
                Portfolio:{portfolio}
                GitHub:{github}

                Proposal Rules:
                - Client এর problem সরাসরি address করো
                - নিজের relevant experience mention করো
                - Portfolio link দাও
                - Clear call to action দাও
                - ৩-৪ paragraph এ রাখো
                - Tone: {tone}""",
                messages=[{
                    "role":"user",
                    "content":f"""এই job এর জন্য winning proposal লেখো:

                    Job Title:{job_description}
                    Budget:{budget}
                    Type:{proposal_type}

                    Proposal লেখো যেটা:
                    1. Client এর problem বোঝে
                    2. আমার experience relevant করে দেখায়
                    3. Portfolio mention করে
                    4. Next step clear করে"""  
                }]
            )

            proposal=response.content[0].text
            st.success("✅ Proposal তৈরি!")
            st.markdown("### 📄 Generated Proposal:")
            st.markdown(proposal)
             # Copy & Download
            col1,col2=st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download করো",
                    data=proposal,
                    file_name=f"proposal_{job_title[:20]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
st.divider()

# ✅ Fiverr Gig Generator
st.header("🎯 Fiverr Gig Generator")
gig_service=st.selectbox(
    "কোন service এর Gig?",
    [
        "AI Chatbot Development",
        "RAG Knowledge Base",
        "AI Agent Building",
        "Streamlit Dashboard",
        "Telegram AI Bot"
    ]
)
gig_price=st.number_input("Basic Package Price($):",value=50)

if st.button("🎯 Gig Description Generate করো!"):
    with st.spinner("Gig বানাচ্ছি..."):
        response=client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system="""তুমি Fiverr gig writing expert।
            Fiverr এ rank করার জন্য optimized gig লেখো।""",
            messages=[{
                "role": "user",
                "content": f"""এই service এর জন্য Fiverr gig লেখো:

                Service: {gig_service}
                Basic Price: ${gig_price}
                Seller: {your_name} — {experience}

                লেখো:
                1. Gig Title (SEO optimized)
                2. Gig Description (200 words)
                3. Basic Package details
                4. Standard Package details
                5. Premium Package details
                6. FAQ (3টা)
                7. Tags (5টা)"""
            }]
        )

        st.success("✅ Gig তৈরি!")
        st.markdown(response.content[0].text)

        st.download_button(
            "📥 Gig Download করো",
            data=response.content[0].text,
            file_name=f"fiverr_gig_{gig_service}.txt",
            mime="text/plain"
        )
