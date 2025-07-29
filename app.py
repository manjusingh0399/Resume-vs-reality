import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Resume vs Reality", layout="wide")
st.title("📌 Resume vs Reality – Which Skills Help You Get Hired?")

# Load model and encoder
@st.cache_data

def load_model():
    with open("model.pkl", "rb") as f:
        model, mlb = pickle.load(f)
    return model, mlb

model, mlb = load_model()

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", [
    "🔮 Hiring Prediction",
    "📊 Skill Insights Dashboard",
    "📎 Resume vs Job Match"
])

# --------------------- Section 1: Hiring Prediction ---------------------
if section == "🔮 Hiring Prediction":
    st.subheader("🔍 Enter Your Skills")
    user_input = st.text_area("List your skills separated by commas (e.g., Excel, SQL, Communication)",
                              height=150, placeholder="Python, Excel, Teamwork, Leadership")

    if st.button("Predict Likelihood"):
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
            st.success("🟢 Likely to get hired." if pred_label == 1 else "🔴 Less likely to get hired.")

            st.write("### 🔍 Skill Match")
            matched = [s for s in user_skills if s in mlb.classes_]
            unmatched = [s for s in user_skills if s not in mlb.classes_]

            st.write(f"✅ Matched skills: {', '.join(matched)}")
            if unmatched:
                st.write(f"❌ Unrecognized skills: {', '.join(unmatched)}")

# --------------------- Section 2: Skill Insights Dashboard ---------------------
elif section == "📊 Skill Insights Dashboard":
    st.subheader("📊 Skill Frequency and Correlation Insights")

    resumes = pd.read_csv("resumes.csv")
    hired = pd.read_csv("hired_profiles.csv")
    jobs = pd.read_csv("job_enriched.csv")

    resumes['skills'] = resumes['skills_listed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    hired['skills'] = hired['skills_endorsed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    jobs['skills'] = jobs['job_skills'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])

    from collections import Counter

    def get_freq(df, label):
        all_skills = sum(df['skills'].tolist(), [])
        freq = Counter(all_skills)
        df_freq = pd.DataFrame(freq.items(), columns=['skill', f'count_{label}'])
        return df_freq

    resume_freq = get_freq(resumes, 'resumes')
    hired_freq = get_freq(hired, 'hired')
    job_freq = get_freq(jobs, 'jobs')

    df_all = resume_freq.merge(hired_freq, on='skill', how='outer').merge(job_freq, on='skill', how='outer').fillna(0)
    df_all['Resume Inflation Index'] = (df_all['count_resumes'] + 1) / (df_all['count_jobs'] + 1)
    df_all['Hiring Edge'] = (df_all['count_hired'] + 1) / (df_all['count_resumes'] + 1)

    top_skills = df_all.sort_values('count_resumes', ascending=False).head(30)

    fig = px.bar(top_skills.melt(id_vars='skill', value_vars=['count_resumes', 'count_hired', 'count_jobs']),
                 x='skill', y='value', color='variable', barmode='group',
                 title="Top 30 Skill Frequencies Across Resumes, Hired Profiles, and Job Listings")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### 📌 Resume Inflation Index vs Hiring Edge")
    fig2 = px.scatter(df_all, x='Resume Inflation Index', y='Hiring Edge', text='skill',
                      title="Resume Inflation vs Hiring Edge for Each Skill",
                      labels={"Resume Inflation Index": "Overstated on Resumes",
                              "Hiring Edge": "Useful for Getting Hired"})
    fig2.update_traces(textposition='top center')
    st.plotly_chart(fig2, use_container_width=True)

# --------------------- Section 3: Resume vs Job Match ---------------------
elif section == "📎 Resume vs Job Match":
    st.subheader("📎 Compare Resume Skills with Job Description")

    resume_input = st.text_area("Paste your resume skills (comma-separated)", height=150)
    job_input = st.text_area("Paste job description skills (comma-separated)", height=150)

    if st.button("Compare and Evaluate"):
        if not resume_input.strip() or not job_input.strip():
            st.warning("Please fill both sections.")
        else:
            resume_skills = set([s.strip().lower() for s in resume_input.split(',') if s.strip()])
            job_skills = set([s.strip().lower() for s in job_input.split(',') if s.strip()])

            matched = resume_skills & job_skills
            missing = job_skills - resume_skills
            extra = resume_skills - job_skills

            st.write(f"✅ Matched Skills ({len(matched)}):", ', '.join(matched))
            st.write(f"❌ Missing Skills ({len(missing)}):", ', '.join(missing))
            st.write(f"➕ Extra Resume Skills ({len(extra)}):", ', '.join(extra))

            match_score = len(matched) / len(job_skills) if job_skills else 0
            st.metric("🔍 Relevance Score", f"{match_score*100:.2f}%")

            if match_score > 0.7:
                st.success("🎯 Great match! You're well aligned with the job description.")
            elif match_score > 0.4:
                st.warning("⚠️ Partial match. Consider learning the missing skills.")
            else:
                st.error("❌ Low match. You may not be a strong fit without upskilling.")
