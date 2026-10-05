from collections import Counter


def aggregate_results(batch_results):
    reviews = batch_results.get("reviews", [])
    sentiment_counts = Counter(r.get("sentiment", "Neutral") for r in reviews)
    total = len(reviews)
    sentiment_percentages = {k: round((sentiment_counts.get(k, 0) / total) * 100, 1) if total else 0.0 for k in ["Positive", "Negative", "Neutral", "Mixed"]}
    pos = Counter(); neg = Counter()
    for r in reviews:
        pos.update(r.get("positive_aspects", []))
        neg.update(r.get("negative_aspects", []))
    return {
        "total_reviews": total,
        "sentiment_counts": {k: sentiment_counts.get(k, 0) for k in ["Positive", "Negative", "Neutral", "Mixed"]},
        "sentiment_percentages": sentiment_percentages,
        "common_positive_aspects": [{"aspect": k, "count": v} for k,v in pos.most_common(10)],
        "common_negative_aspects": [{"aspect": k, "count": v} for k,v in neg.most_common(10)],
        "reviews": reviews,
        "genai_reviews": sum(1 for r in reviews if r.get("source") == "gemini"),
    }
