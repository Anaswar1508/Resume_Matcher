"""
Resume Screening System
Matches resumes to jobs using NLP stuff
"""

import re
import string
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# grab NLTK stuff - needed for tokenization
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

# stopwords too
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class ResumeKeywordExtractor:
    """Gets keywords from text"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # keywords that matter more - like programming stuff
        self.technical_keywords = {
            'python', 'javascript', 'java', 'sql', 'react', 'node.js', 'aws',
            'docker', 'kubernetes', 'machine learning', 'ai', 'data science',
            'tensorflow', 'pytorch', 'nlp', 'deep learning', 'api', 'rest',
            'microservices', 'agile', 'scrum', 'git', 'ci/cd', 'devops'
        }
    
    def clean_text(self, text: str) -> str:
        """normalize text - lowercase it, remove junk"""
        text = text.lower()
        text = re.sub(r'http\S+|www.\S+', '', text)  # urls
        text = re.sub(r'\S+@\S+', '', text)  # emails
        text = re.sub(r'[^a-z0-9\s\-./]', '', text)  # special chars
        return text
    
    def extract_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """get the important words"""
        cleaned_text = self.clean_text(text)
        tokens = word_tokenize(cleaned_text)
        
        # filter out junk - stopwords and single chars
        keywords = [
            token for token in tokens
            if token not in self.stop_words 
            and len(token) > 2
            and not token.isdigit()
        ]
        
        # score them - technical stuff counts more
        keyword_scores = {}
        for keyword in keywords:
            weight = 2.0 if keyword in self.technical_keywords else 1.0
            keyword_scores[keyword] = keyword_scores.get(keyword, 0) + weight
        
        # sort and get top N
        top_keywords = sorted(
            keyword_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        return [kw[0] for kw in top_keywords]


class ResumeMatcher:
    """Matches resumes to jobs"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.keyword_extractor = ResumeKeywordExtractor()
    
    def preprocess_text(self, text: str) -> str:
        """clean up text before matching"""
        return self.keyword_extractor.clean_text(text)
    
    def calculate_similarity(self, job_desc: str, resumes: List[str]) -> List[Dict]:
        """figure out how much each resume matches the job"""
        # clean everything
        processed_job = self.preprocess_text(job_desc)
        processed_resumes = [self.preprocess_text(resume) for resume in resumes]
        
        # get job keywords
        job_keywords = set(self.keyword_extractor.extract_keywords(job_desc))
        
        # vectorize
        all_texts = [processed_job] + processed_resumes
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # calc similarity
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        results = []
        for idx, resume in enumerate(processed_resumes):
            resume_keywords = set(
                self.keyword_extractor.extract_keywords(resume)
            )
            
            # how many keywords match
            matched_keywords = job_keywords & resume_keywords
            keyword_match_score = len(matched_keywords) / max(len(job_keywords), 1)
            
            similarity_score = similarities[0][idx]
            keyword_score = keyword_match_score
            
            # 70/30 split - similarity is more important
            final_score = (similarity_score * 0.7) + (keyword_score * 0.3)
            
            results.append({
                'resume_index': idx,
                'similarity_score': float(similarity_score),
                'keyword_match_score': float(keyword_score),
                'final_score': float(final_score),
                'matched_keywords': list(matched_keywords)
            })
        
        return results
    
    def rank_resumes(
        self,
        job_desc: str,
        resumes: List[str],
        top_k: int = None
    ) -> List[Dict]:
        """rank resumes by relevance"""
        scores = self.calculate_similarity(job_desc, resumes)
        ranked = sorted(scores, key=lambda x: x['final_score'], reverse=True)
        
        if top_k:
            ranked = ranked[:top_k]
        
        return ranked
    
    def get_ranking_report(
        self,
        job_desc: str,
        resumes: List[str],
        resume_names: List[str] = None,
        top_k: int = None
    ) -> str:
        """format the results"""
        if not resume_names:
            resume_names = [f"Resume {i+1}" for i in range(len(resumes))]
        
        ranked = self.rank_resumes(job_desc, resumes, top_k)
        
        report = "=" * 70 + "\n"
        report += "RESUME RANKING REPORT\n"
        report += "=" * 70 + "\n\n"
        
        for rank, result in enumerate(ranked, 1):
            idx = result['resume_index']
            report += f"Rank #{rank}: {resume_names[idx]}\n"
            report += f"  Final Score:        {result['final_score']:.2%}\n"
            report += f"  Similarity Score:   {result['similarity_score']:.2%}\n"
            report += f"  Keyword Match:      {result['keyword_match_score']:.2%}\n"
            report += f"  Matched Keywords:   {', '.join(result['matched_keywords'][:10])}\n"
            report += "-" * 70 + "\n"
        
        return report


def main():
    """run test"""
    job_description = """
    Senior Python Developer
    
    Looking for Python dev with backend experience.
    - 5+ years Python
    - Django or FastAPI
    - SQL and NoSQL (PostgreSQL, MongoDB)
    - REST APIs
    - Docker and Kubernetes  
    - AWS
    - ML basics
    - Git and CI/CD
    - Agile/Scrum
    """
    
    resumes = [
        """
        John Doe
        Senior Software Engineer
        
        Experience:
        - 6 years Python developer
        - Built REST APIs with Django and FastAPI
        - PostgreSQL and MongoDB databases
        - Docker and Kubernetes orchestration
        - AWS deployment
        - CI/CD pipelines
        - Agile team environment
        - ML model implementation
        """,
        
        """
        Jane Smith
        Full Stack Developer
        
        Experience:
        - 4 years JavaScript/React
        - 2 years Python
        - SQL databases
        - REST API integration
        - Git version control
        - Startup experience
        - Docker basics
        """,
        
        """
        Bob Johnson
        Junior Frontend Developer
        
        Skills:
        - HTML, CSS, JavaScript
        - React and Vue.js
        - CSS frameworks
        - Git basics
        - Learning Python
        """
    ]
    
    matcher = ResumeMatcher()
    
    report = matcher.get_ranking_report(
        job_description,
        resumes,
        resume_names=["John Doe", "Jane Smith", "Bob Johnson"],
        top_k=3
    )
    
    print(report)
    
    print("\n" + "=" * 70)
    print("KEYWORD ANALYSIS")
    print("=" * 70 + "\n")
    
    extractor = ResumeKeywordExtractor()
    print("Job Keywords:")
    job_keywords = extractor.extract_keywords(job_description)
    print(f"  {', '.join(job_keywords)}\n")
    
    for i, resume in enumerate(resumes, 1):
        print(f"Resume {i} Keywords:")
        resume_keywords = extractor.extract_keywords(resume)
        print(f"  {', '.join(resume_keywords)}\n")


if __name__ == "__main__":
    main()
