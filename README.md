# AI Engineering Change Assistant

An AI-assisted engineering change management application that combines **PLM-style product data**, **deterministic BOM impact analysis**, **domain-aware RAG**, and a **locally hosted LLM** to support engineering change reviews.

The application identifies affected parts and assemblies, evaluates change impact across multiple BOM levels, retrieves relevant engineering guidelines, and generates evidence-grounded engineering recommendations using a local Llama model through Ollama.

---

## Overview

Engineering changes can affect multiple parts, assemblies, documents, validation activities, and stakeholders.

The **AI Engineering Change Assistant** provides a lightweight PLM-style workflow for managing engineering changes while using AI as an advisory layer.

For each engineering change, the system can:

- identify the affected part
- determine where that part is used
- recursively calculate impacted assemblies
- assign a deterministic baseline risk
- retrieve relevant engineering guidance using RAG
- generate an engineering assessment using a local LLM
- identify potential risks
- highlight missing information
- suggest relevant engineering reviewers
- show the source evidence used by the AI

The LLM does **not** determine BOM relationships or modify product data. Product relationships and baseline risk are calculated deterministically by the backend.

---

## Architecture

```text
                         React + TypeScript
                                │
                                ▼
                           FastAPI API
                                │
               ┌────────────────┴────────────────┐
               │                                 │
               ▼                                 ▼
          PostgreSQL                         ChromaDB
               │                                 │
      PLM/Product Data                  Engineering Knowledge
               │                                 │
      Parts / Revisions                     Embeddings
      BOM / Changes                            │
               │                       nomic-embed-text
               │                                 │
               └───────────────┬─────────────────┘
                               ▼
                           Llama 3.2
                          via Ollama
                               │
                               ▼
                    AI Engineering Analysis
```

---

## Key Design Principle

The system separates deterministic engineering data from generative AI reasoning.

```text
PostgreSQL / Backend
→ determines what is affected

Deterministic rules
→ determine baseline risk

RAG
→ retrieves relevant engineering knowledge

LLM
→ explains engineering implications

Engineer
→ makes the final decision
```

This prevents the LLM from being responsible for critical product-structure calculations.

---

## Features

### PLM-Style Product Management

The application manages:

- Parts
- Part revisions
- Lifecycle states
- Bill of Materials
- Engineering Changes

Example product structure:

```text
VEH-001 — Vehicle Electronics Module
└── ASSY-100 — ECU Assembly
    ├── BRK-001 — ECU Bracket
    ├── ECU-100 — Main ECU
    ├── HAR-201 — Wiring Harness
    └── BLT-006 — Bolt M6
```

---

### Revision Management

Parts can contain revision histories such as:

```text
BRK-001
├── Revision A — Released
└── Revision B — In Work
```

---

### BOM Management

The application stores parent-child relationships between parts.

Example:

```text
ASSY-100
├── BRK-001 ×1
├── ECU-100 ×1
├── HAR-201 ×1
└── BLT-006 ×4
```

---

### Where-Used Analysis

The backend can determine which assemblies contain a specific component.

Example:

```text
BRK-001
   ↑
ASSY-100
```

---

### Recursive Impact Analysis

Impact analysis continues recursively through higher-level assemblies.

Example:

```text
BRK-001
   ↑
ASSY-100
   ↑
VEH-001
```

The backend therefore identifies:

```text
Level 1 → ASSY-100
Level 2 → VEH-001
```

This analysis is calculated using PostgreSQL and Python rather than an LLM.

---

## Engineering Change Management

Example engineering change:

```text
Change Number: EC-001
Title: Replace ECU Bracket
Affected Part: BRK-001
Reason: Vibration failures detected during endurance testing
Status: Draft
```

The system automatically combines the engineering change with the product structure to determine affected assemblies.

---

## Deterministic Risk Assessment

The initial baseline risk is calculated by backend rules rather than by the LLM.

Current simplified rule:

```text
No impacted assemblies
→ Low

Level 1 impact
→ Medium

Level 2+ impact
→ High
```

