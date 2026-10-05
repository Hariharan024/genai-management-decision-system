import json
from app.batch_analyzer import load_reviews, analyze_reviews_batch
from app.aggregation import aggregate_results
from app.sales_analysis import analyze_sales
from app.image_analysis import analyze_store_images
from app.decision_engine import build_decision
from app.report_generator import generate_markdown


def run_pipeline():
    reviews = load_reviews("data/feedback/reviews.txt")
    feedback = analyze_reviews_batch(reviews)
    aggregation = aggregate_results(feedback)
    sales = analyze_sales("data/sales/sales_data.csv")
    images = analyze_store_images("data/images/store")
    decision = build_decision(aggregation, sales, images)
    report = generate_markdown(aggregation, sales, images, decision)
    Path = __import__('pathlib').Path
    Path("outputs/reports").mkdir(parents=True, exist_ok=True)
    Path("outputs/reports/full_summary.json").write_text(json.dumps({"feedback":aggregation,"sales":sales,"images":images,"decision":decision}, indent=4, ensure_ascii=False), encoding="utf-8")
    return {"feedback":aggregation,"sales":sales,"images":images,"decision":decision,"report":report}

if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2, ensure_ascii=False))
