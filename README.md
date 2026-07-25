# BBL RAG Agent

CLI RAG agent that answers questions about US stocks from a local knowledge base.

## Flow

```
                +-------------------+
                |  User query       |
                |  (CLI / REPL)     |
                +---------+---------+
                          |
                          v
                +-------------------+
                |  React agent      |
                |  (LangGraph)      |
                +---------+---------+
                          |
            calls tool    v
        +-------------------+-------------------+
        |                                       |
        v                                       |
+-------------------+                            |
| retrieve_from_kb  |                            |
+---------+---------+                            |
          |                                        |
          v                                        |
+-------------------+                              |
| load_kb()         |                              |
| read + split      |                              |
| paragraphs        |                              |
+---------+---------+                              |
          |                                        |
          v                                        |
+-------------------+                              |
| tokenize +        |                              |
| overlap score,    |                              |
| keep top 3        |                              |
+---------+---------+                              |
          |                                        |
          +-------------------+--------------------+
                              |
                              v
                +-------------------+
                |  Markdown report  |
                |  to user          |
                +-------------------+
```

The right-side path is the react loop - the agent may call the tool again (e.g. once per company) before answering.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env  # then set LITELLM_API_KEY and LITELLM_API_BASE
```

## Usage

```bash
# single query
uv run python main.py "What is Apple's market cap?"

# interactive REPL
uv run python main.py

# debug retrieval ranking
uv run python -m src.tools.retrieval "Apple market cap"
```

## Configuration

Settings come from `.env` (see `.env.example`):

| Var | Default | Purpose |
|-----|---------|---------|
| `LITELLM_API_KEY` | (none) | API key for the LiteLLM proxy |
| `LITELLM_API_BASE` | (none) | Proxy base URL |
| `LITELLM_MODEL` | `openai/glm-5.2` | Model name (must be exposed by the proxy) |
| `KB_PATH` | `knowledge_base.txt` | Path to the KB file |
