import json
import os
import re
from dotenv import load_dotenv
from app.prompts import SENTIMENT_PROMPT

load_dotenv()

VALID_SENTIMENTS = {"Positive", "Negative", "Neutral", "Mixed"}


def create_prompt(feedback: str) -> str:
    return SENTIMENT_PROMPT.format(feedback=feedback)


def local_analyze_feedback(feedback: str) -> dict:
    text = feedback.lower()
    positive_words = ["excellent","great","good","friendly","pleasant","clean","organized","helped","liked","reasonable","delicious","definitely","again","service"]
    negative_words = ["poor","cold","slow","long","wait","waiting","crowded","difficult","unavailable","rude","queue"]
    pos = sum(w in text for w in positive_words)
    neg = sum(w in text for w in negative_words)
    if pos and neg: sentiment = "Mixed"
    elif pos: sentiment = "Positive"
    elif neg: sentiment = "Negative"
    else: sentiment = "Neutral"
    positives=[]; negatives=[]
    mappings_pos={"food":"Food quality","friendly":"Friendly staff","staff":"Helpful staff","clean":"Clean store","organized":"Well organized store","service":"Good service","reasonable":"Reasonable prices"}
    mappings_neg={"wait":"Long waiting time","slow":"Slow process","crowded":"Crowded store","unavailable":"Products unavailable","cold":"Food/order served cold","queue":"Long checkout queue","poor":"Poor quality"}
    for k,v in mappings_pos.items():
        if k in text and v not in positives: positives.append(v)
    for k,v in mappings_neg.items():
        if k in text and v not in negatives: negatives.append(v)
    suggestion = "Reduce waiting time and improve the affected store process." if negatives else ("Maintain the current positive customer experience." if positives else "Collect more specific customer feedback.")
    reason = f"The review contains {pos} positive signal(s) and {neg} negative signal(s)."
    return {"sentiment":sentiment,"positive_aspects":positives,"negative_aspects":negatives,"reason":reason,"suggestion":suggestion,"source":"local_fallback"}


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"\{.*\}", cleaned, flags=re.S)
    if not match:
        raise ValueError("Gemini did not return JSON")
    data = json.loads(match.group(0))
    if data.get("sentiment") not in VALID_SENTIMENTS:
        raise ValueError("Invalid sentiment returned by Gemini")
    for key in ("positive_aspects", "negative_aspects"):
        if not isinstance(data.get(key), list):
            data[key] = []
    data["reason"] = str(data.get("reason", ""))
    data["suggestion"] = str(data.get("suggestion", ""))
    return data


def analyze_with_gemini(feedback: str) -> dict:
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=create_prompt(feedback),
    )
    result = _extract_json(response.text or "")
    result["source"] = "gemini"
    result["model"] = model
    return result


def analyze_feedback(feedback: str) -> dict:
    use_gemini = os.getenv("USE_GEMINI", "true").lower() == "true"
    if not use_gemini:
        return local_analyze_feedback(feedback)
    try:
        return analyze_with_gemini(feedback)
    except Exception as exc:
        result = local_analyze_feedback(feedback)
        result["gemini_error"] = str(exc)
        return result
