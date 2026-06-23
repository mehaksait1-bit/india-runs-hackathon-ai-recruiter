def calculate_score(candidate):

    score = 0

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    skills_data = candidate.get("skills", [])

    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 10:
        score += 20
    elif exp > 10:
        score += 15
    else:
        score += 5

    skills = [s.get("name", "").lower() for s in skills_data]

    important_skills = [
        "nlp",
        "fine-tuning llms",
        "lora",
        "milvus",
        "bentoml",
        "rag",
        "python",
        "mlops",
        "machine learning",
        "deep learning"
    ]

    for skill in important_skills:
        if skill in skills:
            score += 10

    total_endorsements = sum(
        skill.get("endorsements", 0)
        for skill in skills_data
    )

    score += min(total_endorsements / 20, 20)

    score += signals.get(
        "profile_completeness_score", 0
    ) / 10

    score += signals.get(
        "recruiter_response_rate", 0
    ) * 20

    score += signals.get(
        "interview_completion_rate", 0
    ) * 20

    score += signals.get(
        "offer_acceptance_rate", 0
    ) * 20

    score += signals.get(
        "github_activity_score", 0
    )

    score += (
        signals.get(
            "saved_by_recruiters_30d", 0
        ) * 2
    )

    score += (
        signals.get(
            "search_appearance_30d", 0
        ) / 100
    )

    if signals.get("open_to_work_flag", False):
        score += 10

    if signals.get("willing_to_relocate", False):
        score += 5

    return round(score, 2)