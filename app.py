import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Resume Relevance Check System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #1f77b4; margin-bottom: 1rem; }
    .section-header { font-size: 2rem; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 0.5rem; margin-top: 2rem; }
    .highlight { background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .score-card { text-align: center; padding: 20px; border-radius: 10px; margin: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    .high-score { background-color: #d4edda; color: #155724; }
    .medium-score { background-color: #fff3cd; color: #856404; }
    .low-score { background-color: #f8d7da; color: #721c24; }
    .skill-chip { display: inline-block; padding: 5px 15px; margin: 5px; border-radius: 20px; font-weight: 500; }
    .present-skill { background-color: #d4edda; color: #155724; }
    .missing-skill { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resumes' not in st.session_state:
    st.session_state.resumes = []
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

# Sample job roles with required skills
JOB_ROLES = {
    "Data Scientist": ["Python", "Machine Learning", "Data Analysis", "SQL", "Data Visualization", "Statistics"],
    "Frontend Developer": ["JavaScript", "HTML", "CSS", "React", "Angular", "Vue"],
    "Backend Developer": ["Python", "Java", "Node.js", "SQL", "REST API", "Docker"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "CI/CD", "Git", "Azure"],
    "Full Stack Developer": ["JavaScript", "Python", "React", "Node.js", "SQL", "HTML", "CSS"]
}

# Create a comprehensive skills database
all_skills = set()
for skills in JOB_ROLES.values():
    all_skills.update(skills)

# Add additional common skills
additional_skills = [
    'C++', 'Express', 'Django', 'Flask', 'TensorFlow', 'PyTorch', 
    'Deep Learning', 'GraphQL', 'MongoDB', 'PostgreSQL', 'MySQL'
]
all_skills.update(additional_skills)

# Convert to sorted list for the multiselect
SKILLS_DB = sorted(list(all_skills))

# Function to calculate relevance score
def calculate_relevance_score(resume_skills, required_skills):
    if not required_skills:
        return 0
    
    matched_skills = set(resume_skills) & set(required_skills)
    score = (len(matched_skills) / len(required_skills)) * 100
    return min(score, 100)  # Cap at 100

# Function to get fit verdict
def get_fit_verdict(score):
    if score >= 80:
        return "High Suitability", "high-score"
    elif score >= 50:
        return "Medium Suitability", "medium-score"
    else:
        return "Low Suitability", "low-score"

# Function to extract skills from text (simplified)
def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)
    return found_skills

# Function to parse resume (simulated)
def parse_resume(file_content, filename):
    # Extract skills from file content
    skills = extract_skills(file_content)
    
    # Generate mock resume data
    resume_data = {
        "filename": filename,
        "name": f"Candidate {len(st.session_state.resumes) + 1}",
        "email": f"candidate{len(st.session_state.resumes) + 1}@example.com",
        "skills": skills,
        "experience": f"{np.random.randint(1, 10)} years",
        "education": np.random.choice(["B.Tech", "B.E.", "M.Tech", "M.S.", "Ph.D"]),
        "score": 0,
        "verdict": "",
        "verdict_class": "",
        "missing_skills": []
    }
    
    return resume_data

# Function to get valid default skills
def get_valid_default_skills(role):
    # Ensure all default skills are in SKILLS_DB
    role_skills = JOB_ROLES.get(role, [])
    return [skill for skill in role_skills if skill in SKILLS_DB]

# Main app
def main():
    st.title("📄 Automated Resume Relevance Check System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("System Configuration")
        
        # Job role selection
        selected_role = st.selectbox("Select Job Role", list(JOB_ROLES.keys()))
        
        # Get valid default skills for the selected role
        valid_default_skills = get_valid_default_skills(selected_role)
        
        # Custom skills input
        st.subheader("Required Skills")
        required_skills = st.multiselect(
            "Add required skills:",
            options=SKILLS_DB,
            default=valid_default_skills
        )
        
        # File upload
        st.subheader("Upload Resumes")
        uploaded_files = st.file_uploader(
            "Choose PDF or DOCX files", 
            type=["pdf", "docx"], 
            accept_multiple_files=True
        )
        
        # Analyze button
        analyze_btn = st.button("Analyze Resumes", type="primary", use_container_width=True)
        
        # Sample data button
        if st.button("Load Sample Data", use_container_width=True):
            load_sample_data(required_skills)
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Job Requirements")
        st.write(f"**Role:** {selected_role}")
        st.write("**Required Skills:**")
        for skill in required_skills:
            st.markdown(f'<span class="skill-chip present-skill">{skill}</span>', unsafe_allow_html=True)
        
        st.subheader("Uploaded Resumes")
        if st.session_state.resumes:
            for i, resume in enumerate(st.session_state.resumes):
                st.write(f"{i+1}. {resume['filename']} - {resume['name']}")
        else:
            st.info("Upload resumes to get started")
    
    with col2:
        st.subheader("Analysis Results")
        
        if analyze_btn and uploaded_files:
            # Process uploaded files
            for uploaded_file in uploaded_files:
                file_content = str(uploaded_file.read())
                resume_data = parse_resume(file_content, uploaded_file.name)
                
                # Calculate relevance score
                resume_data['score'] = calculate_relevance_score(resume_data['skills'], required_skills)
                
                # Get verdict
                resume_data['verdict'], resume_data['verdict_class'] = get_fit_verdict(resume_data['score'])
                
                # Find missing skills
                resume_data['missing_skills'] = list(set(required_skills) - set(resume_data['skills']))
                
                # Add to session state
                st.session_state.resumes.append(resume_data)
                st.session_state.analysis_results.append(resume_data)
        
        # Display results
        if st.session_state.analysis_results:
            for result in st.session_state.analysis_results:
                with st.expander(f"{result['name']} - Score: {result['score']:.1f}%", expanded=True):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown(f'<div class="score-card {result["verdict_class"]}">'
                                   f'<h3>{result["score"]:.1f}%</h3>'
                                   f'<p>{result["verdict"]}</p>'
                                   f'</div>', unsafe_allow_html=True)
                        
                        st.write("**Experience:**", result["experience"])
                        st.write("**Education:**", result["education"])
                        st.write("**Email:**", result["email"])
                    
                    with col_b:
                        st.write("**Matched Skills:**")
                        for skill in result["skills"]:
                            if skill in required_skills:
                                st.markdown(f'<span class="skill-chip present-skill">{skill}</span>', unsafe_allow_html=True)
                        
                        if result["missing_skills"]:
                            st.write("**Missing Skills:**")
                            for skill in result["missing_skills"]:
                                st.markdown(f'<span class="skill-chip missing-skill">{skill}</span>', unsafe_allow_html=True)
            
            # Visualization
            st.subheader("Performance Analytics")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Score distribution
                scores = [r["score"] for r in st.session_state.analysis_results]
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(scores, bins=10, edgecolor='black', alpha=0.7)
                ax.set_xlabel('Relevance Score (%)')
                ax.set_ylabel('Frequency')
                ax.set_title('Distribution of Relevance Scores')
                st.pyplot(fig)
            
            with chart_col2:
                # Skill frequency
                all_skills = []
                for r in st.session_state.analysis_results:
                    all_skills.extend(r["skills"])
                
                skill_series = pd.Series(all_skills)
                top_skills = skill_series.value_counts().head(10)
                
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.barh(top_skills.index, top_skills.values)
                ax.set_xlabel('Frequency')
                ax.set_title('Top Skills in Resumes')
                st.pyplot(fig)
        
        elif analyze_btn and not uploaded_files:
            st.warning("Please upload at least one resume to analyze.")
        else:
            st.info("Upload resumes and click 'Analyze' to see results here.")

# Function to load sample data
def load_sample_data(required_skills):
    sample_resumes = [
        {
            "filename": "john_doe.pdf",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "Statistics"],
            "experience": "5 years",
            "education": "M.S.",
            "score": calculate_relevance_score(["Python", "Machine Learning", "Data Analysis", "SQL", "Statistics"], required_skills),
            "verdict": "",
            "verdict_class": "",
            "missing_skills": []
        },
        {
            "filename": "jane_smith.pdf",
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "skills": ["Python", "Data Analysis", "SQL", "Data Visualization"],
            "experience": "3 years",
            "education": "B.Tech",
            "score": calculate_relevance_score(["Python", "Data Analysis", "SQL", "Data Visualization"], required_skills),
            "verdict": "",
            "verdict_class": "",
            "missing_skills": []
        },
        {
            "filename": "robert_johnson.pdf",
            "name": "Robert Johnson",
            "email": "robert.j@example.com",
            "skills": ["JavaScript", "HTML", "CSS", "React"],
            "experience": "2 years",
            "education": "B.E.",
            "score": calculate_relevance_score(["JavaScript", "HTML", "CSS", "React"], required_skills),
            "verdict": "",
            "verdict_class": "",
            "missing_skills": []
        }
    ]
    
    # Add verdict and missing skills
    for resume in sample_resumes:
        verdict, verdict_class = get_fit_verdict(resume['score'])
        resume['verdict'] = verdict
        resume['verdict_class'] = verdict_class
        resume['missing_skills'] = list(set(required_skills) - set(resume['skills']))
    
    st.session_state.resumes = sample_resumes
    st.session_state.analysis_results = sample_resumes

if __name__ == "__main__":
    main()
