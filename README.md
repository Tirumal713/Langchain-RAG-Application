# Document Q&A RAG System

A full-stack Retrieval-Augmented Generation (RAG) project for semantic search and question-answering over your own documents. This project uses a FastAPI backend, a Streamlit frontend, Pinecone vector store, and Groq LLM for chat-based Q&A with memory and source citation.

---

## Features
- **Upload** PDFs, PPTXs, Excels for semantic chunking and indexing
- **Ask questions** about your documents, get answers with cited sources
- **Chat memory:** Each conversation is saved and can be revisited
- **Delete chat histories** from the UI
- **Modern UI** with Streamlit
- **FastAPI backend** with endpoints for upload, query, chat history, and more

---

## Folder Structure
```
RAG_TASK/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── pinecone_vectorstore.py # Pinecone integration
├── document_processor.py   # PDF, PPTX, Excel chunking
├── temp/                   # Temporary files
│   ├── chat_history/       # Stores chat session JSONs
│   └── uploads/            # Uploaded documents
├── tmp/                    # Additional temp files
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

---

## Quickstart

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd RAG_TASK
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up Pinecone and Groq
- Add your Pinecone API key/config as `pinecone_config.json` (not tracked by git)
- Add your Groq/OpenAI API key as an environment variable or in your code (do not hardcode in repo)

### 4. Run the backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Visit http://localhost:8000/docs for FastAPI Swagger UI
```

### 5. Run the frontend
```bash
streamlit run app.py
# Visit http://localhost:8501 for the UI
```

---

## API Endpoints (FastAPI)
- `POST /upload`         — Upload and process a document
- `POST /query`          — Ask a question (with optional chat_id for memory)
- `GET /chat-history`    — List all chat sessions
- `GET /chat-history/{chat_id}` — Get specific chat history
- `DELETE /chat-history/{chat_id}` — Delete a chat session

---

## Notes
- The folders `temp/`, `tmp/`, `uploads/`, and `temp/chat_history/` are tracked by git and should exist after cloning.
- Store API keys securely. Do not commit secrets to the repo.
- For best results, use high-quality documents and clear questions.

---

## License
MIT License (add your own if needed)

---

## Credits
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pinecone](https://www.pinecone.io/)
- [Groq](https://groq.com/)
- [OpenAI](https://openai.com/)

---

For issues or contributions, please open a pull request or issue on GitHub.
