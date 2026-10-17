# 🛡️ AI-Guard-Judge

### A RAG-Based AI Safety, Evaluation & Policy Assistant

[![AI-Guard-Judge CI](https://github.com/AnshuVerma22/AI-Guard-Judge/actions/workflows/ci.yml/badge.svg)](https://github.com/AnshuVerma22/AI-Guard-Judge/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)
![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

**AI-Guard-Judge** is an end-to-end Retrieval-Augmented Generation (RAG) application that answers questions using internal company policy documents and evaluates AI responses for relevance, faithfulness, and safety.

Unlike a basic chatbot, the system combines semantic retrieval, context-grounded generation, source attribution, safe rejection of unsupported questions, and automated evaluation.

The project demonstrates practical approaches to building and testing more reliable AI-powered knowledge assistants.

## 🚀 Key Features

- 📚 **Retrieval-Augmented Generation (RAG):** Answer questions using company policy documents.
- 🔎 **Semantic Search:** Retrieve relevant document chunks using vector embeddings.
- 🧠 **LLM-Powered Responses:** Generate answers using the Groq API.
- 📌 **Source Attribution:** Return source document information with responses.
- 🛡️ **Safe Rejection:** Reject unsupported and out-of-scope questions instead of inventing policy information.
- 🚨 **Prompt-Injection Testing:** Evaluate behavior against adversarial instructions.
- 📊 **Automated Evaluation:** Assess relevance, faithfulness, and safety.
- ⚡ **FastAPI REST API:** Expose question-answering and evaluation endpoints.
- 📈 **Streamlit Dashboard:** Visualize evaluation results.
- 🧪 **Automated Testing:** Run evaluation cases through GitHub Actions.
- 📝 **Logging and Reports:** Support debugging and evaluation analysis.
- 🐳 **Docker Support:** Build a containerized API image.

## 🏗️ System Architecture

```text
            Company Policy Documents
                       |
                       v
              Document Ingestion
                       |
                       v
                 Text Chunking
                       |
                       v
              Embedding Generation
                       |
                       v
                   ChromaDB
                       |
                       v
                  User Query
                       |
                       v
               Semantic Retrieval
                       |
                       v
                Relevance Check
                       |
              +--------+--------+
              |                 |
        Relevant Context   Insufficient Context
              |                 |
              v                 v
           Groq LLM         Safe Rejection
              |
              v
       Answer + Source Metadata
              |
              v
       Evaluation Pipeline
              |
              v
      Results / Dashboard / Logs
```

## 🔄 RAG Pipeline

### 1. Document ingestion

Policy documents are loaded from `data/documents/`.

Example documents:

- `leave_policy.txt`
- `expense_policy.txt`
- `security_policy.txt`

### 2. Text chunking

Documents are divided into smaller chunks to improve retrieval.

Current configuration:

| Parameter | Value |
|---|---:|
| Chunk size | 500 characters |
| Chunk overlap | 50 characters |
| Stored vectors in the current local dataset | 13 |

Each chunk retains metadata such as its source filename and chunk ID.

### 3. Embedding generation

The application uses `sentence-transformers/all-MiniLM-L6-v2` through the Hugging Face Transformers library and PyTorch.

The embedding implementation performs mean pooling and L2 normalization to produce vector representations of text.

### 4. Vector storage and retrieval

ChromaDB stores document chunks and their embeddings. When a user asks a question, the retriever searches for semantically similar policy content.

A relevance threshold helps prevent answers from being generated when the retrieved context is insufficient.

### 5. Answer generation

Relevant context is passed to the Groq-hosted language model, configured as `llama-3.1-8b-instant` in the current implementation.

The model is instructed to answer using the available policy context.

### 6. Source attribution and safe rejection

The API returns the answer along with source metadata. If the question cannot be answered from the available policies, the system can return:

```text
I could not find this information in the company policies.
```

This behavior is intended to reduce unsupported claims and policy hallucinations.

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| API framework | FastAPI |
| LLM provider | Groq |
| Language model | Llama 3.1 8B Instant |
| Embedding model | all-MiniLM-L6-v2 |
| ML libraries | Transformers, PyTorch |
| Vector database | ChromaDB |
| Document processing | LangChain Text Splitters |
| Evaluation | Custom evaluation pipeline |
| Dashboard | Streamlit |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Version control | Git and GitHub |

## 📁 Project Structure

```text
AI-Guard-Judge/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── api.py
│   └── services/
│       ├── __init__.py
│       ├── embedding.py
│       ├── ingestion.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── rag.py
│       └── evaluator.py
├── data/
│   └── documents/
│       ├── leave_policy.txt
│       ├── expense_policy.txt
│       └── security_policy.txt
├── dashboard/
│   └── app.py
├── evaluation/
│   └── run_evaluation.py
├── tests/
│   ├── evaluation_cases.json
│   └── test_evaluator.py
├── db/
│   └── chroma/
├── reports/
├── Dockerfile
├── requirements.txt
├── requirements-api.txt
├── .env.example
├── .gitignore
└── README.md
```

The generated vector database and evaluation artifacts may be created locally or during execution, depending on the configured workflow.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or a compatible supported version
- Git
- A Groq API key
- Internet access for downloading the embedding model on the first run

### 1. Clone the repository

```bash
git clone https://github.com/AnshuVerma22/AI-Guard-Judge.git
cd AI-Guard-Judge
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

For the complete project, use the dependency file configured in the repository:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you are setting up only the API, check whether `requirements-api.txt` contains all dependencies required by the API and its RAG pipeline before using it instead.

### 4. Configure environment variables

Create a `.env` file in the repository root.

```env
GROQ_API_KEY=your_groq_api_key
```

Keep your API key private. Never commit `.env` or expose credentials in screenshots, source code, or public logs.

The GitHub Actions workflow should receive required credentials through repository Actions secrets.

### 5. Build the vector database

Run this command from the repository root:

```bash
python -m app.services.vector_store
```

This loads the policy documents, splits them into chunks, generates embeddings, and stores them in ChromaDB.

The first run may take longer because the embedding model needs to be downloaded.

### 6. Start the API

```bash
uvicorn app.api:app --reload
```

Open:

- API base URL: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## 🔌 API Endpoints

### Health check

**`GET /health`**

Checks whether the API is running.

```bash
curl http://127.0.0.1:8000/health
```

Example response, subject to the implementation:

```json
{
  "status": "healthy",
  "service": "AI-Guard-Judge API",
  "version": "1.0.0"
}
```

### Ask a policy question

**`POST /ask`**

Example request:

```json
{
  "question": "How many annual leave days do employees get?"
}
```

Example response:

```json
{
  "question": "How many annual leave days do employees get?",
  "answer": "Employees are entitled to 18 days of paid annual leave per calendar year.",
  "sources": [
    {
      "source": "leave_policy.txt",
      "chunk_id": 0
    }
  ],
  "source_count": 1
}
```

The example illustrates the intended response structure; exact output depends on the current API schema, retrieved context, and generated answer.

### Evaluate the system

**`POST /evaluate`**

Runs the evaluation functionality exposed by the API.

The evaluation suite covers:

- Policy question answering
- Questions without supporting evidence
- Out-of-scope questions
- Prompt-injection and safety scenarios

Consult the interactive Swagger documentation at `/docs` for the exact request schema.

## 🧪 Testing and Evaluation

The project includes an automated evaluation dataset with **14 test cases**.

### Test distribution

| Category | Test cases |
|---|---:|
| RAG / policy questions | 5 |
| No-answer cases | 3 |
| Out-of-scope questions | 3 |
| Prompt-injection cases | 3 |
| **Total** | **14** |

### Run the evaluation tests

Run the pytest suite:

```bash
python -m pytest -v
```

Run the standalone evaluation runner, if configured:

```bash
python -m evaluation.run_evaluation
```

These commands serve different purposes: pytest reports test outcomes, while the standalone runner may generate evaluation reports according to its implementation.

### Evaluation metrics

The current local evaluation run reported all 14 application-level cases as passing, with judge scores of 1.0 for the displayed relevance, faithfulness, and safety metrics.

These are results from the current test dataset and evaluation logic, **not a guarantee of 100% real-world accuracy**. LLM-based judging can miss incomplete answers, and the test suite should be expanded with stronger assertions and additional edge cases.

Important evaluation goals include:

- Correct retrieval of policy evidence
- Answers supported by retrieved context
- Appropriate rejection of unsupported questions
- Robustness against adversarial prompts
- Detection of incomplete or misleading answers

## 📈 Evaluation Dashboard

A Streamlit dashboard is included for reviewing evaluation results.

Start it with:

```bash
streamlit run dashboard/app.py
```

If configured to consume the generated evaluation report, the dashboard can display information such as:

- Pass/fail status
- Test categories
- Relevance and faithfulness scores
- Safety scores
- Evaluation summaries

Ensure the expected report file exists before launching the dashboard.

## 🔐 AI Safety Design

The system follows a simple principle:

> If sufficient supporting evidence is unavailable, the assistant should not fabricate a policy answer.

Its intended behavior separates evidence retrieval from answer generation:

```text
User Question
     |
     v
Semantic Retrieval
     |
     v
Relevant Evidence?
     |
  +--+--+
  |     |
 Yes    No
  |     |
  v     v
 LLM   Reject
  |
  v
Answer + Sources
```

The relevance threshold and safe-rejection behavior provide basic safeguards. They do not guarantee complete protection against prompt injection, incorrect retrieval, or hallucinations, so continued adversarial testing is important.

## 🐳 Docker

Build the Docker image from the repository root:

```bash
docker build -t ai-guard-judge .
```

Run the API:

```bash
docker run --env-file .env -p 8000:8000 ai-guard-judge
```

Then open http://127.0.0.1:8000/docs.

**Deployment note:** Ensure the Docker image includes all required runtime dependencies and that the embedding model can be downloaded or loaded from a configured cache. Persistent ChromaDB storage must be configured if vector data needs to survive container restarts.

## ⚙️ Continuous Integration

The repository uses GitHub Actions to run the CI workflow on pushes and pull requests targeting `main`.

Workflow configuration:

`.github/workflows/ci.yml`

The workflow includes dependency installation, vector database creation, and evaluation execution.

[View workflow runs](https://github.com/AnshuVerma22/AI-Guard-Judge/actions)

The status badge at the top of this README displays the workflow's latest status for the configured branch. A passing CI workflow indicates that the configured checks succeeded; it does not independently prove production readiness.

## 💡 Example Use Cases

- HR and leave policy assistants
- Expense policy question answering
- Internal IT and security knowledge assistants
- Employee self-service helpdesks
- Company-document search applications
- Testing and monitoring RAG application behavior

## 🔮 Future Improvements

- [ ] Expand the evaluation dataset with more adversarial cases
- [ ] Add stricter checks for incomplete policy answers
- [ ] Improve retrieval quality and ranking
- [ ] Add authentication and role-based access control
- [ ] Track evaluation history across runs
- [ ] Improve structured logging and monitoring
- [ ] Optimize embedding model loading and deployment size
- [ ] Add cloud deployment and persistent storage
- [ ] Add stronger source-grounding checks

## 👨‍💻 Author

**Anshu Verma**

B.Sc. Computer Science | M.Sc. Operational Research

Interested in AI/ML engineering, RAG systems, LLM applications, and AI evaluation.

- GitHub: [AnshuVerma22](https://github.com/AnshuVerma22)
- Project: [AI-Guard-Judge](https://github.com/AnshuVerma22/AI-Guard-Judge)

---

## ⭐ Project Summary

AI-Guard-Judge brings together document ingestion, embeddings, semantic retrieval, LLM-based answer generation, source attribution, safe rejection, and automated evaluation in one application.

The goal is not only to build a question-answering assistant, but also to **test how reliably it uses evidence and handles unsupported requests**.
