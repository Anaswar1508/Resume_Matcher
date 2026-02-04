import csv
from typing import List
import streamlit as st
import pandas as pd

from resume_matcher import ResumeMatcher


@st.cache_data
def load_resumes(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_texts(df: pd.DataFrame) -> List[str]:
    texts = []
    for _, row in df.iterrows():
        parts = [str(row.get('title', '')), str(row.get('summary', '')), str(row.get('skills', '')), str(row.get('education', ''))]
        texts.append(' '.join([p for p in parts if p and p != 'nan']))
    return texts


def main():
    st.set_page_config(page_title="Resume Matcher", layout="wide")
    st.title("Resume — Job Description Matcher")

    st.sidebar.header("Data")
    use_sample = st.sidebar.checkbox("Use sample_resumes.csv", value=True)
    uploaded = st.sidebar.file_uploader("Or upload resumes CSV", type=["csv"] )

    if use_sample or not uploaded:
        df = load_resumes("sample_resumes.csv")
    else:
        df = pd.read_csv(uploaded)

    st.sidebar.markdown(f"Resumes loaded: **{len(df)}**")

    st.sidebar.header("Matching Settings")
    top_k = st.sidebar.slider("Top K results", min_value=1, max_value=20, value=10)

    st.header("Job Description")
    job_desc = st.text_area("Enter the job description to match against resumes:", height=200)

    if st.button("Run Matching"):
        if not job_desc.strip():
            st.error("Please provide a job description.")
            return

        with st.spinner("Computing matches..."):
            matcher = ResumeMatcher()
            resumes_texts = build_texts(df)
            ranked = matcher.rank_resumes(job_desc, resumes_texts, top_k=top_k)

        # map results to dataframe for display
        rows = []
        for r in ranked:
            idx = r['resume_index']
            name = df.iloc[idx].get('name', f"Resume {idx+1}") if 'name' in df.columns else f"Resume {idx+1}"
            rows.append({
                'rank': len(rows) + 1,
                'resume_id': idx + 1,
                'name': name,
                'final_score': r['final_score'],
                'similarity_score': r['similarity_score'],
                'keyword_match_score': r['keyword_match_score'],
                'matched_keywords': ', '.join(r.get('matched_keywords', [])[:10])
            })

        result_df = pd.DataFrame(rows)
        result_df_display = result_df.copy()
        # show percentages
        for col in ['final_score', 'similarity_score', 'keyword_match_score']:
            result_df_display[col] = (result_df_display[col] * 100).map(lambda x: f"{x:.2f}%")

        st.subheader(f"Top {top_k} Matches")
        st.table(result_df_display)

        csv = result_df.to_csv(index=False)
        st.download_button("Download results CSV", csv, file_name="matching_results.csv", mime='text/csv')

    st.sidebar.markdown("---")
    st.sidebar.markdown("Built with TF-IDF + cosine similarity. Uses `resume_matcher.py` for scoring.")


if __name__ == '__main__':
    main()
