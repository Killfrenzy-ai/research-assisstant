from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

# PDF/CSV support
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Define state schema
class ResearchState(TypedDict):
    query: str
    search_results: str
    file_context: str
    summary: str
    chat_history: str

# Define LLM
llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

# Initialize Web Search Tool
search_tool = TavilySearchResults(max_results=3)

# Define graph
graph = StateGraph(ResearchState)

# Node 1: Web Search (with source refinement)
def search(state: ResearchState):
    query = state["query"]
    results = search_tool.invoke(query)   # list of dicts
    refined_sources = "\n".join(
        [f"- {r['title']}: {r['content']}" for r in results]
    )
    return {"search_results": refined_sources}

# Node 2: File Context Loader
def load_file(state: ResearchState):
    file_context = state.get("file_context", "")
    return {"file_context": file_context}

# Node 3: Summarize with context + memory
def summarize(state: ResearchState):
    query = state["query"]
    sources = state.get("search_results", "")
    file_data = state.get("file_context", "")
    history = state.get("chat_history", "")

    prompt = f"""
    You are a research assistant. Use the following info to answer clearly.

    Conversation history:
    {history}

    User query: {query}

    Relevant web sources:
    {sources}

    Relevant file data:
    {file_data}

    Summarize the key findings for the user.
    """
    response = llm.invoke(prompt)
    return {
        "summary": response.content,
        "chat_history": history + f"\nUser: {query}\nAssistant: {response.content}"
    }

# Add nodes
graph.add_node("search", search)
graph.add_node("file_loader", load_file)
graph.add_node("summarizer", summarize)

# Flow: query → search + file → summarizer
graph.set_entry_point("search")
graph.add_edge("search", "file_loader")
graph.add_edge("file_loader", "summarizer")
graph.set_finish_point("summarizer")

# Compile graph
app = graph.compile()

# Expose helper function
def run_agent(query: str, file_context: str = "", history: str = "") -> dict:
    result = app.invoke({
        "query": query,
        "file_context": file_context,
        "chat_history": history
    })
    return {"summary": result["summary"], "chat_history": result["chat_history"]}


# Utility: process uploaded files (PDF or CSV)
def process_file(file_path: str) -> str:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    else:
        return ""

    docs = loader.load()
    chunks = text_splitter.split_documents(docs)
    return "\n".join([c.page_content for c in chunks[:5]])  # limit to first few chunks
