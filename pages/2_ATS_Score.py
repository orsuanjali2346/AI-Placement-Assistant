import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(page_title="ATS Score")

st.title("📊 ATS Score")

resume_text = st.session_state.get("resume_text")

if resume_text is None:
    st.warning("⚠ Please upload a resume first from the Resume Analyzer page.")
    st.stop()

ats_prompt = f"""
You are an Applicant Tracking System (ATS).

Evaluate the following resume.

Return the response in EXACTLY this format:

ATS_SCORE: <score out of 100>

REASON:
- Point 1
- Point 2
- Point 3

SUGGESTIONS:
- Suggestion 1
- Suggestion 2
- Suggestion 3

Do not write anything outside this format.

Resume:
{resume_text}
"""

try:
    with st.spinner("📊 Calculating ATS Score..."):

        ats_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=ats_prompt
        )

except Exception as e:
    st.error("❌ Unable to generate ATS evaluation.")
    st.error(f"Error: {e}")
    st.stop()

lines = ats_response.text.split("\n")

score = ""

for line in lines:
    if line.startswith("ATS_SCORE:"):
        score = line.replace("ATS_SCORE: ", "").strip()
        score=score.replace("/100","").strip()
        break

formatted_response = "\n".join(lines[1:]).strip()



st.subheader("📋 ATS Evaluation")
st.markdown(formatted_response)

required_skills = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "react",
    "aws",
    "git",
    "django",
    "html",
    "css",
    "javascript"
]

ats_keywords = [
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "rest api",
    "docker",
    "github"
]


resume_lower = resume_text.lower()

found_keywords = []

for keyword in ats_keywords:
    if keyword in resume_lower:
        found_keywords.append(keyword)
keyword_match = (len(found_keywords) / len(ats_keywords)) * 100

found_skills = []

for skill in required_skills:
    if skill in resume_lower:
        found_skills.append(skill)

missing_skills = []

for skill in required_skills:
    if skill not in found_skills:
        missing_skills.append(skill)

skill_match = (len(found_skills) / len(required_skills)) * 100
st.session_state["skill_match"] = skill_match


col1, col2, col3 = st.columns(3)

with col1:
    st.session_state["ats_score"] = score
    st.metric("📊 ATS Score", score + "/100")

with col2:
    st.metric("🎯 Skill Match", f"{skill_match:.1f}%")

with col3:
    st.metric("🔑 Keyword Match", f"{keyword_match:.1f}%")



st.subheader("💻 Skills Found")
if found_skills:
    st.write(" • ".join(skill.title() for skill in found_skills))
else:
    st.write("No required skills found.")



st.subheader("🛠 Missing Skills")
if missing_skills:
    st.write(" • ".join(skill.title() for skill in missing_skills))
else:
    st.write("🎉 No missing skills!")