import re

KNOWN_SKILLS = [
    "python", "django", "flask", "fastapi", "java", "spring", "php", "laravel",
    "javascript", "typescript", "node", "react", "html", "css",
    "sql", "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "rest", "api", "graphql", "git", "github", "docker", "kubernetes",
    "aws", "azure", "linux", "ci/cd", "testing", "celery", "agile",
]


def has_skill(text, skill):
    pattern = rf"(?<![a-z0-9]){re.escape(skill)}s?(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def analyze_match(job_description, my_skills):
    required = [s for s in KNOWN_SKILLS if has_skill(job_description, s)]
    matched = [s for s in required if has_skill(my_skills, s)]
    missing = [s for s in required if s not in matched]
    score = round(100 * len(matched) / len(required)) if required else 0
    result = {
        "mode": "keyword",
        "score": score,
        "required_skills": required,
        "matched": matched,
        "missing": missing,
    }
    if not required:
        result["note"] = "No known skills were found in this job description."
    return result