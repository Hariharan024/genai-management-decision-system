from pathlib import Path


def generate_markdown(feedback, sales, images, decision):
    path=Path("outputs/reports/management_report.md")
    path.parent.mkdir(parents=True,exist_ok=True)
    lines=["# GenAI-Powered Management Decision Support System","","## Executive Summary",decision["executive_summary"],"","## Customer Feedback Analysis",f"Total reviews: {feedback.get('total_reviews',0)}",""]
    for k,v in feedback.get("sentiment_counts",{}).items(): lines.append(f"- {k}: {v} ({feedback.get('sentiment_percentages',{}).get(k,0)}%)")
    lines += ["",f"GenAI-analyzed reviews: {feedback.get('genai_reviews',0)}","","## Sales Analysis",f"Total revenue: ₹{sales.get('total_revenue',0)}",f"Total units: {sales.get('total_units',0)}","","## Store Image Analysis",f"Images analyzed: {images.get('image_count',0)}","","## Management Actions"]
    lines += [f"- {a}" for a in decision.get("actions",[])]
    lines += ["","## Analysis Note","Gemini is used for customer-feedback sentiment analysis when USE_GEMINI=true and a valid GEMINI_API_KEY is configured. Sales and store-image metrics use deterministic analytical methods."]
    path.write_text("\n".join(lines),encoding="utf-8")
    return str(path)
