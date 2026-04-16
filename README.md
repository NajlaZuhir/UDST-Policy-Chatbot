# UDST Policy Assistant 📚🤖

## Overview
A **Retrieval-Augmented Generation (RAG)** chatbot designed to provide quick and accurate answers to questions about **University of Doha for Science & Technology (UDST)** policies. It fetch relevant policy information and present structured responses.

## Features
- 📜 **Fetch and process university policies** from official UDST web pages.
- 🤖 **AI-powered chatbot** for answering policy-related questions.
- 🔍 **Retrieval-Augmented Generation (RAG)** to enhance accuracy.
- 📄 **Automatic policy retrieval** using FAISS for efficient search.
- 🌐 **Streamlit Web Interface** for an interactive chatbot experience.

---

## Quick Start
### 1️) Clone the Repository

### 2️) Install Dependencies
Ensure you have Python 3.8+ installed. Then run:
```bash
pip install -r requirements.txt
```

### 3️) Set Up API Keys
Create a `.env` file in the root directory and add:
```
MISTRAL_API_KEY=your_mistral_api_key
```

### 4) Run the Chatbot
```bash
streamlit run app.py
```

### 5) Ask a Policy Question
- Example: *"What is the student attendance policy?"*
- The chatbot will return relevant policy details along with official UDST references.

---

## Project Structure
```
📂 UDST-Policy-Chatbot
│-- ⚙️ config.py (Shared constants and policy links)
│-- 📄 policy_data.py (Fetches, cleans, and chunks policy text)
│-- 🧠 rag_engine.py (Embeddings, FAISS index, and answer generation)
│-- 🔁 retriever.py (Compatibility wrapper for older imports)
│-- 🤖 app.py (Streamlit web app for chatbot UI)
│-- 📄 requirements.txt (Dependencies list)
│-- 🔑 .env (Stores Mistral API key - NOT included in repo)
```

---

## Technologies Used
- 📝 **BeautifulSoup & Requests** - Web scraping for policy extraction
- 🧠 **Mistral AI** - Embedding-based retrieval and response generation
- 🔍 **FAISS** - Efficient vector search for policy retrieval
- 🌐 **Streamlit** - Web UI for chatbot interaction

---
LLM RAG Project | 2025




