import streamlit as st
import pandas as pd
import plotly.express as px

# --- COLORS ---
BLACK = "#18181b"
PINK = "#ff4da6"
WHITE = "#f9fafb"
GRAY = "#232329"
MINT = "#65fcda"
ORANGE = "#ffae42"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Resume vs Reality",
    page_icon=":sparkles:",
    layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown(f"""
    <style>
    body {{background: {BLACK}; color: {WHITE};}}
    .css-10trblm {{color: {PINK}!important;}}
    .stTabs [role="tab"] {{background: {GRAY}; border-radius:12px 12px 0 0; color: {WHITE}; font-weight:700;}}
    .stTabs [aria-selected="true"] {{background: {PINK}; color: {BLACK};}}
    .insight-card {{
        border-radius:13px; background:{WHITE}; color:{BLACK};
        font-size:1.19rem; margin:1.5em 0 .8em 0; padding:1.2em;
        border-left:7px solid {PINK}; box-shadow:0 2px 8px #0002;
    }}
    .big-header {{
        font-size:2.2em; font-weight:bold; color:{PINK};
        text-shadow:0 2px 18px #0007;
        margin-top:.7em; margin-bottom:.2em;
    }}
    .score-bar-container {{background:{WHITE}; border-radius:12px; overflow:hidden;}}
    .score-bar-fill {{background:{PINK}; color:{BLACK}; font-weight:bold; padding:0.4em;}}
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    skills = pd.DataFrame({
        "Skill":["Excel","SQL","Python","Communication","Teamwork","Power BI","Market Research"],
        "Job Ads":[92,76,68,45,41,32,29],
        "Resumes":[88,49,37,93,88,27,30],
        "Hires":[64,54,55,37,31,18,15]
    })
    return skills

skills = load_data()

# --- TABS LAYOUT ---
tabs = st.tabs(["🏠 Home", "📊 Insights", "📈 Role Explorer", "🎯 Score & Feedback", "ℹ️ About"])

# --- HOME ---
with tabs[0]:
    st.markdown('<div class="big-header">Unlock What REALLY Gets You Hired</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-card">Welcome! This tool reveals which resume skills actually matter for landing a job—based on real job ads, resumes & successful hires. Enjoy smart graphics, simple insights, and friendly encouragement. 🚀</div>', unsafe_allow_html=True)
    st.write("Use the tabs above to explore skill demand, discover role-specific tips, and check your personalized fit score!")

# --- INSIGHTS ---
with tabs[1]:
    st.markdown("<h2 style='color:#ff4da6;'>Key Skill Insights</h2>", unsafe_allow_html=True)
    fig = px.bar(skills, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group", color_discrete_sequence=[PINK, WHITE, MINT])
    fig.update_layout(
        plot_bgcolor=BLACK, paper_bgcolor=BLACK, font_color=WHITE,
        legend=dict(font=dict(color=WHITE)), xaxis=dict(color=WHITE), yaxis=dict(color=WHITE)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-card">💡 <b>Insight:</b> Many resumes list soft skills like “Teamwork” and “Communication”, but hiring often favors tools like SQL and Python for Analyst and Tech roles.</div>', unsafe_allow_html=True)

# --- ROLE EXPLORER ---
with tabs[2]:
    st.markdown("<h2 style='color:#ff4da6;'>Explore By Role</h2>", unsafe_allow_html=True)
    role = st.selectbox("Choose a target job role", ["Analyst", "Marketing", "HR", "Sales"])
    skills_role = {
        "Analyst":["SQL","Python","Excel"],
        "Marketing":["Canva","SEO","Market Research"],
        "HR":["Communication","Recruitment"],
        "Sales":["Negotiation","CRM"]
    }
    core = ", ".join(skills_role.get(role, []))
    st.markdown(f'<div class="insight-card"><b>{role} roles:</b> Key skills include {core}.</div>', unsafe_allow_html=True)

# --- SCORE & FEEDBACK ---
with tabs[3]:
    st.markdown("<h2 style='color:#ff4da6;'>Score & Personalized Feedback</h2>", unsafe_allow_html=True)
    myskills = st.text_input("List your skills (comma-separated)", "Excel, Python, Communication")
    role = st.selectbox("Target role?", list(skills_role.keys()), key=2)
    pick = set([x.strip().capitalize() for x in myskills.split(",") if x.strip()])
    target = set(skills_role.get(role, []))
    score = int(100 * len(pick & target) / len(target)) if target else 0

    st.markdown(f"""<div class='score-bar-container' style='width:100%; max-width:400px;'>
        <div class='score-bar-fill' style='width:{score}%;'>Resume Fit Score: {score}/100</div>
    </div>""", unsafe_allow_html=True)

    missing = target - pick
    advice = {
        "Python":"Learning Python can launch your Analyst career.",
        "SQL":"SQL is crucial for data roles.",
        "Excel":"Excel is essential everywhere.",
        "Canva":"Canva helps tell visual stories for Marketers.",
        "SEO":"SEO skills boost digital marketing jobs.",
        "Market Research":"Strengthen your market research side.",
        "Recruitment":"HR jobs always value recruitment skills.",
        "Communication":"Communication matters in every field.",
        "Negotiation":"Negotiation sets Sales pros apart.",
        "CRM":"Salesforce/HubSpot experience is valued!"
    }

    if score == 100:
        st.markdown('<div class="insight-card" style="border-left:8px solid #65fc65;">🌟 Outstanding! Your resume matches all major skills for this role.</div>', unsafe_allow_html=True)
    elif score >= 60:
        st.markdown(f'<div class="insight-card">You're close! Improve your score by adding: {", ".join(missing)}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-card" style="border-left:8px solid #ffae42;">Let's build your skill set further. Start with:</div>', unsafe_allow_html=True)
        for skill in missing:
            st.markdown(f'<div class="insight-card" style="border-left:7px solid #ffc400;">{advice.get(skill, "Add " + skill.title() + "!")}</div>', unsafe_allow_html=True)

# --- ABOUT ---
with tabs[4]:
    st.markdown("<h2 style='color:#ff4da6;'>About & Credits</h2>", unsafe_allow_html=True)
    st.markdown("<div class='insight-card'>Built with ❤️ by Manju Singh to help you see which skills matter most for your dream job. Powered by real hiring data, simple visuals, and personalized guidance. Professional. Insightful. You-ready.</div>", unsafe_allow_html=True)
