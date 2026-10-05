import os
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.main import run_pipeline
from app.sentiment import analyze_feedback

load_dotenv()
app=FastAPI(title="GenAI Management Decision Support System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://genai-management-decision-system.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FEEDBACK_DIR=Path("data/feedback"); SALES_DIR=Path("data/sales"); IMAGE_DIR=Path("data/images/store")
for d in [FEEDBACK_DIR,SALES_DIR,IMAGE_DIR]: d.mkdir(parents=True,exist_ok=True)
app.mount("/images",StaticFiles(directory=str(IMAGE_DIR)),name="store-images")

@app.get("/api/health")
def health():
    key=bool(os.getenv("GEMINI_API_KEY","" ).strip())
    return {"status":"ok","gemini_enabled":os.getenv("USE_GEMINI","true").lower()=="true" and key,"model":os.getenv("GEMINI_MODEL","gemini-3.8-flash")}

@app.get("/api/dashboard")
def dashboard(): return run_pipeline()

@app.post("/api/analyze-review")
def analyze_review(payload: dict):
    review=str(payload.get("review","")).strip()
    if not review: return {"status":"error","message":"review is required"}
    return analyze_feedback(review)

@app.post("/api/upload")
async def upload_file(file: UploadFile=File(...)):
    filename=Path(file.filename or "").name; ext=Path(filename).suffix.lower()
    if ext==".txt": destination=FEEDBACK_DIR/"reviews.txt"
    elif ext==".csv": destination=SALES_DIR/"sales_data.csv"
    elif ext in {".jpg",".jpeg",".png",".webp"}: destination=IMAGE_DIR/filename
    else: return {"status":"error","message":f"Unsupported file type: {ext}"}
    destination.write_bytes(await file.read())
    return {"status":"success","filename":filename,"saved_to":str(destination)}
