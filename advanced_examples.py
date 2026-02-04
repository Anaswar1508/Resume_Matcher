"""
Advanced Resume Screening Examples
Demonstrates different use cases and advanced features
"""

from resume_matcher import ResumeMatcher, ResumeKeywordExtractor


def example_1_basic_ranking():
    """Example 1: Basic ranking of resumes"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Resume Ranking")
    print("="*70 + "\n")
    
    job_desc = """
    Data Science Engineer - Machine Learning
    
    We need a data scientist with:
    - Python and SQL
    - Machine Learning (TensorFlow, PyTorch, scikit-learn)
    - Data visualization (Matplotlib, Seaborn, Plotly)
    - Jupyter Notebook experience
    - Statistical analysis
    - Big data tools (Spark, Hadoop)
    - Deep learning and NLP
    """
    
    resumes = [
        "Python expert with 5 years ML experience. TensorFlow and PyTorch. "
        "Built neural networks for NLP tasks. Spark and SQL proficient.",
        
        "Data analyst with Excel and Tableau. Basic Python. "
        "SQL databases. No ML experience yet.",
        
        "Recently completed ML bootcamp. Python, scikit-learn, Jupyter. "
        "Worked on classification projects. Learning deep learning."
    ]
    
    matcher = ResumeMatcher()
    report = matcher.get_ranking_report(
        job_desc,
        resumes,
        resume_names=["Candidate A", "Candidate B", "Candidate C"]
    )
    print(report)


def example_2_keyword_extraction():
    """Example 2: Detailed keyword extraction"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Keyword Extraction Analysis")
    print("="*70 + "\n")
    
    extractor = ResumeKeywordExtractor()
    
    job_desc = """
    DevOps Engineer - Cloud Infrastructure
    
    Required:
    - Kubernetes and Docker
    - CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
    - AWS and GCP
    - Infrastructure as Code (Terraform, Ansible)
    - Linux administration
    - Monitoring and logging (Prometheus, ELK Stack)
    - Python scripting
    """
    
    resume = """
    DevOps Specialist with 4 years experience
    - Managed Kubernetes clusters in AWS
    - Set up CI/CD with Jenkins and GitLab
    - Infrastructure automation with Terraform
    - Docker containerization
    - Linux server management
    - Prometheus monitoring
    - Python automation scripts
    """
    
    print("Job Description Keywords:")
    job_keywords = extractor.extract_keywords(job_desc, top_n=20)
    print(f"  {', '.join(job_keywords)}\n")
    
    print("Resume Keywords:")
    resume_keywords = extractor.extract_keywords(resume, top_n=20)
    print(f"  {', '.join(resume_keywords)}\n")
    
    matched = set(job_keywords) & set(resume_keywords)
    print(f"Matched Keywords: {', '.join(matched)}")
    print(f"Match Percentage: {len(matched)/len(job_keywords)*100:.1f}%")


def example_3_batch_processing():
    """Example 3: Processing multiple job postings"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Processing Multiple Positions")
    print("="*70 + "\n")
    
    job_descriptions = {
        "Backend Developer": """
            Python, FastAPI, PostgreSQL, REST APIs,
            Docker, Kubernetes, AWS
        """,
        "Frontend Developer": """
            React, JavaScript, TypeScript, CSS, HTML,
            Vue.js, REST APIs, Git
        """,
        "DevOps Engineer": """
            Docker, Kubernetes, AWS, CI/CD, Jenkins,
            Linux, Python scripting, Terraform
        """
    }
    
    resume = """
    5 years as full-stack developer. Python backend with FastAPI.
    React frontend experience. Docker and Kubernetes.
    PostgreSQL and REST API design. CI/CD with GitHub Actions.
    AWS deployment. Linux administration.
    """
    
    matcher = ResumeMatcher()
    
    print("Candidate resume relevance to different positions:\n")
    for position, job_desc in job_descriptions.items():
        result = matcher.rank_resumes(job_desc, [resume])
        score = result[0]['final_score']
        print(f"  {position:20s}: {score:.1%}")


def example_4_scoring_breakdown():
    """Example 4: Detailed score breakdown"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Scoring Breakdown")
    print("="*70 + "\n")
    
    job_desc = """
    Senior Software Architect
    
    Requirements:
    - 10+ years experience
    - System design and architecture
    - Cloud platforms (AWS, Azure, GCP)
    - Microservices architecture
    - Database design (relational and NoSQL)
    - API design and REST principles
    - Leadership and mentoring
    - Agile methodologies
    """
    
    resumes = [
        "Architect with 12 years experience. AWS expert. Designed microservices "
        "for Fortune 500. Led teams. PostgreSQL and MongoDB. REST APIs.",
        
        "Senior developer with 5 years experience. Some architectural work. "
        "AWS basics. Worked on APIs. Learning microservices.",
        
        "Junior developer with 2 years experience. Full-stack web development. "
        "Node.js and React. Basic databases."
    ]
    
    matcher = ResumeMatcher()
    scores = matcher.calculate_similarity(job_desc, resumes)
    
    print("Detailed Score Breakdown:\n")
    for i, score_data in enumerate(scores, 1):
        print(f"Resume {i}:")
        print(f"  Similarity Score:     {score_data['similarity_score']:>6.1%}")
        print(f"  Keyword Match Score:  {score_data['keyword_match_score']:>6.1%}")
        print(f"  Final Score:          {score_data['final_score']:>6.1%}")
        print()


def example_5_custom_threshold():
    """Example 5: Filtering by threshold"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Threshold-Based Filtering")
    print("="*70 + "\n")
    
    job_desc = """
    Machine Learning Engineer
    
    Must have:
    - TensorFlow and PyTorch
    - Python
    - Deep learning
    - Computer vision or NLP
    - Large dataset experience
    """
    
    resumes = {
        "ML Expert": "10 years ML. Deep learning, computer vision. TensorFlow, PyTorch.",
        "Good Candidate": "4 years ML. Python, scikit-learn, basic deep learning.",
        "Average Candidate": "2 years data analysis. Python, SQL. Learning ML.",
        "Junior": "Recent bootcamp graduate. Python basics. No ML experience."
    }
    
    matcher = ResumeMatcher()
    
    ranked = matcher.rank_resumes(job_desc, list(resumes.values()))
    
    threshold = 0.5
    print(f"Candidates scoring above {threshold:.0%}:\n")
    
    for i, result in enumerate(ranked):
        name = list(resumes.keys())[result['resume_index']]
        score = result['final_score']
        status = "[PASS]" if score >= threshold else "[FAIL]"
        print(f"  {name:20s} {score:.1%}  {status}")


if __name__ == "__main__":
    example_1_basic_ranking()
    example_2_keyword_extraction()
    example_3_batch_processing()
    example_4_scoring_breakdown()
    example_5_custom_threshold()
