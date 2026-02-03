# System Design: Clinical Summary RAG with Agentic AI

![System Design Architecture Flow](./assets/system_design.png)

This document outlines the technical architecture of the Clinical Summary RAG Application, integrating high-performance vector retrieval with autonomous AI agents.

## 1. The RAG Pipeline (Retrieval-Augmented Generation)

The RAG framework ensures that every discharge summary is grounded in historical patient context and medical standards stored in the database.

### Workflow:
1.  **Ingestion**: Clinical data is vectorized using **Bio ClinicalBERT** (768 dimensions) and stored in **Endee**.
2.  **Query**: When a doctor requests a summary or case comparison, the query is embedded into the same vector space.
3.  **Endee Retrieval**: The engine performs an HNSW search to find the top-$K$ similar historical cases.
4.  **Data Augmentation**: The system fetches full medical details from **MongoDB** using the IDs returned by Endee.
5.  **LLM Generation**: The Groq LLM receives the current patient data + the retrieved cases as "Context" to generate a precise summary.



---

## 2. Autonomous AI Agent Layer (AutoGen)

![Agent Workflow Schematic](./assets/agent_workflow.png)

The system leverages **AutoGen** to transform the static RAG pipeline into a conversational and autonomous clinical assistant.

### Agent Roles:
-   **User Proxy Agent**: Represents the Doctor, translating natural language queries into system commands.
-   **Medical Specialist Agent**: Focuses on analyzing historical cases retrieved from Endee to find patterns.
-   **Documentation Agent**: Specifically tuned to structure generating discharge summaries following hospital guidelines.

### Agent Collaboration:
When a complex query is received (e.g., "Review this patient against similar cases and identify potential complications"), the agents collaborate:
1.  **Specialist Agent** requests the RAG engine for similar cases.
2.  **Specialist Agent** analyzes the differences in recovery times or symptoms.
3.  **Documentation Agent** compiles these findings into a structured note for the Doctor.


---

## 3. Key Performance Enhancements

-   **Endee Vector DB**: C++ based engine provides sub-millisecond similarity search, critical for real-time clinical workflows.
-   **Hybrid Storage**: Separation of vectors (Endee) and large clinical JSONs (MongoDB) ensures memory efficiency.
-   **Groq Inference**: Extremely high token-per-second (TPS) throughput ensures zero-lag conversational experiences with the AI Agents.

---

## 4. Design Decisions

### The Evolution: From Custom Wrapper to Official SDK
A key part of this project's development was the evolution of the vector database interface:

1.  **Phase 1: Deep-Dive Foundations (Custom Client)**
    Initially, I implemented a custom `EndeeClient` using pure REST API calls and `MsgPack` serialization. This was a deliberate learning choice to master the fundamentals of how high-performance vector databases handle data transmission and HNSW indexing.
2.  **Phase 2: Production Readiness (Official SDK Integration)**
    After mastering the fundamentals, I migrated the entire pipeline to the **official Endee Python SDK (`endee>=0.1.8`)**. This transition was aimed at ensuring production reliability, leveraging built-in **Upsert idempotency**, and aligning the project with official feature updates.

### Why Endee?
Unlike standard databases, Endee's **C++ core** and **specialized vector storage** enable the sub-millisecond retrieval required for medical doctors who need information instantly. By decoupling the vector search (Endee) from document storage (MongoDB), the architecture remains lightweight, scalable, and extremely fast.

---
