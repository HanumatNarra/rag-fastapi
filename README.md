# RAG API — FastAPI + ChromaDB + Ollama

[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688.svg)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6B35.svg)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-000000.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A REST API for document question-answering using Retrieval-Augmented Generation. Upload documents, ask questions in plain English, get answers grounded in your actual content — all running locally with no cloud dependencies or API costs.

---

## Why This Exists

Most RAG demos are single-user toys. This one is built with a **multi-tenant architecture** from the start — multiple users can upload their own documents and query them independently, with ChromaDB's metadata filtering ensuring complete data isolation between users in a shared vector database. No separate collections per user, no separate databases — just clean metadata-based filtering that scales.

---

## How It Works

```
User Question
     │
     ▼
Generate Embedding (nomic-embed-text via Ollama)
     │
     ▼
Vector Similarity Search in ChromaDB
(filtered by user metadata for isolation)
     │
     ▼
Inject Top-K Chunks into LLM Prompt
     │
     ▼
Generate Answer (llama3.2:3b via Ollama)
     │
     ▼
Return Answer + Source Context
```

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| API Framework | FastAPI | Async support, automatic OpenAPI docs, Pydantic validation |
| Vector Database | ChromaDB | Lightweight, embedded, no infrastructure needed |
| LLM Inference | Ollama (llama3.2:3b) | Run production-quality LLMs locally, zero API cost |
| Embeddings | Ollama (nomic-embed-text) | Fast, local semantic embeddings |
| Validation | Pydantic | Type-safe request/response models |

---

## Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed and running

### Installation

```bash
git clone https://github.com/HanumatNarra/rag-fastapi.git
cd rag-fastapi

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install fastapi uvicorn chromadb ollama

# Pull the required models
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Run

```bash
uvicorn main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

## API Reference

### `POST /documents` — Add a document

```json
{
  "user_name": "john_doe",
  "content": "John Doe is a software engineer specializing in AI and machine learning..."
}
```

**Response:**
```json
{
  "message": "Added 3 chunks for user 'john_doe'.",
  "user_name": "john_doe",
  "chunks_added": 3
}
```

Documents are automatically split into paragraph-level chunks before embedding. Each chunk is stored with user metadata for isolation.

---

### `GET /ask` — Query the knowledge base

```bash
curl "http://127.0.0.1:8000/ask?question=What does John do?&user=john_doe"
```

**Response:**
```json
{
  "question": "What does John do?",
  "answer": "John Doe is a software engineer who specializes in AI and machine learning.",
  "context_used": ["John Doe is a software engineer..."],
  "filtered_by_user": "john_doe"
}
```

The `user` parameter is optional — omit it to search across all documents in the knowledge base.

---

## Project Structure

```
rag-fastapi/
├── main.py          # FastAPI app — multi-tenant endpoints
├── embed.py         # Standalone embedding script
├── app.py           # Single-user prototype (reference only)
├── my_info.txt      # Sample document for testing
├── chroma_db/       # Vector store (auto-created on first run)
└── README.md
```

---

## Technical Decisions

**Multi-tenancy via metadata filtering, not separate collections**
The straightforward approach to multi-tenancy in a vector DB is one collection per user. The problem is that doesn't scale — you end up managing hundreds of collections. Instead, all documents go into a single ChromaDB collection and each chunk carries a `user_name` metadata field. Queries filter on that field, giving you the same isolation at a fraction of the overhead.

**Local-first with Ollama**
Using Ollama means this entire stack runs on a laptop with no internet connection, no API keys, and no rate limits. The tradeoff is hardware — `llama3.2:3b` needs a reasonable machine to run comfortably. Swapping in an OpenAI or Anthropic client is a one-line change if you need cloud inference.

**Paragraph-level chunking**
Documents are split by paragraph rather than fixed token windows. This keeps semantically related content together, which improves retrieval relevance on most real-world documents.

---

## Roadmap

- [ ] PDF and DOCX file upload support
- [ ] Conversation history / follow-up questions
- [ ] Document management endpoints (list, delete by user)
- [ ] Streaming responses
- [ ] Docker containerization
- [ ] Auth middleware

---

## License

MIT
