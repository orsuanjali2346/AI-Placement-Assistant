import streamlit as st

st.set_page_config(page_title="Job Matcher")

st.title("💼 Job Matcher")

resume_text = st.session_state.get("resume_text")

if not resume_text:
    st.warning(
        "⚠️ Please upload your resume first from the Resume Analyzer page."
    )
    st.stop()

st.write(
    "Paste a job description below to see how well your resume matches the role."
)

job_description = st.text_area(
    "📋 Job Description",
    height=300,
    placeholder="Paste the job description here..."
)

if st.button("🔍 Analyze Job Match"):

    if (
        not job_description
        or not job_description.strip()
        or job_description.strip().lower() == "none"
    ):
        st.warning("⚠️ Please paste a job description first.")
        st.stop()

    st.session_state["job_description"] = job_description

    st.success("✅ Job description saved successfully!")

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

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

    matching_skills = []

    for skill in required_skills:
        if skill in resume_lower and skill in job_lower:
            matching_skills.append(skill)

    missing_job_skills = []

    for skill in required_skills:
        if skill in job_lower and skill not in resume_lower:
            missing_job_skills.append(skill)

    if matching_skills or missing_job_skills:

        total_job_skills = (
            len(matching_skills)
            + len(missing_job_skills)
        )

        job_match_score = (
            len(matching_skills)
            / total_job_skills
        ) * 100

    else:
        job_match_score = None

    if job_match_score is not None:

        st.subheader("🎯 Job Match Result")
        st.session_state["job_match_score"] = job_match_score
        st.metric(
            "Job Match Score",
            f"{job_match_score:.1f}%"
        )

        if job_match_score is not None:

            st.session_state["job_match_score"] = job_match_score

            st.metric(
                "Job Match Score",
                f"{job_match_score:.1f}%"
            )
        
        if job_match_score >= 80:

            st.success(
                "🟢 Strong Match — "
                "Your resume is highly aligned with this job."
            )

        elif job_match_score >= 60:

            st.warning(
                "🟡 Good Match — "
                "Your resume matches many of the job requirements."
            )

        elif job_match_score >= 40:

            st.warning(
                "🟠 Moderate Match — "
                "Consider improving your resume with the missing job skills."
            )

        else:

            st.error(
                "🔴 Low Match — "
                "Your resume needs significant improvement for this role."
            )

    else:

        st.info(
            "ℹ️ No predefined skills were detected in this job description."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🤝 Matching Skills")

        if matching_skills:

            st.write(
                " • ".join(
                    skill.title()
                    for skill in matching_skills
                )
            )

        else:

            st.write("No matching skills found.")

    with col2:

        st.subheader("🛠 Missing Job Skills")

        if missing_job_skills:

            st.write(
                " • ".join(
                    skill.title()
                    for skill in missing_job_skills
                )
            )

        else:

            st.write("🎉 No missing job skills!")

    st.subheader("💡 How to Improve Your Match")

    if missing_job_skills:

        for skill in missing_job_skills:

            st.write(
                f"• **{skill.title()}** — "
                f"Highlight relevant projects, coursework, "
                f"certifications, or genuine experience related "
                f"to {skill.title()} if you have it."
            )

    elif matching_skills:

        st.success(
            "🎉 Your resume covers all the required skills "
            "detected in this job description!"
        )

    else:

        st.info(
            "ℹ️ No predefined skills were detected in this "
            "job description."
        )

    if job_match_score is not None:

        st.subheader("📌 Application Recommendation")

        if job_match_score >= 80:

            st.success(
                "🟢 Highly Recommended — "
                "Your resume has a strong match with this job."
            )

        elif job_match_score >= 60:

            st.success(
                "🟡 Recommended — "
                "You have a good skill match. Consider applying."
            )

        elif job_match_score >= 40:

            st.warning(
                "🟠 Apply After Improving — "
                "Consider addressing the missing skills before applying."
            )

        else:

            st.error(
                "🔴 Low Match — "
                "Consider improving your skills and resume before applying."
            )