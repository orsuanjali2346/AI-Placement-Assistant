import streamlit as st

st.set_page_config(
    page_title="AI Placement Assistant",
    page_icon="🎯",
    layout="wide"
)


st.title("🎯 AI Placement Assistant")

st.subheader(
    "Your Personal AI-Powered Placement Companion"
)

st.write(
    "Prepare smarter for placements with AI-powered resume analysis, "
    "ATS scoring, job matching, mock interviews, and personalized learning."
)

st.write("")

if st.button("🚀 Get Started"):

    st.session_state["started"] = True

    st.success(
        "🎉 Welcome! Start by uploading your resume from the Resume Analyzer."
    )

st.divider()

st.subheader("✨ What You Can Do")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 📄 Resume Analysis")

    st.write(
        "Upload your resume and get AI-powered insights."
    )

with col2:

    st.markdown("### 📊 ATS Score")

    st.write(
        "Check how well your resume performs against ATS requirements."
    )

with col3:

    st.markdown("### 💼 Job Matching")

    st.write(
        "Compare your resume with job descriptions and identify skill gaps."
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.markdown("### 🎤 Mock Interview")

    st.write(
        "Practice interview questions and receive AI-powered feedback."
    )

with col5:

    st.markdown("### 🗺️ Learning Roadmap")

    st.write(
        "Get a personalized learning roadmap based on your career goal."
    )

with col6:

    st.markdown("### 📈 Progress Tracker")

    st.write(
        "Track your learning progress and completed topics."
    )

st.divider()

st.subheader("🚀 Your Placement Journey")

st.write(
    "📄 Resume → 📊 ATS → 💼 Job Match → "
    "🎤 Mock Interview → 🗺️ Learning Roadmap → 📈 Progress"
)