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
Resume Screening — TF-IDF + cosine similarity to match resumes to job descriptions.
Run locally with the included `sample_resumes.csv` or try the web UI via `streamlit_app.py`.
Evaluation on 50 labeled pairs: top-1 accuracy 94%, top-3 accuracy 96%.
See `evaluate_topk.py` to reproduce metrics.
## Use it
