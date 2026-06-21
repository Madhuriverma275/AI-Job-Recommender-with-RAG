import streamlit as st

from model import JobRecommender
from rag import generate_career_advice
from utils import extract_skills, extract_text_from_pdf

st.set_page_config(page_title="AI Job Recommender", page_icon="🚀")

st.title("🚀 AI Job Recommendation System")
st.markdown("### Upload your resume and get smart job suggestions")

@st.cache_resource
def load_recommender(csv_path="jobs.csv"):
    return JobRecommender.from_csv(csv_path)

recommender = load_recommender()

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(text)

    if not text.strip():
        st.warning("Unable to read text from the uploaded PDF.")
    else:
        st.success("✅ Resume processed!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧠 Skills")
            st.write(skills or "No recognized skills found.")

        with col2:
            st.subheader("📄 Resume Preview")
            st.write(text[:300] + "..." if len(text) > 300 else text)

        st.subheader("💼 Recommended Jobs")
        if skills:
            jobs = recommender.recommend(" ".join(skills))
        else:
            st.info("No known skills were detected. Showing top jobs instead.")
            jobs = recommender.recommend("", top_n=5)

        st.dataframe(jobs[['job_title', 'skills']])

        st.subheader("🤖 AI Career Advice")
        advice = generate_career_advice(skills)
        st.info(advice)
