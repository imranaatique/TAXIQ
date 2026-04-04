import streamlit as st
from tax_agent import validate_data, calculate_tax
from dotenv import load_dotenv
import os
import io
import anthropic
import base64

load_dotenv()

st.set_page_config(
    page_title="TaxIQ",
    page_icon="🧾",
    layout="centered"
)
st.markdown("""
    <style>
    .stButton > button {
        background-color: #2D6A4F;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1B4332;
        color: white;
    }
    .stDownloadButton > button {
        background-color: #40916C;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem, 1rem;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def extract_tax_info(uploaded_file):
    file_bytes = uploaded_file.read()
    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    if uploaded_file.type == "application/pdf":
        content = [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": file_base64
                }
            },
            {
                "type": "text",
                "text": "This is a tax document. Please extract the following if present: full name, SSN, W-2 income, 1099 income, tax withheld. Return the values in exactly this format with no extra text:\nName: [value]\nSSN: [value]\nW2 Income: [value]\nIncome 1099: [value]\nWithholding: [value]\nIf a value is not found, write 0 for numbers and unknown for text."
            }
        ]
    else:
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": uploaded_file.type,
                    "data": file_base64
                }
            },
            {
                "type": "text",
                "text": "This is a tax document. Please extract the following if present: full name, SSN, W-2 income, 1099 income, tax withheld. Return the values in exactly this format with no extra text:\nName: [value]\nSSN: [value]\nW2 Income: [value]\nIncome 1099: [value]\nWithholding: [value]\nIf a value is not found, write 0 for numbers and unknown for text."
            }
        ]

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return message.content[0].text



def generate_pdf(user_data, total_income, taxable_income, tax_amount, refund, amount_owed):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "Tax-IQ - Tax Return Summary")

    c.line(50, 740, 550, 740)

    c.setFont("Helvetica", 12)

    c.drawString(50, 710, f"Name: {user_data['name']}")
    c.drawString(50, 690, f"SSN: {user_data['ssn']}")
    c.drawString(50, 670, f"Filing Status: {user_data['filing status']}")
    c.drawString(50, 650, f"Total Income: ${total_income}")
    c.drawString(50, 630, f"Taxable Income: ${taxable_income}")
    c.drawString(50, 610, f"Deductions: ${user_data['deductions']}")
    c.drawString(50, 590, f"Dependents: {user_data['dependents']}")
    c.drawString(50, 570, f"Tax Withheld: ${user_data['withholding']}")

    c.line(50, 555, 550, 555)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 535, f"Estimated Tax: ${tax_amount:.2f}")
    c.drawString(50, 515, f"Estimated Refund: ${refund:.2f}")
    c.drawString(50, 495, f"Amount Owed: ${amount_owed:.2f}")

    c.save()

    buffer.seek(0)
    return buffer

st.title("TaxIQ 🧾")
st.subheader("Your AI-Powered Tax Return Generator")
st.markdown("---")

with st.sidebar:
    st.title("Tax-IQ")
    st.write("Your personal AI-powered tax return generator helping you file your taxes efficiently & accurately ")
    st.markdown("---")

    st.subheader("How it works")
    st.write("1. Upload W-2 or 1099")
    st.write("2. AI extracts your tax info")
    st.write("3. Review and edit the form")
    st.write("4. Calculate your taxes")
    st.write("5. Download your tax return PDF")

    st.markdown("---")

    st.caption("TaxIQ is for educational purposes only and should not be used as official tax advice.")  

if "name" not in st.session_state:
    st.session_state["name"] = ""
if "ssn" not in st.session_state:
    st.session_state["ssn"] = ""
if "w2 income" not in st.session_state:
    st.session_state["w2 income"] = 0
if "income 1099" not in st.session_state:
    st.session_state["income 1099"] = 0
if "withholding" not in st.session_state:
    st.session_state["withholding"] = 0

uploaded_file = st.file_uploader("Upload your W-2 or 1099", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success("File is uploaded! Our AI Accountants will extract your tax information.")

    if st.button("Extract Tax info with AI"):

        with st.spinner("Reading your document..."):
            result = extract_tax_info(uploaded_file)
            st.write("**Extracted information:**")
            st.write(result)

            for line in result.split("\n"):
                if "Name:" in line:
                    st.session_state["name"] = line.split(":")[-1].strip()
                elif "SSN:" in line:
                    st.session_state["ssn"] = line.split(":")[-1].strip()
                elif "W2 Income:" in line:
                    value = line.split(":")[-1].strip().replace("$", "").replace(",", "")
                    st.session_state["w2 income"] = int(float(value)) if value != "0" else 0
                elif "Income 1099:" in line:
                    value = line.split(":")[-1].strip().replace("$", "").replace(",", "")
                    st.session_state["income 1099"] = int(float(value)) if value != "0" else 0
                elif "Withholding:" in line:
                    value = line.split(":")[-1].strip().replace("$", "").replace(",", "")
                    st.session_state["withholding"] = int(float(value)) if value != "0" else 0
            st.rerun()

st.header("Personal Information")

name = st.text_input("Full Name", value=st.session_state["name"])
ssn = st.text_input("Social Security Number", value=st.session_state["ssn"])

filing_status = st.selectbox("Filing Status", ["single", "married filing jointly", "head of household"])

st.header("Income Information")

w2_income = st.number_input("W-2 Income ($s)", min_value=0, value=st.session_state["w2 income"])
income_1099 = st.number_input("1099 Income ($)", min_value=0, value=st.session_state["income 1099"])
withholding = st.number_input("Tax Witheld ($)", min_value=0, value=st.session_state["withholding"])

st.header("Deductions & Dependents")
dependents = st.number_input("Number of Dependents", min_value=0, step=1)
deductions = st.number_input("Total Deductions ($)", min_value=0)

if st.button("Calculate My Taxes"):

    user_data = {
        "name": name,
        "ssn": ssn,
        "filing status": filing_status,
        "w2 income": w2_income,
        "income 1099": income_1099,
        "dependents": dependents,
        "deductions": deductions,
        "withholding": withholding

    }
    #st.write(user_data)

    if validate_data(user_data):

        total_income, taxable_income, tax_amount, refund, amount_owed = calculate_tax(user_data)

        st.success("Your tax summary is ready!")
        
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Income", f"${total_income:}")
            st.metric("Taxable Income", f"${taxable_income:,}")
            st.metric("Estimated Tax", f"${tax_amount:,.2f}")

        with col2:
            st.metric("Tax Withheld", f"${user_data['withholding']:,}")
            st.metric("Estimated Refund", f"${refund:,.2f}")
            st.metric("Amount Owed", f"${amount_owed:,.2f}")

        pdf = generate_pdf(user_data, total_income, taxable_income, tax_amount, refund, amount_owed)

        st.markdown("---")
        st.write("Your tax return packet is ready to download. Please review the information above before submitting.")
        st.download_button(
            label="Download Your Tax Return PDF!",
            data=pdf,
            file_name="TaxIQ_Return.pdf",
            mime="application/pdf"
        )

    else:
        st.error("Please fill out all required fields.") 