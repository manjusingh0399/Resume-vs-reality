import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# ---------- CUSTOM CSS ----------
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
        color: #ff69b4;
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #ffa07a;
        color: black;
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: white;
    }
    .insight {
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        font-size: 16px;
        color: white;
    }
    .positive { background-color: #006400; }
    .warning { background-color: #8b0000; }
    .neutral { background-color: #483d8b; }
    </style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
resumes = pd.read_csv("resumes.csv")
hired = pd.read_csv("hired_profiles.csv")
jobs = pd.read_csv("job_enriched.csv")

resumes["skills"] = resumes["skills_listed"]
hired["skills"] = hired["skills_endorsed"]
jobs["skills"] = jobs["skills_required"]

# ---------- TITLE ----------
st.title("✨ Resume vs Reality ✨")
st.markdown("You + Data = Dream Job 🪄 Let's uncover what *really* gets you hired. 🎯", unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🔥 In-Demand Skills", "🧠 Reality Check"])

# ---------- HELPERS ----------
@st.cache_data
def get_top_skills(df, column):
    all_skills = df[column].dropna().str.lower().str.split(",|;|\\|")
    flat_skills = [s.strip().strip("[]()\"' ") for sublist in all_skills for s in sublist if s.strip()]
    return pd.Series(flat_skills).value_counts()

# ---------- TAB 1: In-Demand Skills ----------
with tab1:
    st.header("📊 What's Hot in the Market?")
    st.markdown("Here's what employers want vs what actually gets people hired:")

    col1, col2 = st.columns(2)

    with col1:
        top_job_skills = get_top_skills(jobs, "skills").head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_job_skills.values, y=top_job_skills.index, ax=ax, palette="rocket")
        ax.set_title("Top Skills in Job Descriptions", color="white")
        ax.tick_params(colors="white")
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        st.pyplot(fig)
        st.markdown("<div class='insight neutral'>📌 These are the skills *most asked for* by recruiters.</div>", unsafe_allow_html=True)

    with col2:
        top_hired_skills = get_top_skills(hired, "skills").head(10)
        fig2, ax2 = plt.subplots()
        sns.barplot(x=top_hired_skills.values, y=top_hired_skills.index, ax=ax2, palette="flare")
        ax2.set_title("Top Skills in Hired Profiles", color="white")
        ax2.tick_params(colors="white")
        fig2.patch.set_facecolor("black")
        ax2.set_facecolor("black")
        st.pyplot(fig2)
        st.markdown("<div class='insight positive'>🌟 These are the skills that actually *got people hired*. Major green flags!</div>", unsafe_allow_html=True)

    # 🔁 Overlap and Insight
    common_skills = set(top_job_skills.index) & set(top_hired_skills.index)
    only_in_resumes = set(top_job_skills.index) - common_skills

    st.subheader("🎯 Skill Gap Analysis")
    st.markdown(f"<div class='insight positive'>✅ Common Winning Skills: {', '.join(common_skills)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight warning'>❗ Resume Buzzwords That Might Be Overrated: {', '.join(only_in_resumes)}</div>", unsafe_allow_html=True)

# ---------- TAB 2: Reality Check ----------
with tab2:
    st.header("🧠 Reality Check: How Do You Compare?")
    st.markdown("Enter your current skills below and we'll compare them to what's hot 🔥")

    user_input = st.text_input("💌 Type your skills (comma-separated)", placeholder="e.g. Excel, Python, Communication")

    if user_input:
        user_skills = set([s.strip().lower() for s in user_input.split(",") if s.strip()])

        top_job = set(get_top_skills(jobs, "skills").head(15).index)
        top_hired = set(get_top_skills(hired, "skills").head(15).index)

        match_job = user_skills & top_job
        match_hired = user_skills & top_hired
        missing = (top_job | top_hired) - user_skills

        st.markdown(f"<div class='insight positive'>✨ You're aligned with job listings on: {', '.join(match_job) if match_job else 'None 😬'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='insight neutral'>🧠 Matched with hired profiles: {', '.join(match_hired) if match_hired else 'None'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='insight warning'>📚 Consider learning: {', '.join(missing) if missing else 'You’re slaying it! 🔥'}</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("<hr style='border-top: 1px solid pink;'>", unsafe_allow_html=True)
st.markdown("<center style='color: white;'>🧁 Built with sass, stats, and sisterly advice. Keep learning. Keep slaying. 💻✨</center>", unsafe_allow_html=True)
