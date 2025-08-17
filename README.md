# 📚 Research Assistant (LangGraph + Ollama + Web Search + File Uploads)

An AI-powered **research assistant** built with [LangGraph](https://github.com/langchain-ai/langgraph), [Ollama](https://ollama.com/), and [Streamlit](https://streamlit.io/).  
It can:
- ✅ Answer queries with **summarized results**
- ✅ Search the **web** (via Tavily API)
- ✅ Process **PDFs/CSVs** for document-based research
- ✅ Maintain **conversation memory**
- ✅ Run **fully local** with Ollama models like `mistral`, `llama2`, `codellama`

---

## 🚀 Features
- Web Search 🔍 (Tavily API, with refined results)
- Document Upload 📂 (PDF & CSV support)
- Local LLM 🔒 (powered by Ollama)
- Chat Memory 💬 (remembers past Q&A in a session)
- Streamlit UI 🎨 (easy to use, chat-style interface)

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/research-assistant.git
cd research-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install & Run Ollama
Download Ollama: [https://ollama.com/download](https://ollama.com/download)

Pull a model (example: `mistral`):
```bash
ollama pull mistral
```

Verify Ollama is running (default at `http://localhost:11434`):
```bash
ollama run mistral
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
TAVILY_API_KEY=your_api_key_here
```

Get a free Tavily API key: [https://tavily.com](https://tavily.com)

---

## ▶️ Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure
```
research_assistant/
│── agent.py        # Core agent logic (LangGraph + Ollama + Tavily + File ingestion)
│── app.py          # Streamlit UI
│── requirements.txt
│── README.md
│── .env            # API keys (ignored by git)
```

---

## ✨ Example Queries
- "Summarize recent advancements in traffic light prediction systems"
- "Compare fraud detection techniques in finance"
- "What are the key takeaways from my uploaded research paper?"

---

## ⚡ Roadmap
- [ ] Add option to toggle **Web Search ON/OFF**
- [ ] Use vector database (FAISS/Chroma) for **smarter file retrieval**
- [ ] Chat-style UI with **bubbles**
- [ ] Config file to easily **switch models**

---

## 🤝 Contributing
PRs and suggestions welcome! 🎉

---

## 📜 License
MIT License
