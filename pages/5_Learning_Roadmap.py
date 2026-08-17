import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(page_title="Learning Roadmap")

st.title("🗺️ Learning Roadmap")

resume_text = st.session_state.get("resume_text")

if not resume_text:
    st.warning(
        "⚠️ Please upload your resume first from the Resume Analyzer page."
    )
    st.stop()

st.write(
    "Generate a personalized learning roadmap based on your current skills and career goals."
)

career_goal = st.selectbox(
    "🎯 Choose Your Career Goal",
    [
        "Software Developer",
        "Python Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI/ML Engineer",
        "Full Stack Developer"
    ]
)

st.subheader("📄 Resume Status")

st.success("✅ Resume loaded successfully.")

st.subheader("🎯 Career Goal")

st.write(f"Selected: **{career_goal}**")

if st.button("🚀 Generate Learning Roadmap"):

    prompt = f"""
You are an expert career mentor.

Create a personalized learning roadmap for the candidate.

Career Goal:
{career_goal}

Candidate Resume:
{resume_text}

Analyze the candidate's existing skills and identify the important skills
they should learn or improve for the selected career goal.

Return the roadmap in EXACTLY this structure:

## Current Skills
- Skill 1
- Skill 2
- Skill 3

## Skill Gaps
- Skill 1
- Skill 2
- Skill 3

## Learning Roadmap

### Phase 1: Fundamentals
- Topic
- Topic

### Phase 2: Intermediate Skills
- Topic
- Topic

### Phase 3: Advanced Skills
- Topic
- Topic

### Phase 4: Projects
- Project idea
- Project idea

### Phase 5: Interview Preparation
- Topic
- Topic

## Recommended Learning Order
1. Topic
2. Topic
3. Topic
4. Topic
5. Topic

Keep the roadmap practical and suitable for a student preparing for placements.
Do not recommend skills that are completely unrelated to the selected career goal.
"""

    try:

        with st.spinner("🤖 Creating your personalized roadmap..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        roadmap = response.text.strip()

        st.session_state["learning_roadmap"] = roadmap

    except Exception as e:

        st.error("❌ Unable to generate learning roadmap.")
        st.error(f"Error: {e}")
        st.stop()

if "learning_roadmap" in st.session_state:

    st.subheader("🗺️ Your Personalized Learning Roadmap")

    st.markdown(
        st.session_state["learning_roadmap"]
    )

    st.download_button(
        "📥 Download Roadmap",
        st.session_state["learning_roadmap"],
        file_name="learning_roadmap.txt",
        mime="text/plain"
    )