import streamlit as st
import sqlite3
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

st.set_page_config(
    page_title="AI SQL Dashboard",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ AI SQL Dashboard")
st.caption("Natural Language দিয়ে Database Query করো!")

# Connect to DB
conn = sqlite3.connect("kids_store.db")

# Sidebar — Quick Stats
with st.sidebar:
    st.header("📊 Quick Stats")

    df_products = pd.read_sql("SELECT * FROM products", conn)
    df_orders = pd.read_sql("SELECT * FROM orders", conn)

    st.metric("Total Products", len(df_products))
    st.metric("Total Orders", len(df_orders))
    st.metric(
        "Total Revenue",
        f"৳{df_orders['total_price'].sum():,}"
    )
    st.metric(
        "Pending Orders",
        len(df_orders[df_orders['status'] == 'pending'])
    )

# Main — NL Query
st.header("💬 Natural Language Query")

question = st.text_input(
    "বাংলায় প্রশ্ন করো:",
    placeholder="সবচেয়ে বেশি বিক্রি হওয়া product কোনটা?"
)
# SQL extract function যোগ করো
def extract_sql(text):
    # Semicolon পর্যন্ত নাও
    if ";" in text:
        sql = text.split(";")[0] + ";"
    else:
        sql = text

    # Code block সরাও
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # শুধু SQL lines নাও
    lines = []
    for line in sql.split("\n"):
        line = line.strip()
        # বাংলা text skip করো
        if line and not any(
            "\u0980" <= c <= "\u09ff"
            for c in line
        ):
            lines.append(line)

    return " ".join(lines).strip()

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Query করো!", type="primary"):
        if question:
            schema = """
Tables:
- products(id, name, price, stock, category, age_min, age_max)
- orders(id, product_id, customer_name, quantity, total_price, status, order_date, location)
- customers(id, name, phone, location, total_orders, total_spent)
"""
            with st.spinner("SQL বানাচ্ছি..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=200,
                    system=f"SQL expert। Schema:\n{schema}\nShould return only SELECT SQL.",
                    messages=[{
                        "role": "user",
                        "content": f"Question: {question}\nSQL:"
                    }]
                )
                #sql = response.content[0].text.strip()
                #sql = sql.replace("```sql", "").replace("```", "").strip()
                #st.code(sql, language="sql")

                raw = response.content[0].text.strip()
                sql = extract_sql(raw)
                st.code(sql, language="sql")

            try:
                df = pd.read_sql(sql, conn)
                st.dataframe(df, use_container_width=True)

                # AI Insight
                insight = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=150,
                    messages=[{
                        "role": "user",
                        "content": f"Data: {df.to_dict()}\nবাংলায় ২ লাইন business insight দাও:"
                    }]
                )
                st.info(f"🤖 {insight.content[0].text}")

            except Exception as e:
                st.error(f"❌ Error: {e}")

with col2:
    st.markdown("**Quick Questions:**")
    quick_qs = [
        "সবচেয়ে বেশি বিক্রি হওয়া product?",
        "মোট revenue কত?",
        "pending orders কতটা?",
        "ঢাকার customers কতজন?"
    ]
    for q in quick_qs:
        if st.button(q, key=q):
            st.session_state.quick_q = q

# Tables
st.divider()
st.header("📋 Database Tables")

tab1, tab2, tab3 = st.tabs(["Products", "Orders", "Customers"])

with tab1:
    st.dataframe(df_products, use_container_width=True)
with tab2:
    df_orders = pd.read_sql("SELECT * FROM orders", conn)
    st.dataframe(df_orders, use_container_width=True)
with tab3:
    df_customers = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df_customers, use_container_width=True)