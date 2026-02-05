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

### Step 2: Run with Docker (Universal & Recommended)
Docker provides the most stable environment for the Clinical Summary RAG Application. It automatically configures the **Endee Vector DB** and all Python dependencies in a consistent Linux container.

1.  **Ensure Docker Desktop is running**: Verify the engine is initialized.
2.  **Launch Full Stack**:
    ```bash
    docker-compose up --build -d
    ```
    - `-d` runs the containers in the background (detached mode).
3.  **Startup Sequence**:
    -   **Endee DB**: High-performance C++ vector engine initializes on port 8080.
    -   **Backend**: FastAPI service handles clinical logic and LLM orchestration (port 8000).
    -   **Frontend**: Streamlit-based healthcare professional dashboard (port 8501).

> [!NOTE]
> **Modern Stack Performance**: This build uses **NumPy 2.2+** and the official **Endee Python SDK**. We have pinned all 30+ dependencies to resolve standard library conflicts, ensuring a stable and repeatable install.

4.  **Access points**:
    -   **Streamlit UI**: [http://localhost:8501](http://localhost:8501)
    -   **Backend Health**: [http://localhost:8000/health](http://localhost:8000/health)
    -   **Endee Health**: [http://localhost:8080/api/v1/health](http://localhost:8080/api/v1/health)

### Step 3: Data Ingestion (One-Time Setup)
Once the containers are running, you need to migrate the patient data from the MongoDB cloud store into your local Endee Vector engine.

```bash
docker exec -it rag-backend python ingest_to_endee.py
```
*This command runs the specialized ingestion script within the backend container to populate the `patient_vectors` index.*

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
-   **Performance**: Built with a C++ core, Endee provides sub-millisecond similarity search, which is critical for real-time clinical decision support.
-   **Production Scalability**: It uses an HNSW (Hierarchical Navigable Small World) index, allowing the system to scale to hundreds of thousands of patient records with industry-leading efficiency.
-   **Full Architectural Control**: Interfacing with Endee allows for explicit tuning of vector dimensions, precision types (e.g., `Float32`, `Int8`), and HNSW parameters ($M$, $ef\_search$).

### Technical Implementation:
The project leverages the **official [Endee Python SDK](https://github.com/EndeeLabs/endee/tree/main/clients/python)** (v0.1.x+) for all vector operations:
1.  **Vectorization**: Patient clinical narratives are converted into 768-dimensional embeddings using the **Bio-ClinicalBERT** transformer model.
2.  **Indexing**: Vectors are stored in the optimized `patient_vectors` index.
3.  **Modern Dependency Management**: The backend is configured to work with **NumPy 2.0+**, aligning with modern Python performance standards and the latest official Endee client requirements.
4.  **Semantic Search**: High-speed similarity matching via HNSW provides sub-millisecond retrieval of historical clinical data.

---

## Evaluation Guidance

> [!TIP]
> **Developer Note on Forking:** This project is designed to showcase the integration of high-performance vector engines in medical AI. As per the evaluation requirements, I have **forked** the official [Endee repository](https://github.com/EndeeLabs/endee) to my personal account:
> 🔗 **[My Endee Fork](https://github.com/rajiv-rane/endee)**

---

---
