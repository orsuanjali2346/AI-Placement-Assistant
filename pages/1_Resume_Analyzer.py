import streamlit as st
import fitz

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(page_title="Resume Analyzer")

st.title("📄 Resume Analyzer")

st.markdown("""
Analyze your resume using AI.

### What this module will do

✅ Extract resume text

✅ Analyze strengths

✅ Find missing skills

✅ Suggest improvements

---
""")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type="pdf"
)

if uploaded_file:

    file_size = len(uploaded_file.getvalue())

    if file_size > 10 * 1024 * 1024:
        file_size_mb = file_size / (1024 * 1024)

        st.error(
            f"❌ File size is {file_size_mb:.2f} MB. Maximum allowed size is 10 MB."
        )
        st.stop()

    st.success("✅ Resume uploaded successfully!")

    st.write("📄 Resume Name:", uploaded_file.name)

    file_size_kb = file_size / 1024
    st.write(f"📦 File Size: {file_size_kb:.2f} KB")

    pdf_document = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    total_pages = len(pdf_document)

    resume_text = ""

    for page in pdf_document:
        resume_text += page.get_text() + "\n"

    total_words = len(resume_text.split())
    total_characters = len(resume_text)

    st.subheader("📊 Resume Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Total Pages", total_pages)

    with col2:
        st.metric("📝 Total Words", total_words)

    with col3:
        st.metric("🔠 Total Characters", total_characters)

    clean_resume_text = []

    for line in resume_text.splitlines():
        if line.strip():
            clean_resume_text.append(line)

    clean_resume_text = "\n".join(clean_resume_text)

    prompt = f"""
    You are an expert resume reviewer.

    Generate a professional summary of the following resume.

    Rules:
    - Summarize in 4-5 sentences.
    - Highlight education, technical skills, projects, and strengths.
    - Keep the tone professional.
    - Do not invent information.

    Resume:
    {clean_resume_text}
    """

    with st.spinner("🤖 Analyzing your resume..."):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    st.subheader("🤖 AI Resume Summary")

    st.write(response.text)

    with st.expander("🧹 Resume Preview"):
        st.text(clean_resume_text)