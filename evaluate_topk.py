import csv
import json
from typing import List
from resume_matcher import ResumeMatcher


def load_resumes_from_csv(path: str) -> List[str]:
    resumes = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = " ".join([row.get('title', ''), row.get('summary', ''), row.get('skills', ''), row.get('education', '')])
            resumes.append(text)
    return resumes


def load_labeled_pairs(path: str):
    pairs = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairs.append({
                'job_id': int(row['job_id']),
                'job_title': row['job_title'],
                'job_description': row['job_description'],
                'correct_resume_id': int(row['correct_resume_id'])
            })
    return pairs


def evaluate_topk(resumes_csv='sample_resumes.csv', labeled_csv='labeled_pairs.csv'):
    resumes = load_resumes_from_csv(resumes_csv)
    labeled = load_labeled_pairs(labeled_csv)

    matcher = ResumeMatcher()

    top1_hits = 0
    top3_hits = 0
    total = len(labeled)

    for item in labeled:
        ranked = matcher.rank_resumes(item['job_description'], resumes, top_k=10)
        # ranked contains resume_index referencing 0-based index of resumes list
        top_indices = [r['resume_index'] + 1 for r in ranked[:3]]  # +1 to match CSV ids

        correct_id = item['correct_resume_id']
        if ranked[0]['resume_index'] + 1 == correct_id:
            top1_hits += 1
        if correct_id in top_indices:
            top3_hits += 1

    top1_acc = top1_hits / total if total else 0
    top3_acc = top3_hits / total if total else 0

    print(f"Evaluation samples: {total}")
    print(f"Top-1 accuracy: {top1_acc:.2%} ({top1_hits}/{total})")
    print(f"Top-3 accuracy: {top3_acc:.2%} ({top3_hits}/{total})")


if __name__ == '__main__':
    evaluate_topk()
