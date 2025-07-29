import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
from collections import Counter

# --- Page Setup ---
st.set_page_config(page_title="Resume vs Reality", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #003262;'>📌 Resume vs Reality</h1>
    <h4 style='text-align: center; color: grey;'>Which Skills Actually Help You Get Hired?</h4>
    <hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# --- Load Model and Encoder ---
@st.cache_data
def load_model():
    with open("model.pkl", "rb") as f:
        model, mlb = pickle.load(f)
    return model, mlb

model, mlb = load_model()

# --- Sidebar Navigation ---
st.sidebar.title("🔍 Explore")
section = st.sidebar.radio("Jump to", [
    "🔮 Hiring Prediction",
    "📊 Skill Insights Dashboard",
    "📎 Resume vs Job Match"
])

# ----------------- SECTION 1: Hiring Prediction -----------------
if section == "🔮 Hiring Prediction":
    st.subheader("🔮 Predict Your Hiring Potential")
    st.markdown("Enter your **skills**, and we'll tell you how likely you are to be hired based on real-world data!")

    user_input = st.text_area("🧠 Your Skills (comma-separated)", placeholder="e.g., Python, Excel, Communication", height=120)

    if st.button("🔍 Predict Hiring Likelihood"):
        if not user_input.strip():
            st.warning("⚠️ Please enter at least one skill.")
        else:
            user_skills = [s.strip().lower() for s in user_input.split(',') if s.strip()]
            input_vector = np.zeros(len(mlb.classes_))
            for skill in user_skills:
                if skill in mlb.classes_:
                    input_vector[np.where(mlb.classes_ == skill)[0][0]] = 1

            pred_proba = model.predict_proba([input_vector])[0][1]
            pred_label = model.predict([input_vector])[0]

            st.metric("📈 Likelihood of Getting Hired", f"{pred_proba*100:.2f}%")
            st.success("🟢 Likely to be hired." if pred_label == 1 else "🔴 Less likely to be hired.")

            matched = [s for s in user_skills if s in mlb.classes_]
            unmatched = [s for s in user_skills if s not in mlb.classes_]

            st.markdown(f"**✅ Recognized Skills:** {', '.join(matched) if matched else 'None'}")
            if unmatched:
                st.markdown(f"**⚠️ Not in model:** {', '.join(unmatched)}")

# ----------------- SECTION 2: Skill Insights Dashboard -----------------
elif section == "📊 Skill Insights Dashboard":
    st.subheader("📊 Skills in Resumes vs Reality")
    st.info("This dashboard compares skill frequency across resumes, hired candidates, and job listings.")

    # Load Data
    resumes = pd.read_csv("resumes.csv")
    hired = pd.read_csv("hired_profiles.csv")
    jobs = pd.read_csv("job_enriched.csv")

    resumes['skills'] = resumes['skills_listed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    hired['skills'] = hired['skills_endorsed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])

    # ✅ Safe skill column detection for job data
    st.write("📄 Columns in job_enriched.csv:", jobs.columns.tolist())
    try:
        skill_col = next(col for col in jobs.columns if 'skill' in col.lower())
        jobs['skills'] = jobs[skill_col].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    except StopIteration:
        st.error("❌ No column containing 'skill' found in job_enriched.csv.")
        st.stop()

    def get_freq(df, label):
        all_skills = sum(df['skills'].tolist(), [])
        freq = Counter(all_skills)
        return pd.DataFrame(freq.items(), columns=['skill', f'count_{label}'])

    resume_freq = get_freq(resumes, 'resumes')
    hired_freq = get_freq(hired, 'hired')
    job_freq = get_freq(jobs, 'jobs')

    df_all = resume_freq.merge(hired_freq, on='skill', how='outer').merge(job_freq, on='skill', how='outer').fillna(0)
    df_all['Resume Inflation Index'] = (df_all['count_resumes'] + 1) / (df_all['count_jobs'] + 1)
    df_all['Hiring Edge'] = (df_all['count_hired'] + 1) / (df_all['count_resumes'] + 1)

    st.markdown("### 🔝 Top 25 Skills Across All Sources")
    top_skills = df_all.sort_values('count_resumes', ascending=False).head(25)
    st.plotly_chart(px.bar(
        top_skills.melt(id_vars='skill', value_vars=['count_resumes', 'count_hired', 'count_jobs']),
        x='skill', y='value', color='variable', barmode='group',
        title="Top 25 Skills: Resumes vs Hired vs Job Listings"
    ), use_container_width=True)

    st.markdown("### ⚖️ Resume Inflation vs Hiring Edge")
    st.plotly_chart(px.scatter(
        df_all, x='Resume Inflation Index', y='Hiring Edge', text='skill',
        title="Skill Positioning Matrix",
        labels={"Resume Inflation Index": "Overstated on Resumes", "Hiring Edge": "Valuable for Hiring"},
    ), use_container_width=True)

# ----------------- SECTION 3: Resume vs Job Match -----------------
elif section == "📎 Resume vs Job Match":
    st.subheader("📎 Skill Alignment Checker")
    st.markdown("Compare your resume skills with a job description to check alignment and missing areas.")

    resume_input = st.text_area("🧾 Resume Skills (comma-separated)", height=120)
    job_input = st.text_area("🧾 Job Description Skills (comma-separated)", height=120)

    if st.button("🔍 Compare and Score"):
        if not resume_input.strip() or not job_input.strip():
            st.warning("⚠️ Please fill both fields.")
        else:
            resume_skills = set([s.strip().lower() for s in resume_input.split(',') if s.strip()])
            job_skills = set([s.strip().lower() for s in job_input.split(',') if s.strip()])

            matched = resume_skills & job_skills
            missing = job_skills - resume_skills
            extra = resume_skills - job_skills

            st.success(f"✅ Matched Skills ({len(matched)}): {', '.join(matched) if matched else 'None'}")
            st.warning(f"❌ Missing Skills ({len(missing)}): {', '.join(missing) if missing else 'None'}")
            st.info(f"➕ Extra Resume Skills ({len(extra)}): {', '.join(extra) if extra else 'None'}")

            match_score = len(matched) / len(job_skills) if job_skills else 0
            st.metric("🎯 Relevance Score", f"{match_score*100:.2f}%")

            if match_score > 0.7:
                st.success("🚀 Strong Match! You align well with the job.")
            elif match_score > 0.4:
                st.warning("⚠️ Moderate Match. Upskilling might help.")
            else:
                st.error("❌ Weak Match. Consider learning missing skills.")
