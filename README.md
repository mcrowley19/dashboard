# Metricare

Medical patient dashboard: patient history, medications, drug interactions (FDA), and AI-generated summaries in one place. Replaces scattered legacy systems with a single Metricare UI and API.

---

## Repo structure

| Path | Purpose |
|------|--------|
| **`frontend/`** | React + Vite app. **Node/npm only** — run `npm install` and `npm run dev` here (not at root). |
| **`backend/`** | FastAPI (Python). **Python only** — no Node; use a venv and `pip install -r requirements.txt` here. |
| **`api/`** | Vercel serverless entry (wraps backend for serverless deploy). No local install. |
| **Root** | `vercel.json`, `requirements.txt` (for Vercel), and convenience scripts. **Do not run `npm install` at root** — only in `frontend/`. |

---

## Prerequisites

- **Node.js** (v18+) and **npm** — for the frontend.
- **Python 3.9+** — for the backend. On some systems the command is `python3` instead of `python`.

---

## 1. Backend setup and run

### 1.1 Create a virtual environment and install dependencies

**Always run these from the `backend/` directory:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 1.2 Configure environment variables

The backend reads `backend/.env`. Copy the example and add your keys:

```bash
cp .env.example .env
```

Edit `backend/.env`:

```env
# Required for POST /patient/summary (AI summaries)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: use a different Gemini model (default is gemini-2.5-flash)
# GEMINI_MODEL=gemini-2.5-flash

# Optional: FDA API key (OpenFDA provides a demo key by default)
# FDA_API_KEY=your_fda_key_here
```

Get a Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey). Use a key that matches the model (e.g. 2.5 Flash for `gemini-2.5-flash`).

### 1.3 Start the backend

From the **backend** directory (with `.venv` activated):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or from the **project root** (backend must be set up first):

```bash
npm run dev
```
(or `npm run dev:backend`)

- **API base URL:** http://localhost:8000  
- **Swagger UI (interactive docs):** http://localhost:8000/docs  
- **OpenAPI JSON:** http://localhost:8000/openapi.json  

If port 8000 is in use:

```bash
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

---

## 2. Frontend setup and run

**Install and run only from the `frontend/` directory** (do not run `npm install` at repo root):

In a **separate terminal**:

```bash
cd frontend
npm install
npm run dev
```

Or from the project root: `npm run dev:frontend`

- **App:** http://localhost:5173  
- **Landing:** http://localhost:5173/  
- **Dashboard:** http://localhost:5173/dashboard  

---

## 3. Testing the backend

### 3.1 Health check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

### 3.2 Root

```bash
curl http://localhost:8000/
```

Expected: `{"message":"Metricare API is running"}`

### 3.3 Patient endpoints (stub data)

Replace `PATIENT_ID` with any string (e.g. `123`).

**Get patient:**
```bash
curl http://localhost:8000/patient/PATIENT_ID
```

**Get patient history:**
```bash
curl http://localhost:8000/patient/PATIENT_ID/history
```

**Get patient medications:**
```bash
curl http://localhost:8000/patient/PATIENT_ID/medications
```

**Get contraindications (FDA-based):**
```bash
curl http://localhost:8000/patient/PATIENT_ID/contraindications
```

### 3.4 AI summary (Gemini)

Requires `GEMINI_API_KEY` in `backend/.env`. Sends history + medications to Gemini and returns a short summary.

```bash
curl -X POST http://localhost:8000/patient/summary \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Test Patient",
    "history": [
      {"label": "Checkup", "date": "Jan 2025", "items": ["Routine exam"]}
    ],
    "medications": [
      {"label": "Aspirin", "items": ["81mg daily"]}
    ]
  }'
```

Expected shape: `[{"type": "diagnostic", "summary": "..."}]`. If the key is missing or invalid, you get a 500 with a Gemini error message.

### 3.5 Drug search and drug info (FDA)

**Search drugs by name:**
```bash
curl "http://localhost:8000/drugs/search?q=aspirin"
```

**Get drug info by name:**
```bash
curl http://localhost:8000/drugs/aspirin
```

### 3.6 Using Swagger UI

1. Open http://localhost:8000/docs  
2. Expand an endpoint, click **Try it out**, set parameters or request body, then **Execute**.  
3. For **POST /patient/summary**, use the same JSON body as in the curl example above.

---

## 4. Quick reference

| What              | Command / URL |
|-------------------|----------------|
| Backend (from repo root) | `npm run dev` or `npm run dev:backend` |
| Backend (from backend/)  | `uvicorn main:app --reload --host 0.0.0.0 --port 8000` |
| Frontend (from repo root) | `npm run dev:frontend` |
| Frontend (from frontend/) | `npm run dev` → http://localhost:5173 |
| API docs          | http://localhost:8000/docs |
| Health            | http://localhost:8000/health |

---

## 5. Security note

`backend/.env` is gitignored. Do not commit API keys. If a key was ever committed, rotate it in the provider’s console.
