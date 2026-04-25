<div align="center">

# 🛡️ InnoGuard AI

### *AI-Powered IP Strategy & Decision Intelligence for Malaysian SMEs*

[![Live App](https://img.shields.io/badge/Live%20App-innoguardai.lovable.app-brightgreen?style=for-the-badge&logo=vercel)](https://innoguardai.lovable.app)
[![Backend API](https://img.shields.io/badge/Backend%20API-Live-009688?style=for-the-badge&logo=fastapi)](https://backendinnoguardai-1.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/Swagger-Docs-blue?style=for-the-badge&logo=swagger)](https://backendinnoguardai-1.onrender.com/docs)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Democratizing IP Strategy and Decision Intelligence for Malaysian SMEs**

*Built for the AI for Economic Empowerment & Decision Intelligence Hackathon 🇲🇾*

[🌐 Live Demo](https://innoguardai.lovable.app) · [⚙️ Backend API](https://backendinnoguardai-1.onrender.com) · [📖 Swagger UI](https://backendinnoguardai-1.onrender.com/docs) · [📁 GitHub Backend](https://github.com/Jeevanesh18/BackendInnoGuardAI) · [📂 Project Documents](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing)

</div>

---

## 🎬 Pitching Video

> 📹 **Watch our demo pitch here:**
> 👉 [Click to watch on Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing)

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [The Problem We Solve](#-the-problem-we-solve)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [User Flow](#-user-flow)
- [Getting Started — Backend](#-getting-started--backend)
- [Getting Started — Frontend](#-getting-started--frontend)
- [API Reference](#-api-reference)
- [Frontend Project Structure](#-frontend-project-structure)
- [CORS & Proxy Setup](#-cors--proxy-setup)
- [Database & Seeded Data](#-database--seeded-data)
- [Impact Metrics](#-impact-metrics)
- [Project Documents](#-project-documents)
- [Team](#-team)

---

## 🧠 About the Project

InnoGuard AI is an **AI-powered Decision Intelligence platform** that acts as a virtual Intellectual Property (IP) strategist for Malaysian SMEs and independent creators. By leveraging **Z.AI's GLM** as its core intelligence engine, it analyzes unstructured product descriptions against structured legal/patent databases (MyIPO) and provides actionable, legally-informed strategies.

Unlike simple keyword-matching tools, InnoGuard AI uses **semantic vector search** and **large language model reasoning** to:

- Understand the *meaning* of your invention, not just its keywords
- Cross-reference it against a patent database at a conceptual level
- Predict infringement risk *before* you spend money filing
- Auto-generate legal-quality MyIPO patent drafts and NDAs in minutes

> ⚠️ **Critical Requirement:** Z.AI's GLM (`ilmu-glm-5.1` via `api.ilmu.ai`) is the **mandatory core engine** of this solution. Without the GLM, the system cannot perform semantic similarity checks, calculate trade-off analyses, or generate legal drafts. The GLM wrapper (`ask_glm()`) is retained in `main.py` for judges' reference.

---

## 🔥 The Problem We Solve

| Pain Point                    | Reality                                   |
| ----------------------------- | ----------------------------------------- |
| 💸 Patent lawyer consultation | Costs **RM 5,000–15,000** before filing   |
| ⏳ Preliminary patent research | Takes **3–4 weeks** manually              |
| ❓ Infringement risk           | Unknown until **after** filing (too late) |
| 📄 Document drafting          | Requires expensive legal expertise        |

**InnoGuard AI solves all four — in under 5 minutes, for a fraction of the cost.**

---

## ✨ Key Features

| Feature                               | Description                                                                                                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 🔍 **Semantic IP Similarity Engine**  | Converts invention descriptions into 1536-dim vectors and finds conceptual overlaps with existing patents — not just keyword matches |
| ⚖️ **Trade-Off & Risk Analyzer**      | Scores infringement risk 0–100 and recommends whether to file a Standard Patent or Utility Innovation                                |
| 🔄 **Self-Correcting Idea Generator** | Identifies underserved patent whitespace and generates novel ideas, then auto-refines them if too similar to existing patents        |
| 🧭 **Strategic Pivot Advisor**        | Provides 2 specific, actionable technical changes to avoid infringement                                                              |
| 📄 **Legal Document Drafter**         | Auto-fills MyIPO Utility Innovation Form (Form P1) and generates a customized NDA — both as downloadable PDFs                        |
| 🔍 **Market Whitespace Finder**       | Analyzes patents in a specific category to find what has *not* been invented yet, directing R&D budgets to profitable gaps           |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│              (React 18 + Vite 5 + Tailwind CSS)            │
│              https://innoguardai.lovable.app                │
└─────────────────────┬───────────────────────────────────────┘
                      │  HTTP POST (JSON)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│         https://backendinnoguardai-1.onrender.com           │
│                                                             │
│  ┌─────────────────┐   ┌──────────────────────────────┐    │
│  │  /generate-idea  │   │       /evaluate-idea          │    │
│  │  /generate-docs  │   │                              │    │
│  └────────┬────────┘   └──────────────┬───────────────┘    │
│           │                           │                      │
│           ▼                           ▼                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ChromaDB (Vector Database)               │   │
│  │      Patent embeddings (text-embedding-3-small)       │   │
│  └──────────────────────────────────────────────────────┘   │
│           │                                                   │
│           ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Z.AI GLM (substitute with OpenAI) — Core Intelligence Engine         │   │
│  │  Creative generation / Risk analysis / Doc drafting   │   │
│  └──────────────────────────────────────────────────────┘   │
│           │                                                   │
│           ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         /download/ (Static PDF File Server)           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

| Layer               | Technology                                          | Purpose                                          |
| ------------------- | --------------------------------------------------- | ------------------------------------------------ |
| **Framework**       | FastAPI (Python)                                    | High-performance REST API with auto Swagger docs |
| **Core LLM**        | Z.AI GLM (`ilmu-glm-5.1`) (substituted with OpenAI) | Semantic reasoning, risk analysis, doc drafting  |
| **Vector Database** | ChromaDB (Persistent)                               | Stores patent embeddings for semantic search     |
| **Embeddings**      | OpenAI `text-embedding-3-small`                     | Converts text to 1536-dim semantic vectors       |
| **Clustering**      | Scikit-learn (K-Means)                              | Groups patents into patent sub-categories        |
| **PDF Generation**  | fpdf2                                               | Renders LLM output as downloadable PDF files     |
| **File Serving**    | FastAPI StaticFiles                                 | Serves generated PDFs at `/download/`            |
| **Environment**     | python-dotenv                                       | Manages API keys securely                        |
| **Deployment**      | Render.com                                          | Live cloud hosting                               |

### Frontend

| Technology   | Version | Purpose                   |
| ------------ | ------- | ------------------------- |
| React        | 18      | UI component framework    |
| Vite         | 5       | Build tool and dev server |
| Tailwind CSS | 3       | Utility-first styling     |
| React Router | 6       | Client-side routing       |
| Fetch API    | Native  | HTTP calls to the backend |

---

## 🗺️ User Flow

The app is a **linear 3-step wizard**. Each step feeds its output into the next.

```
┌──────────────────────────────────────────────────────────┐
│  STEP 1 — Discover                                        │
│  POST /api/v1/generate-idea                               │
│  Input:  category + focus_area                            │
│  Output: Novel invention idea (AI-verified unique)        │
│                  [  Evaluate This Idea →  ]               │
└─────────────────────┬────────────────────────────────────┘
                      │ Pre-fills title & description
                      ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 2 — Evaluate                                        │
│  POST /api/v1/evaluate-idea                               │
│  Input:  title + description + tech_specs                 │
│  Output: Risk score (0-100), verdict, pivots,             │
│          similar patents list                             │
│                  [  Generate Documents →  ]               │
└─────────────────────┬────────────────────────────────────┘
                      │ Pre-fills final_idea
                      ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 3 — Document                                        │
│  POST /api/v1/generate-docs                               │
│  Input:  final_idea + user_name                           │
│  Output: MyIPO patent draft PDF + NDA PDF (downloadable) │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started — Backend

### Prerequisites

- Python 3.10+
- A Z.AI API key (core GLM engine — **mandatory**)
- An OpenAI API key (for embeddings)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Jeevanesh18/BackendInnoGuardAI.git
cd BackendInnoGuardAI

# 2. Install dependencies
pip install fastapi uvicorn chromadb openai fpdf2 numpy python-dotenv scikit-learn

# 3. Create your environment file
cp .env.example .env
# Then fill in your keys in .env
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-key-here
ZAI_API_KEY=your-zai-key-here
```

> ⚠️ Both variables must be present or the server will throw a `ValueError` on startup.

### Running the Server

```bash
# Development (with auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production
python main.py
```

The server will automatically seed the patent database on first run via `run_background_ingestion()`.

Once running, visit:

- **API Root:** `http://localhost:8000/`
- **Interactive Docs:** `http://localhost:8000/docs`

---

## 🚀 Getting Started — Frontend

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# 1. Clone the frontend repository
git clone https://github.com/your-username/innoguard-ai-frontend.git
cd innoguard-ai-frontend

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env

# 4. Start the development server
npm run dev
```

The app will be available at `http://localhost:5173`.

```bash
# Build for production
npm run build
npm run preview
```

### Environment Variables (Frontend)

```env
VITE_API_BASE_URL=https://backendinnoguardai-1.onrender.com
```

---

## 📡 API Reference

**Base URL (Production):** `https://backendinnoguardai-1.onrender.com`

All endpoints accept and return `application/json`.

---

### 1. `POST /api/v1/generate-idea`

Identifies an underserved patent whitespace and generates a novel, AI-verified product idea.

**Request Body:**

```json
{
  "category": "F&B Delivery",
  "focus_area": "Sustainable and affordable cooling using no electricity"
}
```

| Field        | Type   | Required | Valid Values                                  |
| ------------ | ------ | -------- | --------------------------------------------- |
| `category`   | string | ✅        | `"F&B Delivery"` or `"Logistics"`             |
| `focus_area` | string | ✅        | Free-text description of innovation direction |

**Internal Flow:**

```
1. Query ChromaDB for all patents matching the category
2. Count patents per sub-group → find the group with FEWEST patents (the whitespace)
3. GLM Prompt 1 (Creative): Generate a novel product idea as JSON
4. Embed the draft idea → run similarity check vs. full database
5. If similarity > 50% → GLM Prompt 2 (Refinement): Refine to be more distinct
6. Return the verified final idea
```

**Success Response `200 OK`:**

```json
{
  "status": "success",
  "whitespace_found": "Biodegradable Passive Cooling",
  "idea": {
    "title": "Banana-Leaf Composite Cooling Box",
    "description": "A delivery box using treated banana-fiber for insulation.",
    "technical_innovation": "Uses vacuum-sealed fiber layers to replace plastic foam."
  },
  "verification": "First draft highly unique. Highest similarity match was only 15%."
}
```

---

### 2. `POST /api/v1/evaluate-idea`

Performs a deep semantic patent infringement risk analysis on a user's invention.

**Request Body:**

```json
{
  "title": "USB Heated Pizza Bag",
  "description": "A bag with a carbon fiber heating element powered by a 5V USB bank.",
  "tech_specs": "Dual-layer thermal insulation, 10W power draw."
}
```

**Success Response `200 OK`:**

```json
{
  "risk_assessment": {
    "risk_score": 85,
    "verdict": "High Infringement Risk",
    "reasoning": "Overlap with Patent MY-882 (Carbon Fiber Heating for Bags).",
    "closest_match": "Carbon Fiber Heating for Bags"
  },
  "recommendation": {
    "patent_type": "Utility Innovation",
    "pivots": [
      "Switch from resistive wire to induction heating to avoid MY-882",
      "Focus the patent on the latching mechanism instead of the heat."
    ]
  },
  "similar_patents": [
    {"id": "MY-882", "similarity": "89%", "owner": "FoodCorp Ltd"}
  ]
}
```

**Risk Score Reference:**

| Score Range  | Verdict          | Recommended Action                          |
| ------------ | ---------------- | ------------------------------------------- |
| **0 – 39**   | 🟢 Low Risk      | Safe to proceed with patent filing          |
| **40 – 69**  | 🟡 Moderate Risk | Review pivots before filing                 |
| **70 – 100** | 🔴 High Risk     | Apply recommended pivots; do not file as-is |

---

### 3. `POST /api/v1/generate-docs`

Generates a MyIPO Utility Innovation patent draft and NDA as downloadable PDF files.

> ⏱️ **This endpoint takes 20–30 seconds.** Always show a loading state on the frontend.

**Request Body:**

```json
{
  "final_idea": "Induction-based Thermal Bag",
  "user_name": "Ali Bin Ahmad",
  "doc_type": "patent",
  "NDA_optional": "NDA_FORM"
}
```

**Success Response `200 OK`:**

```json
{
  "status": "documents_generated",
  "user": "Ali Bin Ahmad",
  "files": {
    "patent_form_url": "https://backendinnoguardai-1.onrender.com/download/MyIPO_41af1.pdf",
    "nda_url": "https://backendinnoguardai-1.onrender.com/download/NDA_c0224.pdf"
  },
  "preview": {
    "patent_snippet": "**Technical Description**\n\n**Title of Invention:** Induction-based Thermal Bag...",
    "nda_snippet": "**NON-DISCLOSURE AGREEMENT (NDA)**..."
  }
}
```

**Generated Patent Includes:**

- Title, Field, Background, and Summary of Invention
- Detailed Description (with numbered component list)
- Claims (up to 7 structured claims per MyIPO Form P1 format)

**Generated NDA Includes:**

- Parties: Inventor vs. `[Manufacturer]`
- Obligations of Confidentiality (5-year duration)
- Governing Law: **Malaysia**
- Return of Materials clause

---

### `GET /` — Health Check

```json
{ "message": "InnoGuard AI API is live" }
```

### `GET /download/{filename}` — PDF Download

```
GET https://backendinnoguardai-1.onrender.com/download/MyIPO_41af1.pdf
```

> ⚠️ PDF files reset on every Render.com redeploy. Do not cache download URLs across sessions.

---

## 📁 Frontend Project Structure

```
innoguard-ai-frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── StepIndicator.jsx       # Top progress bar (Step 1 → 2 → 3)
│   │   ├── LoadingSpinner.jsx       # Reusable loading state
│   │   ├── RiskGauge.jsx            # Circular risk score (0–100)
│   │   ├── PatentCard.jsx           # Similar patent display card
│   │   └── DownloadButton.jsx       # PDF download button
│   ├── pages/
│   │   ├── Step1GenerateIdea.jsx    # POST /api/v1/generate-idea
│   │   ├── Step2EvaluateIdea.jsx    # POST /api/v1/evaluate-idea
│   │   └── Step3GenerateDocs.jsx    # POST /api/v1/generate-docs
│   ├── App.jsx                      # Main app with routing
│   ├── main.jsx                     # React entry point
│   └── index.css                    # Tailwind imports
├── .env.example
├── vite.config.js                   # Includes API proxy config
├── tailwind.config.js
└── package.json
```

---

## 🔒 CORS & Proxy Setup

### Option A — Vite Dev Proxy (Recommended for development)

```js
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'https://backendinnoguardai-1.onrender.com',
        changeOrigin: true,
        secure: true,
      }
    }
  }
}
```

### Option B — FastAPI CORS Middleware (For production)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://innoguardai.lovable.app"],  # or ["*"] for demo
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🗄️ Database & Seeded Data

On every server startup, `run_background_ingestion()` automatically seeds ChromaDB with 5 patents representing real-world Malaysian IP categories.

### Seeded Patents

| Title                                                          | Category     | Key Technologies                                    |
| -------------------------------------------------------------- | ------------ | --------------------------------------------------- |
| Thermally Regulated Multi-Layer Composite Packaging            | F&B Delivery | Vacuum Insulation (VIP), PCM, Fumed Silica          |
| Wireless Induction Heating System for Portable Food Containers | F&B Delivery | Induction Coils, Resonant Inverters, Li-Po          |
| Hydrophobic Nanocoatings for Moisture-Sensitive Food Packaging | F&B Delivery | CVD, SiO2 Nanostructure, Hydrophobic Polymers       |
| Shock-Absorbent Mycelium-Based Cargo Cushioning                | Logistics    | Mycelium Growth, Bio-Composite, Cold-Press Moulding |
| IoT-Enabled Smart Latching for Secure Parcel Lockers           | Logistics    | ESP32, AES-128 Encryption, Blockchain QR            |

### Clustering Logic

```
DISTANCE_THRESHOLD = 0.5

For each new patent:
  1. Embed to 1536-dim vector
  2. Compute cosine similarity against all existing vectors
  3. If max_similarity < 0.5 → CREATE new sub-group
     → GLM generates a 3-word professional label for this group
  4. If max_similarity >= 0.5 → JOIN the most similar existing sub-group
```

---

## 📊 Impact Metrics

| Metric                     | Without InnoGuard          | With InnoGuard AI              |
| -------------------------- | -------------------------- | ------------------------------ |
| **IP research cost**       | RM 5,000–15,000 (lawyer)   | ~RM 50 (platform subscription) |
| **Research time**          | 3–4 weeks                  | Under 5 minutes                |
| **Infringement awareness** | Unknown until after filing | Scored before you build        |
| **Document drafting**      | Days with legal expert     | Auto-generated in ~30 seconds  |
| **Cost reduction**         | Baseline                   | **~90% reduction**             |

---

## 📂 Project Documents

All official project documentation is available in PDF format on our GitHub repository and Google Drive:

| Document                                 | Description                                                        | Link                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| 📄 PRD (Product Requirements Document)   | Full product specification, features, and hackathon rubric mapping | [Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing) |
| 🏛️ SAD (System Architecture Document)   | Detailed system architecture and component breakdown               | [Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing) |
| 🔧 TAD (Technical Architecture Document) | API specs, data flow, and implementation details                   | [Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing) |
| 📊 Pitch Deck                            | Hackathon presentation slides                                      | [Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing) |
| 🎬 Pitching Video                        | Recorded demo and pitch                                            | [Google Drive](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing) |

---

## 👥 Team

Built for the **AI for Economic Empowerment & Decision Intelligence Hackathon 🇲🇾**

| Name                   | Role               |
| ---------------------- | ------------------ |
| **Kedrick Selvanesan** | Frontend Developer |
| **Jeevanes Gunalan**   | Frontend Developer |
| **Kalvinn Roy Danial** | Backend Developer  |
| **Sharveen**           | Backend Developer  |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**Built with ❤️ in Malaysia 🇲🇾**

*InnoGuard AI — Because every Malaysian SME deserves world-class IP strategy.*

[🌐 Live Demo](https://innoguardai.lovable.app) · [⚙️ API Docs](https://backendinnoguardai-1.onrender.com/docs) · [📁 GitHub](https://github.com/Jeevanesh18/BackendInnoGuardAI) · [📂 Project Docs](https://drive.google.com/drive/folders/1KfNDLMDBJOCYATnqpa709VK_B8t5xKzW?usp=sharing)

</div>
