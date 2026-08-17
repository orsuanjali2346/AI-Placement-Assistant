import streamlit as st

st.set_page_config(
    page_title="Placement Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.metric-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1f2937;
    border: 1px solid #374151;
    text-align: center;
    margin-bottom: 15px;
}

.metric-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Placement Dashboard")

st.write(
    "Track your resume strength, job readiness, interview performance, "
    "and learning progress in one place."
)

resume_text = st.session_state.get("resume_text")

if resume_text:
    resume_status = "✅ Resume Uploaded"
else:
    resume_status = "❌ Resume Not Uploaded"

st.subheader("👤 Resume Status")

if resume_text:
    st.success(resume_status)
else:
    st.warning(resume_status)

ats_score = st.session_state.get("ats_score")
skill_match = st.session_state.get("skill_match")
job_match_score = st.session_state.get("job_match_score")
interview_score = st.session_state.get("interview_score")

col1, col2, col3, col4 = st.columns(4)

with col1:

    ats_value = (
        f"{ats_score}/100"
        if ats_score is not None
        else "—"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">📊 ATS Score</div>
            <div class="metric-value">{ats_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    skill_value = (
        f"{skill_match:.1f}%"
        if skill_match is not None
        else "—"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">🎯 Skill Match</div>
            <div class="metric-value">{skill_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    job_value = (
        f"{job_match_score:.1f}%"
        if job_match_score is not None
        else "—"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">💼 Job Match</div>
            <div class="metric-value">{job_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    interview_value = (
        f"{interview_score:.1f}/10"
        if interview_score is not None
        else "—"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">🎤 Interview</div>
            <div class="metric-value">{interview_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

st.subheader("🚀 Placement Readiness")

scores = []

if ats_score is not None:
    scores.append(float(ats_score))

if skill_match is not None:
    scores.append(float(skill_match))

if job_match_score is not None:
    scores.append(float(job_match_score))

if interview_score is not None:
    scores.append(float(interview_score) * 10)

if scores:

    readiness_score = sum(scores) / len(scores)

    st.progress(
        readiness_score / 100
    )

    st.metric(
        "Overall Placement Readiness",
        f"{readiness_score:.1f}%"
    )

    if readiness_score >= 80:

        st.success(
            "🟢 Excellent readiness! You are strongly prepared for placements."
        )

    elif readiness_score >= 60:

        st.warning(
            "🟡 Good readiness! A little more preparation can improve your chances."
        )

    elif readiness_score >= 40:

        st.warning(
            "🟠 Moderate readiness. Focus on improving your weaker areas."
        )

    else:

        st.error(
            "🔴 Keep preparing. Strengthen your resume, skills, and interview performance."
        )

else:

    st.info(
        "📌 Complete the Resume, ATS, Job Match, or Mock Interview modules "
        "to calculate your placement readiness."
    )

completed_topics = st.session_state.get(
    "completed_topics",
    []
)

total_topics = 9

progress = len(completed_topics) / total_topics

st.divider()

st.subheader("🎯 Recommended Next Step")

if not resume_text:

    st.info(
        "📄 Upload your resume first to begin your placement preparation."
    )

elif ats_score is None:

    st.info(
        "📊 Analyze your resume with the ATS Score module."
    )

elif skill_match is None:

    st.info(
        "🎯 Check your skill match and identify your missing skills."
    )

elif job_match_score is None:

    st.info(
        "💼 Analyze a job description to check your job compatibility."
    )

elif interview_score is None:

    st.info(
        "🎤 Complete a mock interview to evaluate your interview skills."
    )

elif progress < 0.7:

    st.info(
        "🗺️ Continue your Learning Roadmap and improve your learning progress."
    )

else:

    st.success(
        "🏆 Excellent! You have completed the major placement preparation steps."
    )

st.divider()

st.subheader("🗺️ Learning Progress")

st.progress(progress)

st.write(
    f"📊 {len(completed_topics)} / {total_topics} topics completed"
)

if progress == 1:

    st.success(
        "🎉 Congratulations! You completed all learning topics!"
    )

elif progress >= 0.7:

    st.success(
        "🔥 Excellent progress! Keep going!"
    )

elif progress >= 0.4:

    st.info(
        "💪 Good progress! Keep learning!"
    )

else:

    st.warning(
        "🚀 Keep working! You are just getting started!"
    )

st.divider()

st.subheader("🚀 Placement Journey")

st.write(
    "📄 Resume → 📊 ATS → 💼 Job Match → "
    "🎤 Mock Interview → 🗺️ Learning Roadmap → 📈 Progress"
)

st.divider()

st.subheader("📌 Module Status")

col1, col2, col3 = st.columns(3)

with col1:

    if resume_text:

        st.success(
            "📄 Resume Analyzer\n\nCompleted"
        )

    else:

        st.warning(
            "📄 Resume Analyzer\n\nNot completed"
        )

with col2:

    if ats_score is not None:

        st.success(
            "📊 ATS Analysis\n\nCompleted"
        )

    else:

        st.warning(
            "📊 ATS Analysis\n\nNot completed"
        )

with col3:

    if job_match_score is not None:

        st.success(
            "💼 Job Matcher\n\nCompleted"
        )

    else:

        st.warning(
            "💼 Job Matcher\n\nNot completed"
        )

col4, col5, col6 = st.columns(3)

with col4:

    if interview_score is not None:

        st.success(
            "🎤 Mock Interview\n\nCompleted"
        )

    else:

        st.warning(
            "🎤 Mock Interview\n\nNot completed"
        )

with col5:

    if "learning_roadmap" in st.session_state:

        st.success(
            "🗺️ Learning Roadmap\n\nCompleted"
        )

    else:

        st.warning(
            "🗺️ Learning Roadmap\n\nNot completed"
        )

with col6:

    if completed_topics:

        st.success(
            "📈 Progress Tracker\n\nIn Progress"
        )

    else:

        st.warning(
            "📈 Progress Tracker\n\nNot started"
        )