---
name: rag-and-embeddings
description: Managing vector databases, dense embeddings, and LangChain/LangGraph pipelines.
effort_level: High
required_tools: LangChain, ChromaDB / Pinecone
triggers: ["LangChain", "vector databases", "chunking", "context window"]
---
# Skill: RAG, Embeddings & LangChain

## Overview
To provide the swarm with context, we rely on LangChain abstractions and dense vector embeddings.

## Strict Rules
1. **Use LangChain:** Do not write custom document loaders or splitters unless absolutely necessary. Rely on `langchain_community.document_loaders`.
2. **Token Economy:** Implement rigorous chunking strategies (e.g., `RecursiveCharacterTextSplitter`). LLM context windows are large, but filling them with garbage ruins reasoning and burns tokens.
3. **Vector DB:** Use lightweight, local-first vector databases like ChromaDB for development, but ensure the abstraction allows swapping to Pinecone or managed solutions for V3.
