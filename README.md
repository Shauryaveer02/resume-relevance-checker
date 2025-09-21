# resume-relevance-checker
Automated system for evaluating resume relevance to job descriptions
markdown
# 📄 Automated Resume Relevance Check System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)](https://matplotlib.org/)

An intelligent, automated system designed to evaluate resume relevance against job descriptions, built with Streamlit to provide a user-friendly web interface.

## 🌟 Features

- **Automated Resume Evaluation**: Analyze resumes against job requirements at scale
- **Relevance Scoring**: Generate a Relevance Score (0-100) for each resume
- **Gap Analysis**: Highlight missing skills, certifications, or projects
- **Fit Verdict**: Provide suitability assessment (High/Medium/Low)
- **Interactive Dashboard**: Web-based interface for easy access
- **Performance Analytics**: Visualizations of score distributions and skill frequency
- **Sample Data**: Test the system with pre-loaded sample resumes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/resume-relevance-checker.git
cd resume-relevance-checker
Install required dependencies:

bash
pip install -r requirements.txt
Run the application:

bash
streamlit run app.py
Open your browser and navigate to the local URL shown in the terminal (typically http://localhost:8501)

📊 How It Works
1. Select Job Role
Choose from predefined job roles (Data Scientist, Frontend Developer, Backend Developer, DevOps Engineer, Full Stack Developer) or customize the required skills.

2. Upload Resumes
Upload PDF or DOCX resume files for analysis. The system processes each resume to extract skills and relevant information.

3. Analyze & Evaluate
The system calculates a relevance score based on skill matching between the resume and job requirements, providing:

Percentage match score

Suitability verdict (High/Medium/Low)

Matched skills

Missing skills

4. Review Results
View detailed analysis for each candidate with visualizations showing score distribution and skill frequency across all resumes.