For example:

```text
BRK-001
↓
ASSY-100
↓
VEH-001
```

produces:

```text
Impact Depth: 2
Baseline Risk: High
```

The backend enforces this value even if the LLM generates a different risk level.

---

## Local LLM

The application uses:

**Llama 3.2**

through:

**Ollama**

The model runs locally and does not require a paid inference API.

The LLM receives structured information including:

- engineering change details
- affected part
- lifecycle state
- impacted assemblies
- deterministic risk
- retrieved engineering guidance

It then generates:

- engineering summary
- potential risks
- missing information
- suggested reviewers

---

## Retrieval-Augmented Generation

The application uses RAG to provide company/domain knowledge to the LLM.

Example engineering knowledge files:

```text
docs/knowledge/
├── bracket_design_guidelines.txt
├── vibration_guidelines.txt
├── wiring_harness_guidelines.txt
└── engineering_change_process.txt
```

Documents are converted into embeddings using:

```text
nomic-embed-text
```

and stored in:

```text
ChromaDB
```

---

## Domain-Aware Retrieval

Retrieval combines semantic similarity with engineering-domain metadata.

For example:

```text
Affected Part:
HAR-201 — Wiring Harness
```

can prioritize:

```text
wiring_harness_guidelines.txt
vibration_guidelines.txt
```

instead of retrieving bracket-specific documentation.

This improves retrieval relevance compared with purely similarity-based search.

---

## Evidence-Grounded AI Analysis

AI results include the source documents and retrieved text used during analysis.

Example:

```text
Risk Level
High

Summary
The routing change affects multiple product levels and should
be validated under expected vibration and thermal conditions.

Potential Risks
- Harness abrasion or chafing
- Connector strain
- Insufficient component clearance

Missing Information
- Validation results
- Updated routing documentation

Suggested Reviewers
- Mechanical Engineer
- Electrical Engineer

Sources
- wiring_harness_guidelines.txt
- vibration_guidelines.txt
```

The UI also shows the retrieved document content so users can inspect the evidence behind the analysis.

---

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Database

- PostgreSQL

### AI / RAG

- Ollama
- Llama 3.2
- nomic-embed-text
- ChromaDB

### Development

- Git
- GitHub
- VS Code
- PowerShell

---

## Project Structure

```text
ai-engineering-change-assistant/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── service.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingest.py
│   │   │   └── retriever.py
│   │   │
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── .venv/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── Parts.tsx
│       │   ├── PartDetail.tsx
│       │   ├── Bom.tsx
│       │   ├── Changes.tsx
│       │   ├── ChangeDetail.tsx
│       │   └── AiAnalysis.tsx
│       │
│       ├── App.tsx
│       └── App.css
│
├── docs/
│   └── knowledge/
│       ├── bracket_design_guidelines.txt
│       ├── vibration_guidelines.txt
│       ├── wiring_harness_guidelines.txt
│       └── engineering_change_process.txt
│
├── database/
│   └── chroma/
│
├── README.md
└── .gitignore
```

---

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/siddhant1621/ai-engineering-change-assistant.git
cd ai-engineering-change-assistant
```

---

### 2. PostgreSQL

Create a PostgreSQL database:

```text
engineering_change_db
```

Create:

```text
backend/.env
```

and configure:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/engineering_change_db
```

Do not commit `.env`.

---

### 3. Backend

