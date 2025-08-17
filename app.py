import streamlit as st
from agent import run_agent,process_file   # Import our agent logic

st.title("📚 Research Assistant (LangGraph + Ollama + Web Search + Files + Memory)")

# Maintain memory across session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""
if "file_context" not in st.session_state:
    st.session_state.file_context = ""

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or CSV for research", type=["pdf", "csv"])
if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.file_context = process_file(uploaded_file.name)
    st.success(f"Loaded {uploaded_file.name} for research!")

user_query = st.text_input("Enter your research query:")

if st.button("Ask"):
    if user_query.strip():
        with st.spinner("Researching..."):
            result = run_agent(
                user_query,
                file_context=st.session_state.file_context,
                history=st.session_state.chat_history
            )
            st.subheader("📝 Assistant")
            st.write(result["summary"])
            st.session_state.chat_history = result["chat_history"]
    else:
        st.warning("⚠️ Please enter a query before submitting.")

# Show chat history
if st.session_state.chat_history:
    st.subheader("💬 Conversation History")
    st.text(st.session_state.chat_history)
# This code sets up a simple Streamlit app to interact with the research agent.