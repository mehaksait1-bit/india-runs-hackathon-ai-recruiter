import pandas as pd
from ranker import load_candidates
from scorer import calculate_score

print("Loading Job Description...")

with open(
    "data/job_description.txt",
    "r",
    encoding="utf-8"
) as f:
    job_description = f.read().lower()

print("Loading candidates...")

candidates = load_candidates(
    "data/candidates.jsonl"
)

print(f"Loaded {len(candidates)} candidates")

jd_keywords = [
    "retrieval",
    "ranking",
    "embeddings",
    "vector",
    "pinecone",
    "qdrant",
    "milvus",
    "weaviate",
    "faiss",
    "opensearch",
    "elasticsearch",
    "sentence transformers",
    "recommendation",
    "information retrieval",
    "llm",
    "lora",
    "qlora",
    "rag",
    "mlops",
    "python"
]

results = []

for candidate in candidates:

    score = calculate_score(candidate)

    candidate_id = candidate.get(
        "candidate_id",
        "unknown"
    )

    profile = candidate.get(
        "profile",
        {}
    )

    candidate_text = (
        profile.get("headline", "")
        + " "
        + profile.get("summary", "")
    ).lower()

    skills = []

    for skill in candidate.get(
        "skills",
        []
    ):
        skills.append(
            skill.get("name", "")
        )

        if skill.get(
            "name",
            ""
        ).lower() in jd_keywords:
            score += 10

    career_history = candidate.get(
        "career_history",
        []
    )

    for job in career_history:

        description = job.get(
            "description",
            ""
        ).lower()

        if (
            "recommendation" in description
            or "ranking" in description
            or "retrieval" in description
            or "search" in description
        ):
            score += 20

    experience = profile.get(
        "years_of_experience",
        0
    )

    if 5 <= experience <= 9:
        score += 20

    top_skills = ", ".join(
        skills[:5]
    )

    reasoning = (
        f"{experience} years experience, "
        f"Current Role: "
        f"{profile.get('current_title','N/A')}, "
        f"Top Skills: {top_skills}"
    )

    results.append({
        "candidate_id": candidate_id,
        "score": round(score, 2),
        "top_skills": top_skills,
        "reasoning": reasoning
    })

print("Ranking candidates...")

results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

for i, row in enumerate(results):
    row["rank"] = i + 1

results = results[:100]

df = pd.DataFrame(results)

df.to_csv(
    "submission.csv",
    index=False
)

print("\nSubmission Created Successfully\n")
print(df.head(10))