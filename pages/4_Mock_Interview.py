import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="Mock Interview",
    page_icon="🎤"
)

st.title("🎤 Mock Interview")

resume_text = st.session_state.get("resume_text")

if not resume_text:
    st.warning(
        "⚠️ Please upload your resume first from the Resume Analyzer page."
    )
    st.stop()

if "asked_questions" not in st.session_state:
    st.session_state["asked_questions"] = []

if "interview_question" not in st.session_state:
    st.session_state["interview_question"] = None

st.write(
    "Practice interview questions based on your resume and technical skills."
)

interview_type = st.selectbox(
    "Choose Interview Type",
    [
        "Technical",
        "HR",
        "Project Based"
    ]
)

if st.button("🎯 Generate Interview Question"):

    previous_questions = st.session_state["asked_questions"]

    previous_questions_text = "\n".join(
        f"- {question}"
        for question in previous_questions
    )

    prompt = f"""
You are an experienced interviewer conducting a placement interview.

Generate ONE new interview question for the candidate.

Interview Type:
{interview_type}

Candidate Resume:
{resume_text}

Previously Asked Questions:
{previous_questions_text if previous_questions_text else "None"}

Rules:
- Generate exactly ONE question.
- The question must be relevant to the selected interview type.
- The question must be different from every previously asked question.
- Do not repeat or rephrase a previous question.
- For Technical interviews, ask about technical skills mentioned in the resume.
- For HR interviews, ask about background, goals, strengths, weaknesses, teamwork, or career.
- For Project Based interviews, ask about projects mentioned in the resume.
- Keep the question suitable for a placement interview.
- Return ONLY the question.
"""

    try:

        with st.spinner("🎤 Generating a new interview question..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        question = response.text.strip()

        question = re.sub(
            r"^(question\s*:|q\s*:)\s*",
            "",
            question,
            flags=re.IGNORECASE
        ).strip()

        if question in previous_questions:

            st.warning(
                "⚠️ A duplicate question was generated. Please click the button again."
            )

        else:

            st.session_state["interview_question"] = question

            st.session_state["asked_questions"].append(
                question
            )

            st.session_state["interview_answer"] = None
            st.session_state["interview_evaluation"] = None

    except Exception as e:

        if "429" in str(e):

            st.error(
                "⚠️ AI service is temporarily busy. "
                "Please wait a moment and try again."
            )

        else:

            st.error(
                "❌ Unable to generate interview question."
            )

            st.error(
                f"Error: {e}"
            )

if st.session_state.get("interview_question"):

    st.subheader("❓ Interview Question")

    st.info(
        st.session_state["interview_question"]
    )

    st.subheader("✍️ Your Answer")

    answer = st.text_area(
        "Type your answer below:",
        height=200,
        placeholder="Enter your interview answer here..."
    )

    if st.button("📤 Submit Answer"):

        if not answer.strip():

            st.warning(
                "⚠️ Please enter your answer first."
            )

            st.stop()

        st.session_state["interview_answer"] = answer

        evaluation_prompt = f"""
You are an experienced placement interviewer evaluating a candidate's answer.

Interview Type:
{interview_type}

Interview Question:
{st.session_state["interview_question"]}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Return the evaluation in exactly this format:

## Score
X/10

## Strengths
- Strength 1
- Strength 2
- Strength 3

## Improvements
- Improvement 1
- Improvement 2
- Improvement 3

## Better Answer
Provide an example of a stronger answer.

Rules:
- Give a score between 0 and 10.
- Evaluate correctness, relevance, clarity, confidence, and completeness.
- Keep the feedback constructive.
"""

        try:

            with st.spinner(
                "🤖 Evaluating your answer..."
            ):

                evaluation_response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=evaluation_prompt
                )

            evaluation_text = evaluation_response.text.strip()

            st.session_state[
                "interview_evaluation"
            ] = evaluation_text

            st.subheader(
                "📊 Interview Evaluation"
            )

            st.markdown(
                evaluation_text
            )

            score_match = re.search(
                r"(?:score).*?(\d+(?:\.\d+)?)\s*/\s*10",
                evaluation_text,
                re.IGNORECASE | re.DOTALL
            )

            if not score_match:

                score_match = re.search(
                    r"(\d+(?:\.\d+)?)\s*/\s*10",
                    evaluation_text
                )

            if score_match:

                interview_score = float(
                    score_match.group(1)
                )

                st.session_state[
                    "interview_score"
                ] = interview_score

        except Exception as e:

            if "429" in str(e):

                st.error(
                    "⚠️ AI service is temporarily busy. "
                    "Please wait a moment and try again."
                )

            else:

                st.error(
                    "❌ Unable to evaluate the answer."
                )

                st.error(
                    f"Error: {e}"
                )

st.divider()

st.subheader("📚 Interview Progress")

question_count = len(
    st.session_state["asked_questions"]
)

st.write(
    f"🎯 Questions practiced: **{question_count}**"
)

if question_count > 0:

    st.success(
        "🔥 Keep practicing! Each new question will be different."
    )