# Engineering Short & Long Term Agent Memory using MongoDB

A hands-on lab exploring how to build agents that remember — within a session, across sessions, and at scale — using MongoDB as the memory backend.

## What you'll build

| Notebook | Memory type | Key primitive |
|----------|-------------|---------------|
| `01-short-term-memory.ipynb` | Session / Working memory | `MongoDBSaver` (LangGraph checkpointer) |
| `02-long-term-memory.ipynb` | Episodic + Semantic memory | VoyageAI embeddings + `$vectorSearch` |
| `03-semantic-cache.ipynb` | Semantic Cache | VoyageAI embeddings + `$vectorSearch` |

## Concepts covered

```
Short-Term Memory
├── Working memory    — LLM context window
└── Session memory    — LangGraph checkpoints in MongoDB (MongoDBSaver)

Long-Term Memory
├── Episodic          — records of past interactions
├── Semantic          — facts, preferences, entity memory
└── Procedural        — (referenced in slides)

Semantic Cache       — skip the LLM for semantically equivalent queries
```

The full memory pipeline: **Aggregate → Encode → Store → Organise → Retrieve**

## Prerequisites

- [GitHub Codespaces](https://github.com/features/codespaces) (recommended) or Docker + VS Code Dev Containers
- A [VoyageAI API key](https://www.voyageai.com/) — used for embeddings
- An [Anthropic API key](https://console.anthropic.com/) — used for the LLM

## Getting started

1. Open the repo in a Codespace (or Dev Container).
2. Add your secrets in Codespace settings (or a `.env` file for local):
   - `VOYAGE_API_KEY`
   - `ANTHROPIC_API_KEY`
3. Open the `lab/` folder and run the notebooks in order.

The devcontainer automatically starts a local MongoDB Atlas-compatible instance and runs the seed script to populate the listings dataset.

## Stack

- **Runtime:** TypeScript (tslab kernel in Jupyter)
- **LLM:** Claude Haiku via `@langchain/anthropic`
- **Embeddings:** VoyageAI `voyage-4-large` / `voyage-4-lite`
- **Orchestration:** LangGraph (`@langchain/langgraph`)
- **Database:** MongoDB Atlas local (`mongodb/mongodb-atlas-local`)
