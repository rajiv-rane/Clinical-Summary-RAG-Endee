# Clinical Summary RAG Application with Endee Vector DB

**Note**: This project has been updated to use [Endee Vector Database](https://github.com/EndeeLabs/endee) for high-performance vector search.

> [!IMPORTANT]
> **Note for Evaluators:** The first time you run this application via Docker, it will take **10-15 minutes** to initialize. This is because Docker must download heavy dependencies (PyTorch, Transformers ~2GB) and the Bio ClinicalBERT medical model (~400MB). 
> **Subsequent launches will take only 10-20 seconds.** Please be patient during the initial `docker-compose up` command.

## Project Overview

The Clinical Summary RAG Application assists healthcare professionals by:
-   **Generating Discharge Summaries**: Automatically creating structured summaries from patient data.
-   **Clinical Decision Support**: Finding similar historical cases using semantic search.
-   **AI Assistant**: Answering clinical queries based on patient context.

### Problem Statement
Manual creation of discharge summaries is time-consuming and prone to error. Clinicians often lack quick access to relevant historical cases that could inform treatment.

### Solution
This application uses a RAG pipeline to:
1.  Ingest patient data and store semantic embeddings in **Endee Vector DB**.
2.  Retrieve relevant cases during query time to provide context.
3.  Use LLMs (via Groq API) to generate accurate, context-aware summaries.

## System Architecture

### Components
1.  **Frontend**: Streamlit UI for interaction.
2.  **Backend**: FastAPI service handling logic, LLM calls, and DB interactions.
3.  **Vector Database**: **Endee** (C++ high-performance engine) for storing and searching patient embeddings.
4.  **Data Store**: MongoDB (Cloud) for storing raw patient records.
5.  **LLM**: Groq API (LlaMA 3 / 4) for generation.
6.  **Embeddings**: Bio ClinicalBERT for medical domain vectorization.

### Technical Architecture
- **Vectors**: 768-dimensional embeddings from Bio ClinicalBERT.
- **Indexing**: Vectors are indexed in Endee `patient_vectors` index using HNSW (Hierarchical Navigable Small World) for fast ANN search.
- **Search**: The backend queries Endee via REST API to get IDs of similar cases, then fetches full patient details from MongoDB.

---

## System Design & Agentic Framework

![System Design Architecture](./assets/system_design.png)

![Agent Workflow Schematic](./assets/agent_workflow.png)

For a detailed breakdown of how the RAG pipeline integrates with **AutoGen** agents and the **Endee** vector engine, please refer to:

-> **[SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md)**

### Design Highlights:
- **Hybrid RAG**: Combines Endee (Vector) and MongoDB (Document) for optimal performance.
- **Agentic Layer**: Uses AutoGen for autonomous clinical review and documentation tasks.
- **Real-time Performance**: Leverages Groq's high-speed inference and Endee's C++ core.

## Setup and Execution

### Prerequisites
-   Docker and Docker Compose installed.
-   Groq API Key.
-   MongoDB URI.

### Step 1: Clone and Configure
1.  Clone the repository:
    ```bash
    git clone https://github.com/rajiv-rane/Clinical-Summary-RAG-Endee.git
    cd Clinical-Summary-RAG-Endee
    ```
2.  Create a `.env` file in the **root directory** (where `docker-compose.yml` is):
    ```env
    GROQ_API_KEY=your_groq_key
    MONGO_URI="mongodb+srv://ishaanroopesh0102:6eShFuC0pNnFFNGm@cluster0.biujjg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    ```
    *(Note: The `MONGO_URI` above is pre-configured and ready for evaluation. You only need to provide your own `GROQ_API_KEY`.)*

### Step 2: Run with Docker (Required for Windows)
Since Endee Vector DB is a high-performance C++ engine built for Linux, we use **Docker** to provide the necessary environment. This is the simplest way to run the full stack on Windows.

1.  **Install Docker Desktop**: Download and install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/). Ensure it is running.
2.  **Launch Services**: Open a terminal in the project root and run:
    ```bash
    docker-compose up --build
    ```
3.  **Startup Sequence**:
    -   **Endee DB**: Starts first and initializes the vector engine.
    -   **Backend**: Waits for Endee to be "healthy" before starting (handles LLM logic).
    -   **Frontend**: Starts last and connects to the Backend.

> [!CAUTION]
> **First Run Warning**: The initial build takes **10-15 minutes** as it downloads PyTorch, Transformers, and the Bio-ClinicalBERT model. **Subsequent starts take less than 20 seconds.**

4.  **Access the Application**:
    -   **Frontend UI**: [http://localhost:8501](http://localhost:8501)
    -   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Endee Health Check**: [http://localhost:8080/api/v1/health](http://localhost:8080/api/v1/health)

### Step 3: Local Development (Manual Setup)

**⚠️ Windows Users**: Endee Vector DB **only runs on Linux or macOS**. To run it on Windows, you **must** use Docker (Step 2) or set it up inside [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install).

If you are on Linux/Mac or WSL:

1.  **Start Endee Vector DB**:
    Follow instructions at [EndeeLabs/endee](https://github.com/EndeeLabs/endee) to build and run the Endee server on port 8080.

2.  **Install Dependencies**:
    ```bash
    cd ingestion-phase
    pip install -r requirements.txt
    ```

3.  **Run Backend**:
    ```bash
    python start_api.py
    ```

4.  **Run Frontend**:
    ```bash
    streamlit run app.py
    ```

### Step 4: Data Ingestion (First Time Setup)
If your Endee database is empty, migrate data from MongoDB:

```bash
# From the root directory
docker exec -it rag-backend python ingest_to_endee.py
```
*Note: This runs the ingestion script inside the already-running backend container.*

## Endee Usage Explanation

The project uses **Endee**—a high-performance, C++ based vector database—to power the semantic search engine. Unlike standard databases, Endee is optimized for extreme low-latency retrieval.

### Why Endee?
-   **Performance**: Written in C++, Endee provides sub-millisecond similarity search, which is critical for real-time clinical decision support.
-   **Efficiency**: It uses an HNSW (Hierarchical Navigable Small World) index, allowing the system to scale to hundreds of thousands of patient records without a linear increase in search time.
-   **Hybrid Persistence**: We store high-dimensional medical vectors in Endee and full patient record JSONs in MongoDB. This separation ensures that memory is used efficiently for search while data remains readable and structured.

### Implementation Logic:
The project uses a custom Python wrapper (`ingestion-phase/endee_client.py`) to interact with Endee's REST API:
1.  **Vectorization**: Patient summaries are converted into 768-dimensional vectors using **Bio ClinicalBERT**.
2.  **Indexing**: Vectors are pushed to Endee's `patient_vectors` index using the MongoDB `unit no` as the unique ID.
3.  **Semantic Search**: When a doctor asks a question, the system embeds the query and sends it to Endee's `/search` endpoint.
4.  **Context Retrieval**: Endee returns the IDs of the most similar historical cases. The backend then fetches the full clinical details from MongoDB to provide the LLM with "Long-term Memory" context.

---

