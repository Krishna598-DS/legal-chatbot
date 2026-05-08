"""
Streamlit UI — Docker-compatible version
Reads API_BASE_URL from environment variable.
In Docker: http://api:8000
In local dev: http://localhost:8000
"""

import os
import time
import requests
import streamlit as st

st.set_page_config(
    page_title="Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Read API URL from environment — works both locally and in Docker
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def check_api_health() -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.json()
    except:
        return None


def get_model_info() -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/model/info", timeout=5)
        return response.json()
    except:
        return None


def ask_question(question: str, temperature: float, max_tokens: int) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "question": question,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"API error {response.status_code}: {response.text}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API. Make sure FastAPI is running."}
    except Exception as e:
        return {"success": False, "error": str(e)}


st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚖️ Legal AI Assistant")
    st.markdown("---")
    st.markdown("### 🔌 API Status")
    health = check_api_health()
    if health:
        st.success("● ONLINE")
        st.caption(f"Environment: {health.get('environment', 'N/A')}")
    else:
        st.error("● OFFLINE")
        st.error(f"Connecting to: {API_BASE_URL}")

    st.markdown("---")
    st.markdown("### 🤖 Model")
    model_info = get_model_info()
    if model_info:
        st.success("Fine-tuned Model Active")
        model_id = model_info.get("model_id", "")
        st.caption(f"`...{model_id[-20:]}`")
        st.markdown("**Capabilities:**")
        for cap in model_info.get("capabilities", []):
            st.caption(f"• {cap}")

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    max_tokens = st.slider("Max Response Length", 100, 1000, 500, 50)

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.session_state.total_questions = 0
        st.rerun()

    st.markdown("---")
    st.caption(f"API: {API_BASE_URL}")
    st.caption("Built with FastAPI + Streamlit")


st.markdown("""
<div class="main-header">
    <h1>⚖️ Legal AI Assistant</h1>
    <p>Powered by a fine-tuned GPT-4o-mini model trained on legal domain data</p>
    <p><small>For informational purposes only — consult a licensed attorney for legal advice</small></p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Questions Asked", st.session_state.total_questions)
with col2:
    st.metric("Tokens Used", st.session_state.total_tokens)
with col3:
    estimated_cost = st.session_state.total_tokens * 0.00000060
    st.metric("Est. Cost", f"${estimated_cost:.4f}")
with col4:
    st.metric("API Status", "🟢 Online" if health else "🔴 Offline")

st.markdown("---")

if not st.session_state.messages:
    st.markdown("### 💡 Try asking:")
    example_cols = st.columns(3)
    examples = [
        "What is a breach of contract?",
        "What should I know before signing an NDA?",
        "What is the difference between void and voidable contracts?",
        "What are my rights if I am wrongfully terminated?",
        "What is intellectual property and how do I protect it?",
        "What is an indemnification clause?"
    ]
    for i, example in enumerate(examples):
        with example_cols[i % 3]:
            if st.button(example, use_container_width=True, key=f"example_{i}"):
                st.session_state.pending_question = example
                st.rerun()

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="⚖️"):
            st.write(message["content"])
            if "metadata" in message:
                meta = message["metadata"]
                cols = st.columns(3)
                with cols[0]:
                    st.caption(f"⏱️ {meta.get('response_time_ms', 0):.0f}ms")
                with cols[1]:
                    st.caption(f"🔤 {meta.get('tokens_used', 0)} tokens")
                with cols[2]:
                    st.caption(f"🤖 Fine-tuned model")

if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Consulting legal knowledge base..."):
            result = ask_question(question, temperature, max_tokens)
        if result["success"]:
            data = result["data"]
            answer = data["answer"]
            st.write(answer)
            cols = st.columns(3)
            with cols[0]:
                st.caption(f"⏱️ {data.get('response_time_ms', 0):.0f}ms")
            with cols[1]:
                st.caption(f"🔤 {data.get('tokens_used', 0)} tokens")
            with cols[2]:
                st.caption(f"🤖 Fine-tuned model")
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "metadata": data
            })
            st.session_state.total_tokens += data.get("tokens_used", 0)
            st.session_state.total_questions += 1
        else:
            st.error(result["error"])
    st.rerun()

if question := st.chat_input("Ask a legal question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.write(question)
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Consulting legal knowledge base..."):
            result = ask_question(question, temperature, max_tokens)
        if result["success"]:
            data = result["data"]
            answer = data["answer"]
            st.write(answer)
            cols = st.columns(3)
            with cols[0]:
                st.caption(f"⏱️ {data.get('response_time_ms', 0):.0f}ms")
            with cols[1]:
                st.caption(f"🔤 {data.get('tokens_used', 0)} tokens")
            with cols[2]:
                st.caption(f"🤖 Fine-tuned model")
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "metadata": data
            })
            st.session_state.total_tokens += data.get("tokens_used", 0)
            st.session_state.total_questions += 1
        else:
            st.error(result["error"])
    st.rerun()
