import streamlit as st

st.set_page_config(
    page_title="AI Placement Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 AI Placement Assistant")

st.markdown("""
## Welcome to Your AI-Powered Placement Companion

This platform is designed to help final-year students prepare for placements through AI.

### 🚀 Features

- 📄 Resume Analyzer
- 📊 ATS Score
- 💼 Job Matcher
- 🎤 Mock Interview
- 📚 Learning Roadmap
- 📈 Progress Tracker

---

👈 Select a feature from the sidebar to get started.
""")

st.divider()

st.caption("Version 0.1.0 | Developed by Anjali ❤️")