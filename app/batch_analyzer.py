import json
from pathlib import Path
from app.sentiment import analyze_feedback

CACHE_FILE = Path("data/feedback/analysis_results.json")


def load_reviews(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(file_path)
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def _load_cache():
    if not CACHE_FILE.exists():
        return {}
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return {item["review"]: item for item in data.get("reviews", []) if "review" in item}
    except Exception:
        return {}


def analyze_reviews_batch(reviews):
    cache = _load_cache()
    results = []
    for i, review in enumerate(reviews, 1):
        cached = cache.get(review)
        if cached and cached.get("source") == "gemini":
            result = dict(cached)
        else:
            result = analyze_feedback(review)
        result.update({"review_id": i, "review": review})
        results.append(result)
    output = {"reviews": results}
    save_results(output, CACHE_FILE)
    return output


def save_results(results, output_file):
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=4, ensure_ascii=False), encoding="utf-8")
