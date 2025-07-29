import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# Custom CSS for black, pink, and orange theme
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

# Title and Introduction
st.title("✨ Resume vs Reality ✨")
st.markdown("Because what you *say* you know and what actually gets you hired... are two different stories 💅")

# Section Navigation
section = st.radio("Choose a section to explore 👇", [
    "🔥 Top 10 In-Demand Skills", 
    "🧠 Reality Check: Where Do You Stand?", 
    "📂 Raw Data Preview"
])

# Helper function
@st.cache_data
def get_top_skills(df, column):
    all_skills = df[column].dropna().str.lower().str.split(",|;|\\|")
    flat_skills = [skill.strip().strip("[]()\"'") for sublist in all_skills for skill in sublist if skill.strip()]
    return pd.Series(flat_skills).value_counts().head(10)

# Section 1: Top 10 Skills
if section == "🔥 Top 10 In-Demand Skills":
    st.header("🔥 Top 10 In-Demand Skills")
    st.markdown("From job descriptions and hired profiles ✨")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Job Descriptions")
        top_job_skills = get_top_skills(jobs, "skills")
        fig, ax = plt.subplots()
        sns.barplot(x=top_job_skills.values, y=top_job_skills.index, ax=ax, palette="rocket")
        ax.set_title("Top 10 Skills in Job Descriptions", color="white")
        ax.set_xlabel("Frequency", color="white")
        ax.set_ylabel("Skill", color="white")
        ax.set_facecolor("black")
        fig.patch.set_facecolor("black")
        ax.tick_params(colors='white')
        st.pyplot(fig)
        st.markdown("🔍 **Insight:** These are the most requested skills in job ads.")

    with col2:
        st.subheader("Hired Profiles")
        top_hired_skills = get_top_skills(hired, "skills")
        fig2, ax2 = plt.subplots()
        sns.barplot(x=top_hired_skills.values, y=top_hired_skills.index, ax=ax2, palette="flare")
        ax2.set_title("Top 10 Skills in Hired Profiles", color="white")
        ax2.set_xlabel("Frequency", color="white")
        ax2.set_ylabel("Skill", color="white")
        ax2.set_facecolor("black")
        fig2.patch.set_facecolor("black")
        ax2.tick_params(colors='white')
        st.pyplot(fig2)
        st.markdown("🎯 **Insight:** These are the skills that actually helped people get hired.")

# Section 2: Reality Check
elif section == "🧠 Reality Check: Where Do You Stand?":
    st.header("🧠 Reality Check: Where Do You Stand?")
    st.markdown("Let’s compare your skills to what’s *actually* hot in the market 🔥")

    user_input = st.text_input("Enter your skills (comma-separated)", placeholder="e.g., Python, Canva, Teamwork")
    if user_input:
        user_skills = set([s.strip().lower() for s in user_input.split(',') if s.strip()])
        job_top = set(get_top_skills(jobs, "skills").index)
        hired_top = set(get_top_skills(hired, "skills").index)

        matched_job = user_skills & job_top
        matched_hired = user_skills & hired_top
        missing_skills = (job_top | hired_top) - user_skills

        st.subheader("💅 Here's your personal scoop:")
        st.markdown(f"**✔️ Matching Job Description Skills:** {', '.join(matched_job) if matched_job else 'None'}")
        st.markdown(f"**🎯 Matching Hired Profile Skills:** {', '.join(matched_hired) if matched_hired else 'None'}")
        st.markdown(f"**📚 Skills to Learn:** {', '.join(missing_skills) if missing_skills else 'You’re killing it! 💖'}")

# Section 3: Raw Data
elif section == "📂 Raw Data Preview":
    st.header("📂 Raw Data Preview")
    st.markdown("Because we like to peek under the hood ✨")

    st.subheader("Resumes")
    st.dataframe(resumes.head())

    st.subheader("Hired Profiles")
    st.dataframe(hired.head())

    st.subheader("Jobs")
    st.dataframe(jobs.head())

# Footer
st.markdown("<hr style='border-top: 1px solid pink;'>", unsafe_allow_html=True)
st.markdown("<center style='color: white;'>💁‍♀️ Powered by data, glam, and honesty. Your career glow-up starts here.</center>", unsafe_allow_html=True)
