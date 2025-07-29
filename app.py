import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# Custom CSS for dark theme with white text and pink highlights
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    .main {
        background-color: black;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ff69b4; /* pink */
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
resumes = pd.read_csv("resumes.csv")
hired = pd.read_csv("hired_profiles.csv")
jobs = pd.read_csv("job_enriches.csv")

# Title and Introduction
st.title("✨ Resume vs Reality ✨")
st.markdown("Because what you *say* you know and what actually gets you hired... are two different stories 💅")

# Sidebar Navigation
section = st.sidebar.radio("Jump to Section", ["Top 10 In-Demand Skills", "Reality Check: Where Do You Stand?", "Raw Data"])

# Helper function: Top 10 skills
@st.cache_data
def get_top_skills(df, column):
    all_skills = df[column].dropna().str.lower().str.split(", |,|")
    skills_series = pd.Series([skill.strip() for sublist in all_skills for skill in sublist])
    return skills_series.value_counts().head(10)

# Section: Top 10 In-Demand Skills
if section == "Top 10 In-Demand Skills":
    st.header("🔥 Top 10 In-Demand Skills")
    st.markdown("From job descriptions and hired profiles ✨")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Job Descriptions")
        top_job_skills = get_top_skills(jobs, "skills")
        fig, ax = plt.subplots()
        sns.barplot(x=top_job_skills.values, y=top_job_skills.index, ax=ax, palette="pink")
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Skill")
        ax.set_title("Top 10 Skills in Job Descriptions", color="white")
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        st.pyplot(fig)
        st.markdown("🔍 **Insight:** These are the skills most often requested by employers in job posts.")

    with col2:
        st.subheader("Hired Profiles")
        top_hired_skills = get_top_skills(hired, "skills")
        fig2, ax2 = plt.subplots()
        sns.barplot(x=top_hired_skills.values, y=top_hired_skills.index, ax=ax2, palette="pink")
        ax2.set_xlabel("Frequency")
        ax2.set_ylabel("Skill")
        ax2.set_title("Top 10 Skills in Hired Profiles", color="white")
        fig2.patch.set_facecolor('black')
        ax2.set_facecolor('black')
        ax2.tick_params(colors='white')
        ax2.xaxis.label.set_color('white')
        ax2.yaxis.label.set_color('white')
        ax2.title.set_color('white')
        st.pyplot(fig2)
        st.markdown("🎯 **Insight:** These are the skills that actually landed candidates their jobs.")

# Section: Reality Check
elif section == "Reality Check: Where Do You Stand?":
    st.header("🧠 Reality Check: Where Do You Stand?")
    st.markdown("Let's compare your skillset to what’s trending. Enter your skills below 👇")

    user_input = st.text_input("Enter your skills (comma-separated, e.g., Python, Excel, SQL)", "")
    if user_input:
        user_skills = set([skill.strip().lower() for skill in user_input.split(',')])

        job_top_skills = set(get_top_skills(jobs, "skills").index)
        hired_top_skills = set(get_top_skills(hired, "skills").index)

        job_match = user_skills & job_top_skills
        hired_match = user_skills & hired_top_skills
        missing_skills = (job_top_skills | hired_top_skills) - user_skills

        st.subheader("✨ Here's how you stack up:")
        st.markdown(f"**Skills Matching Job Descriptions:** {', '.join(job_match) if job_match else 'None'}")
        st.markdown(f"**Skills Matching Hired Profiles:** {', '.join(hired_match) if hired_match else 'None'}")
        st.markdown(f"**You Might Want to Learn:** {', '.join(missing_skills) if missing_skills else 'You’ve nailed it! 🎯'}")

# Section: Raw Data
elif section == "Raw Data":
    st.header("📂 Raw Data Preview")
    st.markdown("Because you're data-curious ✨")

    st.subheader("Resumes")
    st.dataframe(resumes.head())

    st.subheader("Hired Profiles")
    st.dataframe(hired.head())

    st.subheader("Jobs")
    st.dataframe(jobs.head())
