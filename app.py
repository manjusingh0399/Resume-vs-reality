import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
from collections import Counter

# --- Page Setup ---
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# --- Theme Colors ---
PINK = "#ff69b4"
ORANGE = "#ffa07a"
BLACK = "#1c1c1c"
WHITE = "#ffffff"
BG = BLACK
TEXT = WHITE

# --- Custom CSS Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG};
        color: {TEXT};
    }}
    .stButton>button {{
        background-color: {PINK};
        color: white;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {ORANGE};
        color: black;
    }}
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stTextInput, .stTextArea, .stMetric {{
        color: {TEXT} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
    <h1 style='text-align: center;'>💼 Resume vs Reality</h1>
    <h3 style='text-align: center; color: {ORANGE};'>Real Talk: What's Hot in Hiring</h3>
    <p style='text-align: center;'>🌟 Get the lowdown on what recruiters really want vs. what we all *think* they want.<br>Wiser than your older sister. Prettier than your resume. Tougher than your interview questions.</p>
    <hr style='border: 1px solid {PINK};'>
""", unsafe_allow_html=True)

# --- Load Model ---
@st.cache_data
def load_model():
    with open("model.pkl", "rb") as f:
        model, mlb = pickle.load(f)
    return model, mlb

model, mlb = load_model()

# --- Section Nav ---
section = st.selectbox("👇 Pick your power tool:", [
    "🔮 Hiring Prediction",
    "📊 Skill Insights Dashboard",
    "📎 Resume vs Job Match"
])

# ----------------- SECTION 1: Hiring Prediction -----------------
if section == "🔮 Hiring Prediction":
    st.header("🔮 Hiring Likelihood Predictor")
    st.markdown("_Drop your skills like they're hot (comma-separated)._ 📝")

    user_input = st.text_area("💡 Your Skills", placeholder="e.g., Python, Excel, Communication", height=120)

    if st.button("🔥 Check My Chances"):
        if not user_input.strip():
            st.warning("⚠️ C'mon now. You gotta enter something!")
        else:
            user_skills = [s.strip().lower() for s in user_input.split(',') if s.strip()]
            input_vector = np.zeros(len(mlb.classes_))
            for skill in user_skills:
                if skill in mlb.classes_:
                    input_vector[np.where(mlb.classes_ == skill)[0][0]] = 1

            pred_proba = model.predict_proba([input_vector])[0][1]
            pred_label = model.predict([input_vector])[0]

            st.metric("📈 Hiring Odds", f"{pred_proba*100:.2f}%")
            st.success("💃 You're totally hireable!" if pred_label == 1 else "😬 Might need to glow-up those skills.")

            matched = [s for s in user_skills if s in mlb.classes_]
            unmatched = [s for s in user_skills if s not in mlb.classes_]

            st.markdown(f"**✅ Recognized:** {', '.join(matched) if matched else 'None'}")
            if unmatched:
                st.markdown(f"**🤷 Not in model:** {', '.join(unmatched)}")

# ----------------- SECTION 2: Skill Insights Dashboard -----------------
elif section == "📊 Skill Insights Dashboard":
    st.header("📊 Skills Dashboard: Resume vs Reality")
    st.markdown("_Let’s see who’s flexing too hard on their resume (or not enough)._")

    resumes = pd.read_csv("resumes.csv")
    hired = pd.read_csv("hired_profiles.csv")
    jobs = pd.read_csv("job_enriched.csv")

    resumes['skills'] = resumes['skills_listed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    hired['skills'] = hired['skills_endorsed'].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])

    try:
        skill_col = next(col for col in jobs.columns if 'skill' in col.lower())
        jobs['skills'] = jobs[skill_col].fillna('').apply(lambda x: [i.strip().lower() for i in str(x).split(',')])
    except StopIteration:
        st.error("❌ Couldn't find skill column in jobs file.")
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

    top10_all = df_all.sort_values('count_resumes', ascending=False).head(10)
    st.subheader("🎓 Top 10 Most Listed Skills")
    st.plotly_chart(px.bar(
        top10_all.melt(id_vars='skill', value_vars=['count_resumes', 'count_hired', 'count_jobs']),
        x='skill', y='value', color='variable', barmode='group',
        color_discrete_sequence=[PINK, ORANGE, '#ffcccb'],
        title="Top 10: Resume vs Hired vs Jobs"
    ), use_container_width=True)

    st.subheader("📉 Resume Inflation vs Hiring Edge")
    fig = px.scatter(
        df_all, x='Resume Inflation Index', y='Hiring Edge', text='skill',
        title="Skill Positioning Matrix",
        labels={"Resume Inflation Index": "Oversold on Resumes", "Hiring Edge": "Actually Gets You Hired"}
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(height=600, plot_bgcolor=BG, paper_bgcolor=BG, font=dict(color=TEXT))
    st.plotly_chart(fig, use_container_width=True)

    # Bonus: Top Hiring Skills Pie & Bar
    df_all['skill'] = df_all['skill'].str.replace(r"[\[\]'\"]", '', regex=True)
    top10 = df_all.sort_values('Hiring Edge', ascending=False).head(10)

    fig_bar = px.bar(
        top10, x='skill', y='Hiring Edge', color='Hiring Edge',
        title='💡 Top 10 Skills That Boost Hiring Chances',
        text='skill', color_continuous_scale='sunset',
        labels={'Hiring Edge': 'Hiring Probability Boost'}
    )
    fig_bar.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font=dict(color=TEXT), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        top10, names='skill', values='count_hired',
        title='📈 Distribution of Top Hiring Skills',
        color_discrete_sequence=px.colors.sequential.RdPu
    )
    fig_pie.update_layout(paper_bgcolor=BG, font=dict(color=TEXT))
    st.plotly_chart(fig_pie, use_container_width=True)

# ----------------- SECTION 3: Resume vs Job Match -----------------
elif section == "📎 Resume vs Job Match":
    st.header("📎 Resume vs JD: Skill Match")
    st.markdown("_Compare your resume to the job posting like a detective with tea._ 🔍☕")

    resume_input = st.text_area("📄 Resume Skills", height=120)
    job_input = st.text_area("📝 Job Description Skills", height=120)

    if st.button("🧪 Analyze Match"):
        if not resume_input.strip() or not job_input.strip():
            st.warning("⚠️ Babe, we need both fields filled.")
        else:
            resume_skills = set([s.strip().lower() for s in resume_input.split(',') if s.strip()])
            job_skills = set([s.strip().lower() for s in job_input.split(',') if s.strip()])

            matched = resume_skills & job_skills
            missing = job_skills - resume_skills
            extra = resume_skills - job_skills

            st.success(f"✅ Matched Skills ({len(matched)}): {', '.join(matched) if matched else 'None'}")
            st.warning(f"❌ Missing Skills ({len(missing)}): {', '.join(missing) if missing else 'None'}")
            st.info(f"➕ Extra Skills ({len(extra)}): {', '.join(extra) if extra else 'None'}")

            match_score = len(matched) / len(job_skills) if job_skills else 0
            st.metric("🎯 Relevance Score", f"{match_score*100:.2f}%")

            if match_score > 0.7:
                st.success("🚀 Stellar match! You're their dream date.")
            elif match_score > 0.4:
                st.warning("🤔 Decent-ish. A little polish and you're golden.")
            else:
                st.error("💔 Uh-oh. Might need a skill makeover.")
