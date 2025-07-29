import streamlit as st
import pandas as pd
import plotly.express as px

# ---- THEME COLORS ----
BLACK = "#131313"
PINK = "#ff4da6"
WHITE = "#f3f3fa"
TEAL = "#65fcda"
GRAY = "#22272B"

st.set_page_config(
    page_title="Resume vs Reality",
    page_icon=":sparkles:",
    layout="wide"
)

st.markdown(f"""
    <style>
    .reportview-container {{
        background: {BLACK};
        color: {WHITE};
    }}
    .sidebar .sidebar-content {{
        background: {BLACK}; color: {WHITE};
    }}
    .stButton>button {{
        border-radius:12px; background:{PINK}; color:{WHITE};
        font-weight:bold; border:none; font-size:18px;
        box-shadow:0 2px 8px rgba(0,0,0,0.18);
    }}
    .stRadio>div>label {{
        background:{GRAY};
        color:{WHITE};
        border-radius:9px; padding:8px 14px;
        margin-right:8px;
    }}
    .css-17eq0hr {{
        color: {PINK} !important;
    }}
    .big-font {{
        font-size:36px !important;
        font-weight:700; color:{PINK};
        margin-bottom:12px;
    }}
    .insight-card {{
        border-radius:12px; background:{WHITE}; color:{BLACK};
        padding:18px 20px; margin:12px 0; font-size:18px;
        box-shadow:0 1px 6px #2222;
        border-left:6px solid {PINK};
    }}
    .score-bar-container {{
        background:{WHITE}; color:{BLACK};
        border-radius:10px; height:26px; margin: 12px 0; width: 100%;
        border:1.5px solid {PINK}; box-shadow:0 1px 6px #0001;
        display:flex; align-items:center; overflow:hidden;
    }}
    .score-bar-fill {{
        height:26px; background:{PINK}; color:{BLACK};
        font-weight:bold; text-align:center; 
        padding-left:12px; display:flex; align-items:center;
        font-size:18px;
        transition:width 0.9s;
    }}
    </style>
""", unsafe_allow_html=True)

# ---- SIDEBAR NAVIGATION ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Overview", "Key Insights", "Role Explorer", "My Resume vs Reality", "About"])

@st.cache_data
def load_data():
    job_df = pd.read_csv("job_enriched.csv")
    resume_df = pd.read_csv("synthetic_resumes.csv")
    hired_df = pd.read_csv("synthetic_hired_profiles.csv")
    return job_df, resume_df, hired_df

job_df, resume_df, hired_df = load_data()

# ------- SCORE & FEEDBACK UTILITIES -------
def get_hired_skills_by_role(role):
    # Placeholder: Adjust with your real role-to-skill mapping logic
    skill_dict = {
        "Analyst": {"Python", "SQL", "Excel", "Data Visualization"},
        "Marketing": {"Canva", "Market Research", "SEO", "Content Creation"},
        "HR": {"Communication", "Recruitment", "Excel", "Teamwork"},
        "Sales": {"Communication", "Negotiation", "CRM", "Excel"}
    }
    return skill_dict.get(role, {"Excel", "Communication"})

def get_feedback(user_skills, target_skills):
    missing = target_skills - user_skills
    feedback = []
    for skill in missing:
        # Customize feedback as you want
        advice = {
            "Python": "Learning Python will make you stand out for analyst/data roles.",
            "SQL": "SQL is highly valued by employers in data-driven jobs.",
            "Excel": "Even basic Excel mastery is foundational for most office jobs.",
            "Data Visualization": "Try learning Tableau or Power BI to visualize data better.",
            "Canva": "Design skills like Canva boost your appeal in marketing roles.",
            "Market Research": "Strengthen your market research expertise for marketing opportunities.",
            "SEO": "Understanding SEO is critical for digital marketing roles.",
            "Content Creation": "Try building a content portfolio—great for creative/marketing paths.",
            "Recruitment": "Recruitment know-how is essential for HR advancement.",
            "Teamwork": "Showcasing team projects gives you an edge for HR jobs.",
            "Negotiation": "Negotiation skills can be your differentiator in sales.",
            "CRM": "Learn Salesforce or HubSpot for a leg up in Sales or Customer Success."
        }
        feedback.append(advice.get(skill, f"Consider developing your {skill} skill!"))
    return feedback

# ------- PAGE LOGIC -------
if page == "My Resume vs Reality":
    st.header("Your Skills: How Do You Match The Market?")
    st.write("Enter your skills (comma-separated), choose your target role, and see your fit score—plus personalized feedback!")
    user_input = st.text_input("List your skills", "Excel, Communication, Python")
    role = st.selectbox("Target Role", ["Analyst", "Marketing", "HR", "Sales"])
    user_skills = set([s.strip().capitalize() for s in user_input.split(",") if s.strip()])
    target_skills = get_hired_skills_by_role(role)

    # --- Calculate Fit Score ---
    matched = user_skills & target_skills
    missing = target_skills - user_skills
    score = int(100 * len(matched) / len(target_skills)) if target_skills else 0

    # --- Animated Progress Bar ---
    st.markdown(f"""
        <div class="score-bar-container">
            <div class="score-bar-fill" style="width: {score}%;">Resume Fit Score: {score}/100</div>
        </div>
    """, unsafe_allow_html=True)
    
    if score == 100:
        st.markdown(
            '<div class="insight-card" style="border-left:6px solid #65fc65;">🎉 Outstanding!<br>You have all the key skills for this role. Go crush those interviews!</div>',
            unsafe_allow_html=True)
    elif score >= 60:
        st.markdown(
            f'<div class="insight-card">Great! You match {len(matched)} out of {len(target_skills)} essential {role} skills: <b>{", ".join(matched) if matched else "None yet"}</b>.</div>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class
