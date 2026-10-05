# GenAI-Powered Management Decision Support System

A ready-to-run college project combining:
- Gemini GenAI sentiment analysis for customer feedback (Experiment 7)
- Pandas sales analytics
- OpenCV store-image evidence analysis
- Rule-based management decision support
- FastAPI backend
- React/Vite dashboard

## 1. Backend setup (PowerShell)

Open PowerShell in this project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your own Gemini API key in `.env`:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
USE_GEMINI=true
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env` or expose the key in GitHub/chat.

Start backend:

```powershell
python -m uvicorn app.api:app --reload --port 8000
```

Test: http://127.0.0.1:8000/api/health

## 2. Frontend setup

Open a second PowerShell terminal in the project folder:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## 3. GenAI proof

The dashboard sends customer reviews through `app/sentiment.py` to Gemini when `USE_GEMINI=true`. The response is forced into a structured JSON format containing sentiment, positive aspects, negative aspects, reason, and suggestion.

The dashboard also shows `Gemini reviews: X/10`, which makes the GenAI contribution visible. `/api/analyze-review` can be used to demonstrate one live review without rerunning the full dashboard.

## 4. Image analysis note

The OpenCV module measures image dimensions, brightness, and edge density. It does not claim object detection or semantic recognition.

## 5. Existing images

Place your actual store images in `data/images/store/` (`.jpg`, `.jpeg`, `.png`, `.webp`). The dashboard will display them automatically.
