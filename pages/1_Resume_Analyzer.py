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

    st.session_state["resume_text"] = clean_resume_text
    

    summary_prompt = f"""
You are an expert resume reviewer.

Analyze the following resume and respond using exactly this format:

### Professional Summary
(4-5 sentences)

### Education
(List the education)

### Technical Skills
(List the technical skills)

### Projects
(List the important projects)

### Strengths
(List 3-5 strengths based only on the resume.)

Do not invent any information that is not present in the resume.

Resume:
{clean_resume_text}
"""

    analysis_prompt = f"""
You are an expert resume reviewer.

Analyze the following resume.

Return the response in Markdown format.

## ⭐ Strengths
- List 3-5 strengths based only on the resume.

## ⚠️ Weaknesses
- List 3-5 weaknesses based only on the resume.

## 🛠 Missing Skills
- List important missing skills based only on the resume.

## 💡 Suggestions
- Suggest practical improvements to make the resume stronger for placements.

Do not invent any information that is not present in the resume.

Resume:
{clean_resume_text}
"""

    try:
        with st.spinner("🤖 Generating AI Resume Summary..."):

            summary_response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=summary_prompt
            )

        st.subheader("🤖 AI Resume Summary")
        st.markdown(summary_response.text)

    
    except Exception:
        st.error("❌ Gemini is currently busy. Please try again in a few moments.")


    try:
        with st.spinner("🔍 Analyzing Resume..."):

            analysis_response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=analysis_prompt
        )

        st.subheader("📋 AI Resume Analysis")
        st.markdown(analysis_response.text)

    except Exception as e:
        st.error("❌ Unable to analyze the resume.")
        st.error(f"Error: {e}")


    















    with st.expander("🧹 Resume Preview"):
        st.text(clean_resume_text)


   