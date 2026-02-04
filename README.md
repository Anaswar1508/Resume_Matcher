# Resume Screening System

Quick way to match resumes to job postings. Uses some NLP stuff to figure out which resumes are actually relevant.

## What it does

Takes a job description, throws a bunch of resumes at it, and tells you which ones are worth looking at. Scores them based on keywords and text similarity.

## How it works

**3 main parts:**

1. **Keyword extraction** - pulls out important words from the job and resumes
2. **Similarity matching** - uses TF-IDF to find how similar resume text is to job description
3. **Ranking** - combines the scores and sorts by best match first

## Install

```bash
pip install -r requirements.txt
```

Need: scikit-learn, nltk, numpy

## Use it

### Basic example

```python
from resume_matcher import ResumeMatcher

matcher = ResumeMatcher()

job = "Senior Python developer with AWS experience"

resumes = [
    "5 years Python, built APIs, deployed on AWS",
    "Junior JavaScript developer", 
    "DevOps engineer with Kubernetes"
]

# get rankings
ranked = matcher.rank_resumes(job, resumes)

for result in ranked:
    print(f"Score: {result['final_score']:.1%}")
    print(f"Keywords: {result['matched_keywords']}\n")
```

### Get a formatted report

```python
report = matcher.get_ranking_report(
    job,
    resumes,
    resume_names=["Alice", "Bob", "Charlie"]
)
print(report)
```

## Files

- **resume_matcher.py**: Core system (ResumeMatcher, ResumeKeywordExtractor)
- **advanced_examples.py**: 5 detailed usage examples
- **test_resume_system.py**: Unit tests and performance benchmarks
- **requirements.txt**: Python dependencies
- **README.md**: This file

## Scoring Formula

$$\text{Final Score} = (0.7 \times \text{Similarity Score}) + (0.3 \times \text{Keyword Match Score})$$

Where:
- **Similarity Score**: Cosine similarity of TF-IDF vectors
- **Keyword Match Score**: $\frac{\text{Matched Keywords}}{\text{Job Keywords}}$

## Running Examples

### Example 1: Basic Ranking
```bash
python advanced_examples.py
```

Output shows 5 different examples:
1. Basic resume ranking
2. Detailed keyword extraction
3. Batch processing multiple positions
4. Scoring breakdown analysis
5. Threshold-based filtering

### Example 2: Run Tests
```bash
python test_resume_system.py
```

Tests include:
- Keyword extraction validation
- Similarity calculations
- Ranking order verification
- Real-world scenarios
- Performance metrics

## Algorithm Details

### Keyword Extraction
1. **Text Cleaning**: Remove URLs, emails, special characters
2. **Tokenization**: Break text into words using NLTK
3. **Filtering**: Remove stopwords, single characters, numbers
4. **Scoring**: Weight technical keywords higher
5. **Ranking**: Sort by frequency and weight

### Similarity Calculation
1. **Vectorization**: Convert text to TF-IDF vectors
2. **Cosine Similarity**: Calculate angle between vectors
3. **Keyword Matching**: Find overlap in extracted keywords
4. **Score Combination**: Weighted average of metrics

### Ranking
1. Calculate all metrics for each resume
2. Compute final score (70% similarity + 30% keywords)
3. Sort by final score (descending)
4. Filter top K results if specified

## Customization

### Adjust Scoring Weights
Modify in `ResumeMatcher.calculate_similarity()`:
```python
final_score = (similarity_score * 0.6) + (keyword_score * 0.4)  # 60/40 split
```

### Add Technical Keywords
Modify `ResumeKeywordExtractor.__init__()`:
```python
self.technical_keywords.add('new_keyword')
```

### Change N-gram Range
Modify in `ResumeMatcher.__init__()`:
```python
ngram_range=(1, 3)  # Include trigrams
```

## Performance

- **100 resumes**: ~0.5 seconds
- **Scales linearly** with resume count
- **Memory efficient**: Processes text in batches

## Metrics

| Metric | Description |
|--------|-------------|
| Similarity Score | TF-IDF cosine similarity (0-100%) |
| Keyword Match Score | % of job keywords found in resume |
| Final Score | Weighted combination of above |
| Matched Keywords | List of skill overlap between job and resume |

## Use Cases

1. **Applicant Tracking**: Automatically rank job applicants
2. **Skill Gap Analysis**: Identify missing skills
3. **Job Matching**: Match candidates to positions
4. **Resume Screening**: Filter qualified candidates
5. **Career Planning**: Find relevant jobs for skills

## Limitations

- Requires sufficient text length for accuracy
- May miss domain-specific terminology
- Doesn't account for experience level/years
- Binary keyword matching (doesn't check proficiency)
- No consideration of education requirements

## Future Enhancements

- Weight scores by keyword importance
- Include GPA, certifications, years of experience
- Support for PDF resume parsing
- Deep learning models (BERT, RoBERTa)
- Multi-language support
- Resume parsing with structured extraction
- Fuzzy matching for misspelled keywords

## License

Open source for educational purposes

## Author

AI Resume Screening System
