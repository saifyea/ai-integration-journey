import os
import streamlit as st
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from anthropic import Anthropic

#=====setup========#
load_dotenv()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)


st.set_page_config(
    page_title="RMG AI Tool",
    page_icon="🏭",
    layout="centered"
)

st.title("🏭 RMG Sector AI Assistant")
st.caption("Powered by Claude AI — IT & Payroll Management")

with st.sidebar:
    st.header("📋 Menu")
    page=st.selectbox(
         "Tool বেছে নাও:",
        [
            "💰 Payroll Calculator",
            "📄 HR Document Generator",
            "📊 Attendance Analyzer",
            "📧 Email Generator"
        ]
    )
    st.divider()


if page=="💰 Payroll Calculator":
    st.markdown("💰 Payroll Calculator")
    st.caption("Salary Formula:")
    col1, col2 = st.columns(2)
    with col1:
        employee_name = st.text_input("Employee Name:")
        designation = st.text_input("Designation:",value="Sewing Operator")
        gross_salary = st.number_input("Gross Salary (৳):",value=14273)
        attendance_days = st.number_input("Attendance Days:",value=26,max_value=31)
        overtime_hours = st.number_input("Overtime Hours:",value=20)
    with col2:
        absent_days = st.number_input("Absent Days:",value=0)
        tax = st.number_input("Tax Amount:",value=0)
        advance = st.number_input("Advacne Amount:",value=0)
        arrear = st.number_input("Arrear Amunt:",value=0)
        deductions = st.number_input("Deductions (৳):",value=0)
    if st.button("💰 Calculate করো!", type="primary"):
        # Basic calculations
        medical=750
        transport=450
        food=1250
        basic_salary=(gross_salary-(medical+transport+food))/1.5
        net_salary=(gross_salary/30)*(attendance_days+absent_days)
        absent_amount=(basic_salary/30)*absent_days
        overtime_rate=(basic_salary/104)
        overtime_amount=overtime_rate*overtime_hours
        payble=((net_salary+overtime_amount+arrear)-(absent_amount+advance+deductions))
        
        # Show metrics
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Basic Pay", f"৳{basic_salary:,.0f}")
        m2.metric("OT Pay", f"৳{overtime_amount:,.0f}")
        m3.metric("Gross Salary", f"৳{gross_salary:,.0f}")    
        m4.metric("Net Salary", f"৳{payble:,.0f}")

        # AI Analysis
        with st.spinner("AI analyzing..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system="""তুমি Bangladesh RMG sector payroll expert। Labour law ও industry standard জানো। বাংলায় উত্তর দাও। """,
                messages=[
                    {"role":"user","content":f"""
                        এই payroll analyze করো:
                        Employee: {employee_name}
                        Designation: {designation}
                        Basic: ৳{basic_salary}
                        Attendance: {attendance_days}/30 days
                        OT Hours: {overtime_hours}
                        Gross: ৳{gross_salary:,.0f}
                        Net: ৳{payble:,.0f}

                        As per Gedget 2023:
                        Grade-1: Gross: 15035, Basic:8390, House Rent: 4195, Medical Allowance: 750, Transport Allowance: 450, Food Allowance: 1250
                        Grade-2: Gross: 14273, Basic:7882, House Rent: 3941, Medical Allowance: 750, Transport Allowance: 450, Food Allowance: 1250
                        Grade-3: Gross: 13550, Basic:7400, House Rent: 3700, Medical Allowance: 750, Transport Allowance: 450, Food Allowance: 1250
                        Grade-4: Gross: 12500, Basic:600, House Rent: 3350, Medical Allowance: 750, Transport Allowance: 450, Food Allowance: 1250

                        Salary Calculation Formula: (Gross Salary/30)*attendance_day+(overtime_amount+arrear)-(tax+deductions+absent_amount+advance)
                        OT Rate calculaiton formula: (Basic/208)*2
                        বলো:
                        1. Minimum wage comply করছে?
                        2. OT calculation সঠিক?
                        3. কোনো সমস্যা আছে?
                        4. Suggestion কী?
                    """
                     }
                ]
            )
            st.markdown("### 🤖 AI Analysis:")
            st.markdown(response.content[0].text)
            

# ✅ Page 2 — HR Document Generator
elif page == "📄 HR Document Generator":
    st.header("📄 HR Document Generator")

    doc_type = st.selectbox(
        "Document Type:",
        [
            "Appointment Letter",
            "Warning Letter",
            "Experience Certificate",
            "Salary Certificate",
            "Show Cause Notice",
            "Increment Letter"
        ]
    )

    col1, col2 = st.columns(2)
    with col1:
        emp_name = st.text_input("Employee Name:")
        emp_id = st.text_input("Employee ID:")
        emp_designation = st.text_input("Designation:")
        department = st.text_input("Department:")

    with col2:
        company_name = st.text_input(
            "Company:",
            value="Harry Fashion Limited"
        )
        joining_date = st.date_input("Joining Date:")
        salary = st.number_input("Salary (৳):", value=8000)
        reason = st.text_area(
            "Additional Info/Reason:",
            height=100
        )
    if st.button("📄 HR Document Generator", type="primary"):
        with st.spinner("Document বানাচ্ছি..."):
            response=client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=600,
                system="""তুমি Bangladesh RMG sector HR expert।
                Professional HR documents লেখো।
                Bangladesh Labour Law follow করো।""",
                messages=[{
                    "role": "user",
                    "content": f"""এই HR document বানাও:
                    Document Type: {doc_type}
                    Employee: {emp_name}
                    ID: {emp_id}
                    Designation: {emp_designation}
                    Department: {department}
                    Company: {company_name}
                    Joining Date: {joining_date}
                    Salary: ৳{salary:,}
                    Additional Info: {reason}

                    Professional document লেখো।"""
                }]

            )
            doc_content = response.content[0].text
            st.success("✅ Document তৈরি!")
            st.markdown(doc_content)
            st.download_button(
                "📥 Download Document",
                data=doc_content,
                file_name=f"{doc_type}_{emp_name}.txt"
            )
# ✅ Page 3 — Attendance Analyzer
elif page == "📊 Attendance Analyzer":
    st.header("📊 Attendance Report Analyzer")

    st.info("Employee attendance data paste করো — AI analyze করবে!")

    attendance_data = st.text_area(
        "Attendance Data paste করো:",
        height=200,
        placeholder="""Example:
Employee ID | Name | Present | Absent | Late | OT
001 | Rahim | 24 | 2 | 3 | 15
002 | Karim | 26 | 0 | 1 | 20
003 | Salam | 20 | 6 | 5 | 5"""
    )

    month = st.selectbox(
        "Month:",
        ["January", "February", "March", "April",
         "May", "June", "July", "August",
         "September", "October", "November", "December"]
    )

    if st.button("📊 Analyze করো!", type="primary"):
        if not attendance_data:
            st.warning("Data paste করো!")
        else:
            with st.spinner("Analyzing..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=600,
                    system="""তুমি RMG sector HR analyst।
Attendance data analyze করো এবং insights দাও।
বাংলায় উত্তর দাও।""",
                    messages=[{
                        "role": "user",
                        "content": f"""এই attendance data analyze করো:

Month: {month}
Data:
{attendance_data}

বলো:
1. Overall attendance rate কত?
2. কে সবচেয়ে ভালো attendance করেছে?
3. কে সবচেয়ে বেশি absent ছিল?
4. Late comers কারা?
5. OT কে সবচেয়ে বেশি করেছে?
6. HR action কী নেওয়া উচিত?
7. Summary report দাও।"""
                    }]
                )

                st.success("✅ Analysis Complete!")
                st.markdown(response.content[0].text)

# ✅ Page 4 — Email Generator
elif page == "📧 Email Generator":
    st.header("📧 Professional Email Generator")

    email_type = st.selectbox(
        "Email Type:",
        [
            "Vendor Communication",
            "Buyer Update",
            "Internal Memo",
            "Complaint Letter",
            "Meeting Request",
            "Report Submission"
        ]
    )

    col1, col2 = st.columns(2)
    with col1:
        to_name = st.text_input("To:")
        from_name = st.text_input(
            "From:",
            value="Saifuddin, IT Manager"
        )
        subject = st.text_input("Subject:")

    with col2:
        key_points = st.text_area(
            "Key Points (যা বলতে চাও):",
            height=150
        )
        tone_email = st.selectbox(
            "Tone:",
            ["Formal", "Semi-formal", "Urgent"]
        )

    if st.button("📧 Email Generate করো!", type="primary"):
        with st.spinner("Email লিখছি..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system="""তুমি professional email writer।
RMG sector এর context বোঝো।
Professional English এ email লেখো।""",
                messages=[{
                    "role": "user",
                    "content": f"""এই email লেখো:

Type: {email_type}
To: {to_name}
From: {from_name}
Subject: {subject}
Key Points: {key_points}
Tone: {tone_email}

Professional email লেখো।"""
                }]
            )

            st.success("✅ Email তৈরি!")
            st.markdown(response.content[0].text)

            st.download_button(
                "📥 Email Download",
                data=response.content[0].text,
                file_name=f"email_{subject[:20]}.txt"
            )
