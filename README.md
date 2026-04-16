# UDST Policy Chatbot 📚🤖

## Overview
The **UDST Policy Chatbot** is an AI-powered assistant designed to provide quick and accurate answers to questions about **University of Doha for Science & Technology (UDST)** policies. It utilizes **retrieval-augmented generation (RAG)** to fetch relevant policy information and present structured responses.

## Features
- 📜 **Fetch and process university policies** from official UDST web pages.
- 🤖 **AI-powered chatbot** for answering policy-related questions.
- 🔍 **Retrieval-Augmented Generation (RAG)** to enhance accuracy.
- 📄 **Automatic policy retrieval** using FAISS for efficient search.
- 🌐 **Streamlit Web Interface** for an interactive chatbot experience.

---

## Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/NajlaZuhir/UDST-Policy-Chatbot.git
cd UDST-Policy-Chatbot
```

### 2️⃣ Install Dependencies
Ensure you have Python 3.8+ installed. Then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys
Create a `.env` file in the root directory and add:
```
MISTRAL_API_KEY=your_mistral_api_key
```

---

## Usage
### Run the Chatbot
```bash
streamlit run app.py
```

### Ask a Policy Question
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

## Contributing
Feel free to fork this repository, submit issues, or suggest improvements! 🚀



