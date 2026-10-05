def build_decision(feedback_summary, sales_summary, image_summary):
    actions=[]
    counts=feedback_summary.get("sentiment_counts",{})
    negative_count=counts.get("Negative",0); mixed_count=counts.get("Mixed",0)
    negative_aspects=feedback_summary.get("common_negative_aspects",[])
    if negative_count or mixed_count:
        actions.append("Investigate recurring negative or mixed customer experiences.")
    if negative_aspects:
        actions.append(f"Investigate recurring customer issue: {negative_aspects[0]['aspect']}.")
    top=sales_summary.get("top_products",[])
    if top:
        actions.append(f"Monitor sales performance of {top[0]['Product']} ({top[0]['Revenue']} revenue).")
    images=image_summary.get("images",[])
    moderately=[x for x in images if x.get("brightness_status")=="Moderately lit"]
    if moderately:
        actions.append(f"Review lighting conditions in {len(moderately)} store image(s).")
    if not images:
        actions.append("Collect store images before making visual-condition decisions.")
    return {"executive_summary":"Management insights were generated from customer feedback, sales data, and store-image evidence.","actions":actions,"evidence":{"sentiment":counts,"sales_total_revenue":sales_summary.get("total_revenue",0),"store_images":len(images)}}
