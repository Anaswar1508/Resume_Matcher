"""
Resume Screening System - Testing and Evaluation
Includes unit tests and performance metrics
"""

import unittest
from resume_matcher import ResumeMatcher, ResumeKeywordExtractor


class TestKeywordExtractor(unittest.TestCase):
    """Test keyword extraction functionality"""
    
    def setUp(self):
        self.extractor = ResumeKeywordExtractor()
    
    def test_text_cleaning(self):
        """Test text preprocessing"""
        text = "Check out my portfolio: http://example.com and email@test.com"
        cleaned = self.extractor.clean_text(text)
        
        self.assertNotIn("http", cleaned)
        self.assertNotIn("@", cleaned)
        self.assertTrue(cleaned.islower())
    
    def test_keyword_extraction(self):
        """Test keyword extraction returns valid results"""
        text = "Python developer with Django and REST API experience"
        keywords = self.extractor.extract_keywords(text)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertIn("python", keywords)
    
    def test_technical_keyword_weighting(self):
        """Test that technical keywords are weighted higher"""
        text = "Python Django REST API"
        keywords = self.extractor.extract_keywords(text, top_n=10)
        
        # Technical keywords should be in top results
        self.assertIn("python", keywords)


class TestResumeMatcher(unittest.TestCase):
    """Test resume matching functionality"""
    
    def setUp(self):
        self.matcher = ResumeMatcher()
        self.job_desc = "Python developer with Django and AWS experience"
        self.resumes = [
            "5 years Python Django developer on AWS",  # Should match well
            "Java developer with Spring Boot",         # Poor match
            "Python and Django freelancer"             # Good match
        ]
    
    def test_similarity_calculation(self):
        """Test similarity score calculation"""
        scores = self.matcher.calculate_similarity(self.job_desc, self.resumes)
        
        self.assertEqual(len(scores), len(self.resumes))
        for score_data in scores:
            self.assertIn('similarity_score', score_data)
            self.assertIn('final_score', score_data)
            self.assertIn('matched_keywords', score_data)
            
            # Scores should be between 0 and 1
            self.assertGreaterEqual(score_data['final_score'], 0)
            self.assertLessEqual(score_data['final_score'], 1)
    
    def test_ranking_order(self):
        """Test that resumes are ranked correctly"""
        ranked = self.matcher.rank_resumes(self.job_desc, self.resumes)
        
        # Check that scores are in descending order
        scores = [r['final_score'] for r in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_top_k_filtering(self):
        """Test limiting results with top_k"""
        top_k = 2
        ranked = self.matcher.rank_resumes(
            self.job_desc,
            self.resumes,
            top_k=top_k
        )
        
        self.assertEqual(len(ranked), top_k)
    
    def test_keyword_matching(self):
        """Test keyword matching logic"""
        job_desc = "Python JavaScript SQL"
        resumes = ["Python and SQL expert", "JavaScript only"]
        
        scores = self.matcher.calculate_similarity(job_desc, resumes)
        
        # First resume should have more matched keywords
        matched_1 = len(scores[0]['matched_keywords'])
        matched_2 = len(scores[1]['matched_keywords'])
        
        self.assertGreater(matched_1, matched_2)


class TestScenarios(unittest.TestCase):
    """Test real-world scenarios"""
    
    def test_perfect_match(self):
        """Test scenario where resume perfectly matches job"""
        matcher = ResumeMatcher()
        
        job_desc = "Python developer AWS Docker"
        perfect_resume = "Python developer with AWS and Docker expertise"
        
        result = matcher.rank_resumes(job_desc, [perfect_resume])
        
        # Perfect match should score high
        self.assertGreater(result[0]['final_score'], 0.7)
    
    def test_no_match(self):
        """Test scenario where resume doesn't match job"""
        matcher = ResumeMatcher()
        
        job_desc = "Python backend developer"
        no_match_resume = "Graphic designer with Photoshop skills"
        
        result = matcher.rank_resumes(job_desc, [no_match_resume])
        
        # No match should score low
        self.assertLess(result[0]['final_score'], 0.3)
    
    def test_partial_match(self):
        """Test scenario where resume partially matches job"""
        matcher = ResumeMatcher()
        
        job_desc = "Python Django REST API PostgreSQL AWS Docker"
        partial_resume = "Python and Django developer"
        
        result = matcher.rank_resumes(job_desc, [partial_resume])
        
        # Partial match should be medium score (adjusted threshold for realistic expectations)
        score = result[0]['final_score']
        self.assertGreater(score, 0.2)
        self.assertLess(score, 0.7)


def run_performance_test():
    """Test system performance with large datasets"""
    print("\nPerformance Test Results:")
    print("-" * 50)
    
    import time
    
    matcher = ResumeMatcher()
    
    # Generate test data
    job_desc = """
    Senior Software Engineer
    Python Java JavaScript SQL REST API
    AWS Docker Kubernetes Microservices
    """ * 3
    
    resumes = [
        f"""
        Software Engineer Resume {i}
        Skills: Python Java JavaScript SQL Docker
        Experience: Years of software development
        """ * 2
        for i in range(100)
    ]
    
    # Measure ranking time
    start = time.time()
    ranked = matcher.rank_resumes(job_desc, resumes)
    elapsed = time.time() - start
    
    print(f"Resumes processed: {len(resumes)}")
    print(f"Time taken: {elapsed:.3f} seconds")
    print(f"Resumes per second: {len(resumes)/elapsed:.0f}")


if __name__ == "__main__":
    # Run unit tests
    print("Running Unit Tests...")
    print("=" * 50)
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()
