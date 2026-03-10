# rag-proj

A collection of production-ready **Retrieval-Augmented Generation (RAG)** system built with Python, LangChain, ChromaDB, and Ollama. Upload any PDF document and query it intelligently using a locally-running LLM — no cloud dependencies, no data leaving your machine.

---

## Overview

Most LLMs hallucinate when asked about documents they've never seen. This project solves that by combining **vector search** with **language generation** — documents are chunked, embedded, and stored locally. When a query comes in, the most relevant chunks are retrieved first, then passed to the LLM as context. The model answers only from what's actually in your documents.

Everything runs locally via Ollama. No OpenAI key required.


## License

MIT License. See `LICENSE` for details.