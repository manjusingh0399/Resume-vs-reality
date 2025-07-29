import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# Custom CSS for sleek dark-pink-orange theme
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
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff7f50; /* orange */
        color: black;
    }
    .stTextInput>div>div>input {
        background-color: #222;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
resumes = pd.read_csv("resumes.csv")
hired = pd.read_csv("hired_profiles.csv")
jobs = pd.read_csv("job_enriched.csv")

# Fix column names
resumes["skills"] = resumes["skills_listed"]
hired["skills"] = hired["skills_endorsed"]
jobs["skills"] = jobs["skills_required"]  # ← FIXED COLUMN NAME

# Title and Introduction
st.title("✨ Resume vs Reality ✨")
st.markdown("Because what you *say* you know and what actually gets you hired... are two different stories 💅")

# Navigation using tabs
tab1, tab2, tab3 = st.tabs(["🔥 In-Demand Skills", "🧠 Reality Check", "📂 Raw Data"])

@st.cache_data
def get_top_skills(df, column):
    all_skills = df[column].dropna().str.lower().str.split(",|;|\\|")
    flat_skills = [skill.strip().strip("[]()\"'") for sublist in all_skills for skill in sublist if skill.strip()]
    return pd.Series(flat_skills).value_counts().head(10)

# ----------- Tab 1: Top Skills ------------
with tab1:
    st.header("🔥 Top 10 In-Demand Skills")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Job Descriptions")
        top_job_skills = get_top_skills(jobs, "skills")
        fig, ax = plt.subplots()
        sns.barplot(x=top_job_skills.values, y=top_job_skills.index, ax=ax, palette="rocket")
        ax.set_title("Top Skills in Job Descriptions", color="white")
        ax.set_xlabel("Frequency", color="white")
        ax.set_ylabel("Skill", color="white")
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ax.tick_params(colors='white')
        st.pyplot(fig)

    with col2:
        st.subheader("🏆 Hired Profiles")
        top_hired_skills = get_top_skills(hired, "skills")
        fig2, ax2 = plt.subplots()
        sns.barplot(x=top_hired_skills.values, y=top_hired_skills.index, ax=ax2, palette="flare")
        ax2.set_title("Top Skills in Hired Profiles", color="white")
        ax2.set_xlabel("Frequency", color="white")
        ax2.set_ylabel("Skill", color="white")
        fig2.patch.set_facecolor("black")
        ax2.set_facecolor("black")
        ax2.tick_params(colors='white')
        st.pyplot(fig2)

# ----------- Tab 2: Skill Match ------------
with tab2:
    st.header("🧠 Reality Check: Where Do You Stand?")
    user_input = st.text_input("Your Skills (comma-separated)", placeholder="e.g. Excel, Python, SQL")
    if user_input:
        user_skills = set([s.strip().lower() for s in user_input.split(",") if s.strip()])
        top_job = set(get_top_skills(jobs, "skills").index)
        top_hired = set(get_top_skills(hired, "skills").index)
        matched_job = user_skills & top_job
        matched_hired = user_skills & top_hired
        missing = (top_job | top_hired) - user_skills

        st.subheader("💅 Your Skill Status")
        st.success(f"✔️ Matches Job Description: {', '.join(matched_job) if matched_job else 'None'}")
        st.info(f"🎯 Matches Hired Profiles: {', '.join(matched_hired) if matched_hired else 'None'}")
        st.warning(f"📚 Consider Learning: {', '.join(missing) if missing else 'You’re on fire!'}")

# ----------- Tab 3: Data Preview ------------
with tab3:
    st.header("📂 Raw Data Preview")
    st.subheader("Resumes")
    st.dataframe(resumes.head())
    st.subheader("Hired Profiles")
    st.dataframe(hired.head())
    st.subheader("Job Listings")
    st.dataframe(jobs.head())

# Footer
st.markdown("<hr style='border-top: 1px solid pink;'>", unsafe_allow_html=True)
st.markdown("<center style='color: white;'>💁‍♀️ Built with truth, glam, and a dash of sass. Now go get that dream job.</center>", unsafe_allow_html=True)
