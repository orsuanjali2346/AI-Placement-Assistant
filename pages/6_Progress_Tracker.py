import streamlit as st

st.set_page_config(page_title="Progress Tracker")

st.title("📈 Progress Tracker")

st.write(
    "Track your learning progress and mark the topics you have completed."
)

topics = [
    "Python Fundamentals",
    "SQL",
    "Data Structures & Algorithms",
    "Django",
    "REST APIs",
    "Git & GitHub",
    "Machine Learning",
    "Projects",
    "Interview Preparation"
]

if "completed_topics" not in st.session_state:
    st.session_state["completed_topics"] = []

for topic in topics:

    checked = st.checkbox(
        topic,
        value=topic in st.session_state["completed_topics"],
        key=f"progress_{topic}"
    )

    if checked and topic not in st.session_state["completed_topics"]:
        st.session_state["completed_topics"].append(topic)

    elif not checked and topic in st.session_state["completed_topics"]:
        st.session_state["completed_topics"].remove(topic)

completed_topics = st.session_state["completed_topics"]

progress = len(completed_topics) / len(topics)

st.subheader("📊 Your Progress")

st.progress(progress)

st.write(
    f"📊 Progress: {len(completed_topics)} / {len(topics)} topics completed"
)

if progress == 1:
    st.success("🎉 Congratulations! You completed all the topics!")

elif progress >= 0.7:
    st.success("🔥 Excellent progress! Keep going!")

elif progress >= 0.4:
    st.info("💪 Good progress! Keep learning!")

else:
    st.warning("🚀 Keep working! You are just getting started!")