import streamlit as st
import pandas as pd
import plotly.express as px

BLACK = "#18181b"
PINK = "#ff4da6"
WHITE = "#f9fafb"
GRAY = "#232329"

st.set_page_config(
    page_title="Resume vs Reality",
    page_icon=":sparkles:",
    layout="wide"
)

# --- BOLD CUSTOM THEMING ---
st.markdown(
    f"""
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
    </style>
    """, unsafe_allow_html=True
)

# ---- LOAD DATA (DUMMY for demo, load your own as needed) ----
@st.cache_data
def load_data():
    # df = pd.read_csv("YOURDATA.csv")
    # Replace below with your cleaned processed data
    skills = pd.DataFrame({
        "Skill":["Excel","SQL","Python","Communication","Teamwork","Power BI","Market Research"],
        "Job Ads":[92,76,68,45,41,32,29],
        "Resumes":[88,49,37,93,88,27,30],
        "Hires":[64,54,55,37,31,18,15]
    })
    return skills

skills = load_data()

## ---- TABS BASED UI LAYOUT ----
tab = st.tabs(
    ["🏠 Welcome", "📊 Insights", "📈 Role Explorer", "🎯 Score & Feedback", "ℹ️ About"]
)

with tab[0]:
    st.markdown(f'<div class="big-header">Unlock What REALLY Gets You Hired</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="insight-card">Welcome! This tool reveals which resume skills actually matter for landing a job—based on real job ads, resumes & successful hires. Enjoy smart graphics, simple insights, and friendly encouragement. No confusing data dumps—just what you need to grow. 🚀</div>',
        unsafe_allow_html=True)
    st.write("Use the tabs above to see market reality, role insights, and get your personal fit score!")

with tab[1]:
    st.markdown("<h2 style='color:#ff4da6;'>Key Skill Insights</h2>", unsafe_allow_html=True)
    ## SKILLS BAR GRAPH
    fig = px.bar(
        skills, 
        x="Skill", 
        y=["Job Ads","Resumes","Hires"],
        barmode="group", 
        color_discrete_sequence=[PINK, WHITE, "#65fcda"]
    )
    fig.update_layout(
        plot_bgcolor=BLACK, paper_bgcolor=BLACK, font_color=WHITE, 
        legend=dict(font=dict(color=WHITE)), xaxis=dict(color=WHITE), yaxis=dict(color=WHITE)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<div class="insight-card">💡 <b>Insight:</b> Many resumes list “Teamwork” and “Communication”, but in hiring, real tools—like SQL and Python—give you more odds of landing interviews in Analyst, Data, and Tech roles.</div>',
        unsafe_allow_html=True
    )
    st.markdown("<!-- You can add more advanced graphs/charts here (Venn, trends, etc.) -->")
    # Hide data by never showing st.table or st.dataframe here

with tab[2]:
    st.markdown("<h2 style='color:#ff4da6;'>Explore By Role</h2>", unsafe_allow_html=True)
    role = st.selectbox("Choose a target job role", ["Analyst","Marketing","HR","Sales"])
    # Use YOUR OWN LOGIC replacing below
    skills_role = {"Analyst":["SQL","Python","Excel"],"Marketing":["Canva","SEO","Market Research"],"HR":["Communication","Recruitment"],"Sales":["Negotiation","CRM"]}
    core = ", ".join(skills_role.get(role, []))
    st.markdown(
        f'<div class="insight-card"><b>{role} roles:</b> Skills most likely needed are {core}.</div>', 
        unsafe_allow_html=True)
    # Add role-specific charts here

with tab[3]:
    st.markdown("<h2 style='color:#ff4da6;'>Score & Personalized Feedback</h2>", unsafe_allow_html=True)
    st.write("Enter your skills below to see your fit and get encouraging advice!")
    myskills = st.text_input("List some skills (comma-delimited)", "Excel, Python, Communication")
    role = st.selectbox("For which role?", ["Analyst","Marketing","HR","Sales"], key=2)
    pick = set([x.strip().capitalize() for x in myskills.split(",") if x.strip()])
    target = set(skills_role.get(role, []))
    score = int(100 * len(pick & target) / len(target)) if target else 0
    # Score bar
    st.markdown(
        f"""<div class="score-bar-container" style="width:350px;">
            <div class="score-bar-fill" style="width:{score}%;">Resume Fit Score: {score}/100</div>
           </div>
        """, unsafe_allow_html=True)
    # Feedback
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
    if score==100:
        st.markdown('<div class="insight-card" style="border-left:8px solid #65fc65;">🌟 Outstanding! Your resume matches all major skills for this job.</div>', unsafe_allow_html=True)
    elif score >=60:
        st.markdown(f'<div class="insight-card">{len(target-pick)} improvements possible: {", ".join(missing)}</div>',unsafe_allow_html=True)
    else:
        st.markdown("<div class='insight-card' style='border-left:8px solid #ffae42;'>Let's build your skill set further. Start with:</div>",unsafe_allow_html=True)
        for skill in missing:
            st.markdown(f'<div class="insight-card" style="border-left:7px solid #ffc400;">{advice.get(skill,"Add " + skill.title() + "!")}</div>', unsafe_allow_html=True)
    # Never display raw st.dataframe/st.table here either

with tab[4]:
    st.markdown("<h2 style='color:#ff4da6;'>About & Credits</h2>", unsafe_allow_html=True)
    st.markdown("<div class='insight-card'>Built with ❤️ to help you see which skills matter most for your dream job, drawn from real hiring data and job ads. We never show raw data—only clear, beautiful, personal feedback. Enjoy!</div>", unsafe_allow_html=True)
