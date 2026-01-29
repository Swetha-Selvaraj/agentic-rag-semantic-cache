

# Agentic RAG (with Semantic Cache and Memory)

An **agentic RAG system** with:

* **Qdrant** → internal knowledge vector DB
* **Redis Stack** → semantic cache + conversation memory
* **FastAPI** → inference API
* **Sentence Transformer** → for embeddings
* **OpenAI** for generation
* **Web search fallback** → Tavilly

---

## Architecture (High Level)

```
User Query
   ↓
Semantic Cache (Redis)
   ↓ miss
Agent Planner
   ↓
Internal Search (Qdrant)
   ↓ miss
Web Search
   ↓
LLM Answer
   ↓
Semantic Cache (internal only)
```

---

## Prerequisites

* Python **3.11+**
* Docker & Docker Compose
* macOS 

---

## Project Structure

```
Semantic/
├── app/
│   ├── main.py          # FastAPI entry
│   ├── agent.py         # Tool planning + execution
│   ├── cache.py         # Semantic cache (Redis)
│   ├── retriever.py     # Qdrant search
│   ├── llm.py           # LLM wrapper
│   └── memory.py        # Conversation memory
│
├── ingestion/
│   ├── ingest_policy.py # Data ingestion entry
│   ├── text_loader.py   # Text loader
│   ├── chunker.py       # Chunking logic
│   └── embeddings.py    # Embedding model
│
├── policies/
│   └── password_policy_v1.txt
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup

### 1️⃣ Clone & Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 2️⃣ Start Infrastructure

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

### 3️⃣ Create Redis Semantic Cache Index (One-Time)

```bash
docker exec -it redis-stack redis-cli
```

```bash
FT.CREATE semantic_cache_index ON HASH PREFIX 1 scache: SCHEMA embedding VECTOR FLAT 6 TYPE FLOAT32 DIM 384 DISTANCE_METRIC COSINE answer TEXT
```

---

### 4️⃣ Ingest Internal Data

```bash
python ingestion/ingest_policy.py
```

---

### 5️⃣ Start API

```bash
uvicorn app.main:app --reload --port 8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

## Usage

### Ask a Question

```bash
curl -X POST \
"http://127.0.0.1:8000/query?question=What is the password expiration policy?"
```

---

### Semantic Cache Test

```bash
curl -X POST \
"http://127.0.0.1:8000/query?question=How often must passwords be changed?"
```

Expected:

* Instant response
* No vector / web search
* Cache hit

---

## Redis Dashboard

Open:

```
Redis Insight
```

Connect Redis:

* Host: `localhost`
* Port: `6379`

View:

* `scache:*` → semantic cache
* `memory:*` → conversation history
* `semantic_cache_index` → vector index

---
<img width="1470" height="923" alt="Screenshot 2025-12-15 at 1 42 08 AM" src="https://github.com/user-attachments/assets/f18ff738-dabd-4ecc-8afc-1bc71fbd0256" />

## Key Design Rules

* Internal knowledge **always overrides** web data
* Web answers are **also cached** for practicing (not advisible)
* Cache is **semantic**, not exact
* LLM output is **validated + normalized**


---

## Next Improvements

* Policy versioning
* Role-based access
* Evaluation metrics



