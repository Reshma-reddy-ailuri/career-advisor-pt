import streamlit as st
from graphviz import Digraph

# ------------------- CSS Styling with background --------------------
API_KEY = st.secrets["api"]["key"]
st.markdown("""
<style>
/* Full-page background */
[data-testid="stAppViewContainer"] {
    background: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbSVDRKJKOmio6hP8gXdPVxMp7ZJTFVbMtjQ&s') no-repeat center center fixed;
    background-size: cover;
    position: relative;
}
/* Overlay for subtle dim */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top:0; left:0;
    width:100%; height:100%;
    background-color: rgba(255,255,255,0.2);
}
/* Card Styling */
.card {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px 35px;
    margin: 30px auto;
    max-width: 850px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
/* Headers */
.card h2, .card h3 {
    color: #333;
    text-align: center;
}
/* Input fields */
.card input, .card select {
    border-radius: 8px;
    border: 1px solid #ccc;
    padding: 10px;
    font-size: 15px;
    background-color: #f9f9f9;
    width: 100%;
    margin-bottom: 10px;
}
/* Buttons */
.card .stButton>button {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    background: #4CAF50;
    color: white;
    font-size: 16px;
    border: none;
}
.card .stButton>button:hover { background: #45a049; }
/* Tabs */
.stTabs [role="tab"] {
    font-weight: bold;
    font-size: 16px;
    color: #333;
}
/* Badge links */
.badge, .link-badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 5px;
    border-radius: 8px;
    font-size: 14px;
}
.badge { background-color: #e0f0ff; color: #007acc; }
.link-badge { background-color: #f0f0f0; color: #0645AD; text-decoration: none; }
/* Profile icon */
.profile-icon {
    position: fixed;
    top: 15px; right: 25px;
    font-size: 18px;
    background: #4CAF50;
    width: 42px; height: 42px;
    border-radius: 50%;
    text-align: center;
    line-height: 42px;
    font-weight: bold;
    color: white;
    z-index: 9999;
}
/* Role section box */
.role-section {
    margin-bottom: 15px;
    padding: 15px;
    background-color: #ffffffdd;
    border-left: 4px solid #4CAF50;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ------------------- Session State --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ------------------- Mock Career Advice Logic --------------------
def generate_career_advice_locally(user_data):
    # Simple logic to pick roles based on target_role keywords (expand as needed)
    target = user_data.get("target_role", "").lower()
    
    career_options = {
        "data scientist": {
            "Description": "Analyze and interpret complex data to help organizations make informed decisions.",
            "Required Skills": ["Python", "SQL", "Machine Learning", "Data Visualization"],
            "Next Steps": ["Build ML projects", "Complete Kaggle competitions", "Learn Cloud deployment"]
        },
        "machine learning engineer": {
            "Description": "Design and deploy ML models into production systems.",
            "Required Skills": ["Python", "TensorFlow/PyTorch", "SQL", "Model Deployment"],
            "Next Steps": ["Work on end-to-end ML projects", "Learn Docker/Kubernetes"]
        },
        "ai developer": {
            "Description": "Develop AI-powered applications and tools.",
            "Required Skills": ["Python", "NLP/Computer Vision", "Deep Learning", "APIs"],
            "Next Steps": ["Build AI apps", "Contribute to open-source AI projects"]
        }
    }
    
    # Pick matching careers or default list
    selected_careers = {}
    for role, details in career_options.items():
        if target in role:
            selected_careers[role] = details
    if not selected_careers:  # if no exact match, show all
        selected_careers = career_options
    
    roadmap = [
        "Learn Python basics",
        "SQL fundamentals",
        "Data Analysis projects",
        "Machine Learning projects",
        "Advanced ML techniques",
        "Cloud deployment & portfolio building"
    ]
    
    skill_gap = (
        "- Missing skills: Cloud Computing, Advanced ML, Data Visualization\n"
        "- Plan: Complete projects, take online courses, practice daily\n"
        "Practice Plan Checklist:\n- [ ] Python Intermediate\n- [ ] SQL Advanced\n- [ ] ML Projects\n- [ ] Cloud Basics"
    )
    
    learning = [
        ("Coursera – Machine Learning", "https://www.coursera.org/learn/machine-learning"),
        ("Udemy – Data Science Bootcamp", "https://www.udemy.com/course/data-science-bootcamp/"),
        ("Kaggle – Hands-on Projects", "https://www.kaggle.com/")
    ]
    
    practice_websites = [
        ("LeetCode", "https://leetcode.com/"),
        ("HackerRank", "https://www.hackerrank.com/"),
        ("Kaggle", "https://www.kaggle.com/")
    ]
    
    job_platforms = [
        ("LinkedIn Jobs", "https://www.linkedin.com/jobs/"),
        ("Naukri.com", "https://www.naukri.com/"),
        ("Indeed", "https://www.indeed.com/")
    ]
    
    return {
        "career": selected_careers,
        "roadmap": roadmap,
        "skill_gap": skill_gap,
        "learning": learning,
        "practice_websites": practice_websites,
        "job_platforms": job_platforms
    }

# ------------------- Render Helpers --------------------
def render_badges(items, badge_class="badge", clickable=False):
    for item in items:
        if clickable and isinstance(item, tuple):
            label, url = item
            st.markdown(f'<a class="{badge_class}" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="{badge_class}">{item if not isinstance(item, tuple) else item[0]}</span>', unsafe_allow_html=True)

def render_checklist(checklist_text):
    if "checklist_states" not in st.session_state:
        st.session_state.checklist_states = {}
    for line in checklist_text.split("\n"):
        line = line.strip()
        if line.startswith("- [ ]"):
            label = line[5:].strip()
            checked = st.session_state.checklist_states.get(label, False)
            st.session_state.checklist_states[label] = st.checkbox(label, value=checked)

def render_graphviz_roadmap(roadmap_steps):
    dot = Digraph(comment="Career Roadmap", format="png")
    dot.attr(rankdir='TB', size='8')
    for i, step in enumerate(roadmap_steps):
        dot.node(str(i), step)
    for i in range(len(roadmap_steps)-1):
        dot.edge(str(i), str(i+1))
    st.graphviz_chart(dot)

def render_career_suggestions(career_dict):
    for role, details in career_dict.items():
        st.markdown(f'<div class="role-section">', unsafe_allow_html=True)
        st.subheader(role)
        st.markdown(f"**Description:** {details.get('Description','')}")
        st.markdown("**Required Skills:** " + ", ".join(details.get("Required Skills", [])))
        st.markdown("**Next Steps:** " + " | ".join(details.get("Next Steps", [])))
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------- Login --------------------
if not st.session_state.logged_in:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>Login to Career Advisor</h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    email = st.text_input("Email")
    if st.button("Login"):
        if username and email:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- Main App --------------------
else:
    st.markdown(f'<div class="profile-icon">{st.session_state.username[0].upper()}</div>', unsafe_allow_html=True)
    st.title(f"Welcome {st.session_state.username} 👋")
    st.write("Explore your personalized career advisor dashboard.")
    
    if not st.session_state.show_results:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Enter Your Profile Details")
        with st.form("user_input_form"):
            age = st.number_input("Age", min_value=10, max_value=100, value=25)
            location = st.text_input("Location")
            education = st.text_input("Education")
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, value=2)
            target_role = st.text_input("Target Career Role")
            skill_1 = st.text_input("Skill 1")
            skill_1_level = st.selectbox("Skill 1 Proficiency", ["Beginner", "Intermediate", "Advanced"])
            skill_2 = st.text_input("Skill 2")
            skill_2_level = st.selectbox("Skill 2 Proficiency", ["Beginner", "Intermediate", "Advanced"])
            skill_3 = st.text_input("Skill 3")
            skill_3_level = st.selectbox("Skill 3 Proficiency", ["Beginner", "Intermediate", "Advanced"])
            submit_btn = st.form_submit_button("Get Career Advice")
        st.markdown('</div>', unsafe_allow_html=True)

        if submit_btn:
            user_data = {
                "age": age,
                "location": location,
                "education": education,
                "experience": years_exp,
                "target_role": target_role,
                "skills": {
                    skill_1.strip(): skill_1_level,
                    skill_2.strip(): skill_2_level,
                    skill_3.strip(): skill_3_level
                }
            }
            st.session_state.user_data = user_data
            st.session_state.advice_data = generate_career_advice_locally(user_data)
            st.session_state.show_results = True
            st.experimental_rerun()
    else:
        advice = st.session_state.get("advice_data", {})
        st.header("AI-Powered Career Advisor Results")
        
        tabs = st.tabs([
            "Career Suggestions",
            "Roadmap",
            "Skill Gap Analysis",
            "Learning Resources",
            "Practice Websites",
            "Job Search Platforms"
        ])

        with tabs[0]:
            career_suggestions = advice.get("career", {})
            if career_suggestions:
                render_career_suggestions(career_suggestions)
            else:
                st.info("No career suggestions available.")

        with tabs[1]:
            roadmap = advice.get("roadmap", [])
            if roadmap:
                render_graphviz_roadmap(roadmap)
            else:
                st.info("No roadmap available.")

        with tabs[2]:
            skill_gap = advice.get("skill_gap", "")
            if skill_gap:
                render_checklist(skill_gap)
            else:
                st.info("No skill gap analysis available.")

        with tabs[3]:
            learning = advice.get("learning", [])
            if learning:
                render_badges(learning, badge_class="link-badge", clickable=True)
            else:
                st.info("No learning resources provided.")

        with tabs[4]:
            practice_websites = advice.get("practice_websites", [])
            if practice_websites:
                render_badges(practice_websites, badge_class="link-badge", clickable=True)
            else:
                st.info("No practice websites listed.")

        with tabs[5]:
            job_platforms = advice.get("job_platforms", [])
            if job_platforms:
                render_badges(job_platforms, badge_class="link-badge", clickable=True)
            else:
                st.info("No job search platforms available.")
