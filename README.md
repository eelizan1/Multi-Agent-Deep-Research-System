# Multi-Agent Deep Research System

An end-to-end multi-agent research pipeline that decomposes complex queries into structured subtasks, executes parallel web research using agent tools, and synthesizes results into a polished report.

---

## Overview

This project implements a Deep Research system inspired by modern agentic architectures:

- A **Planner LLM** creates a structured research plan
- A **Task Splitter LLM** converts the plan into structured JSON subtasks
- A **Coordinator Agent** orchestrates execution
- Multiple **Sub-Agents** perform focused research using web tools
- Results are merged into a **final research report**

The system leverages:

- Open LLMs via [Hugging Face Inference Providers](https://huggingface.co/inference-providers)
- Tool-augmented agents via [smolagents](https://github.com/huggingface/smolagents)
- Web search and scraping via [Firecrawl](https://www.firecrawl.dev/)

---

## Architecture

```
User Query
    ↓
Planner LLM
    ↓
Research Plan
    ↓
Task Splitter (Structured JSON)
    ↓
Coordinator Agent
    ↓
Sub-Agents (parallel)
    ↓
Firecrawl (search + scrape)
    ↓
Markdown Reports
    ↓
Final Synthesized Report
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLMs | Hugging Face Inference Providers (e.g. Kimi, GLM, Qwen) |
| Agents | smolagents (`ToolCallingAgent`) |
| Web Tools | Firecrawl (MCP-based search and scraping) |
| Schema Validation | Pydantic |
| Orchestration | Python |
| CLI | Lightweight Python interface |

---

## Features

- Multi-agent orchestration (Coordinator and Sub-agents)
- Structured output using JSON schema
- Automated task decomposition
- Tool-augmented research (search and scrape)
- Markdown report generation
- Modular and extensible pipeline

---

## How It Works

### 1. Generate Research Plan

The planner LLM transforms a user query into a detailed research strategy.

### 2. Split into Subtasks

A second LLM converts the plan into structured JSON:

```json
{
  "subtasks": [
    {
      "id": "example",
      "title": "Example Task",
      "description": "Detailed instructions..."
    }
  ]
}
```

### 3. Execute Sub-Agents

Each subtask is assigned to a specialized agent that:

- Searches the web
- Scrapes relevant sources
- Produces a structured markdown report

### 4. Final Synthesis

The coordinator merges all sub-agent outputs into a single report.

---

## Installation

### Option 1 — Local Setup

```bash
uv init deep-research-agent
uv add 'smolagents[mcp]' firecrawl huggingface_hub
```

Create a `.env` file:

```env
HF_TOKEN=your_huggingface_token
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

### Option 2 — Colab

```bash
pip install 'smolagents[mcp]' firecrawl huggingface_hub
```

---

## Usage

Run the CLI:

```bash
uv run main.py
```

Enter a query:

```
Enter your research query:
> What are the economic impacts of climate change in Europe?
```

Output will be written to:

```
research_result.md
```

---

## Project Structure

```
.
├── main.py                # CLI entrypoint
├── planner.py             # Research plan generation
├── task_splitter.py       # JSON subtask generation
├── coordinator.py         # Agent orchestration
├── prompts.py             # Prompt templates
├── tools/                 # Tool integrations (Firecrawl)
└── research_result.md     # Final output
```

---

## Example Use Cases

- Market research automation
- Competitive intelligence
- Technical deep-dives
- Academic research augmentation
- Due diligence workflows

---

## Planned Improvements

- [ ] Parallel sub-agent execution
- [ ] Retry and fault tolerance
- [ ] Caching search results
- [ ] Human-in-the-loop approval
- [ ] Observability (tracing and logs)
- [ ] Model routing and fallback strategy

---

## References

- [Firecrawl](https://www.firecrawl.dev/)
- [smolagents](https://github.com/huggingface/smolagents)
- [Hugging Face Inference Providers](https://huggingface.co/inference-providers)
- [Anthropic Deep Research System](https://www.anthropic.com/)

---

## Key Concepts

- Agentic AI workflows
- Tool-augmented LLMs
- Structured output (JSON schema)
- Multi-agent orchestration
- Retrieval and synthesis pipelines
