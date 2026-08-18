import streamlit as st
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()


claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
#gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))          it will also work but we are using base_url for free token faucet
#deepseek = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"))   it will also work but we are using base_url for free token faucet
gpt = OpenAI(
  base_url="https://freetokenfaucet.com/v1",
  api_key=os.getenv("OPENAI_API_KEY"),
)
DeepSeek = OpenAI(
  base_url="https://freetokenfaucet.com/v1",
  api_key=os.getenv("DEEPSEEK_API_KEY"),
)




st.set_page_config(
    page_title="AI Model Comparison",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Claude vs GPT-4o-mini")
st.caption("Real-time AI Model Comparison")

question = st.text_area(
    "প্রশ্ন লেখো:",
    placeholder="যেকোনো প্রশ্ন করো..."
)

col1, col2, col3 = st.columns(3)

with col1:
    claude_model = st.selectbox(
        "Claude Model:",
        ["claude-haiku-4-5-20251001",
         "claude-sonnet-4-6"]
    )

with col2:
    gpt_model = st.selectbox(
        "GPT Model:",
        ["gpt-5.6-terra", "gpt-5.6-luna"]
    )
with col3:
    deepseek_model = st.selectbox(
        "DeepSeek Model:",
        ["deepseek-v4-flash"]
    )

if st.button("🚀 Compare করো!", type="primary"):
    if not question:
        st.warning("প্রশ্ন লেখো!")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🤖 Claude")
            with st.spinner("Claude ভাবছে..."):
                start = time.time()
                r = claude.messages.create(
                    model=claude_model,
                    max_tokens=300,
                    messages=[{
                        "role": "user",
                        "content": question
                    }]
                )
                elapsed = time.time() - start
                st.success(f"⚡ {elapsed:.2f}s")
                st.markdown(r.content[0].text)

        with col2:
            st.markdown("### 🟢 GPT")
            with st.spinner("GPT ভাবছে..."):
                start = time.time()
                r = gpt.chat.completions.create(
                    model=gpt_model,
                    messages=[{
                        "role": "user",
                        "content": question
                    }]
                )
                elapsed = time.time() - start
                st.success(f"⚡ {elapsed:.2f}s")
                st.markdown(r.choices[0].message.content)
        with col3:
            st.markdown("### 🔵 DeepSeek")
            with st.spinner("DeepSeek ভাবছে..."):
                start = time.time()
                r = DeepSeek.chat.completions.create(
                    model=deepseek_model,
                    messages=[{
                        "role": "user",
                        "content": question
                    }]
                )
                elapsed = time.time() - start
                st.success(f"⚡ {elapsed:.2f}s")
                st.markdown(r.choices[0].message.content)