```powershell
cd backend

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Install Ollama

Install Ollama and verify:

```powershell
ollama --version
```

Pull the local LLM:

```powershell
ollama pull llama3.2
```

Pull the embedding model:

```powershell
ollama pull nomic-embed-text
```

Verify:

```powershell
ollama list
```

---

### 5. Ingest Engineering Knowledge

From the project root:

```powershell
backend\.venv\Scripts\python.exe -m backend.app.rag.ingest
```

This creates embeddings for documents in:

```text
docs/knowledge/
```

and stores them in ChromaDB.

---

### 6. Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Main API Endpoints

### Parts

```text
GET    /api/parts
POST   /api/parts
GET    /api/parts/{part_number}
```

### Revisions

```text
GET    /api/parts/{part_number}/revisions
POST   /api/parts/{part_number}/revisions
DELETE /api/revisions/{revision_id}
```

### BOM

```text
GET    /api/parts/{part_number}/bom
POST   /api/parts/{part_number}/bom
DELETE /api/bom-items/{bom_item_id}
```

### Impact Analysis

```text
GET /api/parts/{part_number}/where-used
GET /api/parts/{part_number}/impact
```

### Engineering Changes

```text
GET  /api/changes
POST /api/changes
GET  /api/changes/{change_number}
```

### AI Analysis

```text
POST /api/changes/{change_number}/analyze
```

---

## Example Workflow

An engineer creates:

```text
EC-002
Improve Wiring Harness Routing
```

Affected part:

```text
HAR-201 — Wiring Harness
```

The backend determines:

```text
HAR-201
   ↓
ASSY-100
   ↓
VEH-001
```

Therefore:

```text
Impact Depth: 2
Risk Level: High
```

RAG retrieves relevant documents:

```text
wiring_harness_guidelines.txt
vibration_guidelines.txt
```

Llama then produces an evidence-grounded engineering assessment.

---

## Why Local AI?

The project intentionally uses a local LLM rather than a paid hosted API.

Benefits include:

- no inference API cost
- no API key dependency
- local experimentation
- improved data privacy
- easy model replacement
- suitable architecture for sensitive engineering information

---

## Current Development Status

Implemented:

- [x] React application shell
- [x] FastAPI backend
- [x] PostgreSQL persistence
- [x] Part management
- [x] Part revisions
- [x] BOM management
- [x] Where-used analysis
- [x] Recursive impact analysis
- [x] Engineering Change creation
- [x] Engineering Change detail view
- [x] Deterministic risk scoring
- [x] Local Llama integration
- [x] ChromaDB vector store
- [x] Local document embeddings
- [x] RAG retrieval
- [x] Domain-aware retrieval
- [x] Evidence-grounded AI analysis
- [x] Engineering Change creation from React

Planned:

- [ ] Engineering Change lifecycle workflow
- [ ] Draft → Review → Approved → Released transitions
- [ ] AI analysis feedback
- [ ] Persistent AI-analysis history
- [ ] Improved retrieval evaluation
- [ ] Automated tests
- [ ] Docker deployment
- [ ] Authentication and roles
- [ ] LoRA/fine-tuning experiments using collected feedback

---

## Future Architecture

Future development will focus on moving from a prototype toward a more production-oriented engineering application.

Planned improvements include:

```text
Engineering Change
        ↓
Lifecycle Workflow
        ↓
Deterministic Impact Analysis
        ↓
Domain-Aware RAG
        ↓
Local LLM
        ↓
Human Feedback
        ↓
Evaluation Dataset
        ↓
Potential Fine-Tuning
```

---

## AI Safety and Engineering Principles

The AI assistant is intentionally designed as an advisory system.

It does not:

- autonomously approve engineering changes
- modify BOM structures
- modify lifecycle states
- invent product relationships
- replace engineering validation
- replace human engineering review

The backend remains the source of truth for structured product data and deterministic calculations.

---

## Project Goal

The goal of this project is to demonstrate how traditional enterprise engineering software and modern AI systems can be combined responsibly.

Rather than replacing PLM logic with an LLM, the application combines:

```text
Structured Product Data
+
Deterministic Engineering Logic
+
Retrieval-Augmented Generation
+
Local LLM Reasoning
+
Human Engineering Review
```

to create an explainable AI-assisted engineering change workflow.

---

## Author

**Siddhanth Tagade**

Focus areas:

- Full-Stack Development
- AI-assisted enterprise applications
- Product Lifecycle Management
- Backend Engineering
- Retrieval-Augmented Generation
- Local LLM integration
