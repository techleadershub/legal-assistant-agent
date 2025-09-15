"""
Legal Assistant Agent - Streamlit Application
An advanced RAG system with agent reasoning for legal document analysis.
"""

import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from typing import List, Optional

# Load environment variables
load_dotenv()

# Import our modules
from src.utils.document_processor import DocumentProcessor, create_sample_contract
from src.utils.vector_store import VectorStoreManager
try:
    from src.agents.legal_agent import LegalAssistantAgent
except ImportError:
    # Fallback to simple agent if LangGraph is not available
    from src.agents.simple_agent import SimpleLegalAgent as LegalAssistantAgent


# Page configuration
st.set_page_config(
    page_title="Legal Assistant Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved contrast
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 2rem;
    color: #1e3a8a;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.section-header {
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #1f2937;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5rem;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-message {
    background-color: #dbeafe;
    border-left: 4px solid #2563eb;
    color: #1e40af;
    font-weight: 500;
}

.assistant-message {
    background-color: #f8fafc;
    border-left: 4px solid #475569;
    color: #334155;
    border: 1px solid #e2e8f0;
}

.suggestion-button {
    margin: 0.25rem;
    padding: 0.5rem 1rem;
    background-color: #ffffff;
    border: 2px solid #3b82f6;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    color: #1e40af;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.suggestion-button:hover {
    background-color: #3b82f6;
    color: #ffffff;
}

.stats-container {
    background-color: #f1f5f9;
    padding: 1rem;
    border-radius: 0.75rem;
    margin: 1rem 0;
    border: 1px solid #cbd5e1;
    color: #334155;
    font-weight: 500;
}

/* Improve general text contrast */
.stMarkdown p {
    color: #1f2937 !important;
}

.stInfo {
    background-color: #eff6ff !important;
    border: 1px solid #3b82f6 !important;
    color: #1e40af !important;
}

.stSuccess {
    background-color: #f0fdf4 !important;
    border: 1px solid #22c55e !important;
    color: #166534 !important;
}

.stError {
    background-color: #fef2f2 !important;
    border: 1px solid #ef4444 !important;
    color: #dc2626 !important;
}

.stWarning {
    background-color: #fffbeb !important;
    border: 1px solid #f59e0b !important;
    color: #d97706 !important;
}

/* Sidebar improvements */
.css-1d391kg {
    background-color: #f8fafc;
}

/* Button improvements */
.stButton > button {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: all 0.2s;
}

.stButton > button:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_vector_store_manager():
    """Get cached vector store manager for better performance."""
    try:
        return VectorStoreManager()
    except Exception as e:
        st.error(f"Error initializing vector store: {str(e)}")
        return None

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "agent" not in st.session_state:
        st.session_state.agent = None

    if "vector_store_manager" not in st.session_state:
        vm = get_vector_store_manager()
        if vm is None:
            st.error("Failed to initialize vector store manager. Please refresh the page.")
            st.stop()
        st.session_state.vector_store_manager = vm

    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "current_document" not in st.session_state:
        st.session_state.current_document = None


def setup_agent():
    """Set up the Legal Assistant Agent with API keys."""
    # Try to get API key from Streamlit secrets first, then environment variables
    google_api_key = None
    
    try:
        # For Streamlit Cloud deployment
        google_api_key = st.secrets.get("GOOGLE_API_KEY")
    except (FileNotFoundError, KeyError):
        # Fallback to environment variables for local development
        google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        st.error("⚠️ Google API Key not found.")
        st.info("💡 **For Streamlit Cloud**: Add GOOGLE_API_KEY to your app's secrets")
        st.info("💡 **For Local Development**: Create a .env file with: GOOGLE_API_KEY=your_api_key_here")
        st.markdown("### 🔑 How to get a Google API Key:")
        st.markdown("""
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a new API key
        3. Add it to your Streamlit Cloud app secrets or .env file
        """)
        return None

    try:
        agent = LegalAssistantAgent(
            google_api_key=google_api_key,
            vector_store_manager=st.session_state.vector_store_manager
        )
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None


def process_document(uploaded_file):
    """Process uploaded PDF document."""
    if uploaded_file is None:
        st.error("No file uploaded.")
        return False
        
    # Check file size (limit to 10MB for cloud deployment)
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        st.error("File too large. Please upload a file smaller than 10MB.")
        return False
        
    with st.spinner("🔄 Processing document..."):
        try:
            processor = DocumentProcessor()

            # Process the PDF with error handling
            try:
                documents = processor.process_pdf(uploaded_file, uploaded_file.name)
                if not documents:
                    st.error("No content could be extracted from the PDF.")
                    return False
            except Exception as pdf_error:
                st.error(f"Error reading PDF: {str(pdf_error)}")
                st.info("Please ensure the PDF is not corrupted and contains readable text.")
                return False

            # Enhance with clause identification
            try:
                enhanced_docs = processor.identify_clauses(documents)
                if not enhanced_docs:
                    st.warning("Document processed but no legal clauses identified.")
                    enhanced_docs = documents  # Use original documents
            except Exception as clause_error:
                st.warning(f"Clause identification failed: {str(clause_error)}")
                enhanced_docs = documents  # Fallback to original documents

            # Add to vector store with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    st.session_state.vector_store_manager.create_vectorstore(enhanced_docs)
                    break
                except Exception as vs_error:
                    if attempt == max_retries - 1:
                        st.error(f"Failed to create vector store: {str(vs_error)}")
                        return False
                    st.warning(f"Vector store creation attempt {attempt + 1} failed, retrying...")

            st.session_state.document_processed = True
            st.session_state.current_document = uploaded_file.name

            st.success(f"✅ Successfully processed {uploaded_file.name}")
            st.info(f"📊 Created {len(enhanced_docs)} document chunks for analysis")

            return True

        except Exception as e:
            st.error(f"❌ Unexpected error processing document: {str(e)}")
            st.info("Please try uploading a different document or refresh the page.")
            return False


def load_sample_document():
    """Load sample contract for demo purposes."""
    with st.spinner("📄 Loading sample contract..."):
        try:
            processor = DocumentProcessor()
            sample_text = create_sample_contract()

            # Create documents from sample text
            documents = processor.split_into_chunks(sample_text, "Sample Professional Services Agreement")
            enhanced_docs = processor.identify_clauses(documents)

            # Add to vector store
            st.session_state.vector_store_manager.create_vectorstore(enhanced_docs)

            st.session_state.document_processed = True
            st.session_state.current_document = "Sample Professional Services Agreement"

            st.success("✅ Sample contract loaded successfully!")
            st.info(f"📊 Created {len(enhanced_docs)} document chunks for analysis")

            return True

        except Exception as e:
            st.error(f"❌ Error loading sample document: {str(e)}")
            return False


def display_conversation_history():
    """Display the conversation history."""
    if not st.session_state.conversation_history:
        st.info("💬 Start a conversation by asking questions about your legal document!")
        return

    for turn in st.session_state.conversation_history:
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {turn['user']}
        </div>
        """, unsafe_allow_html=True)

        # Assistant message
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Legal Assistant:</strong> {turn['agent']}
        </div>
        """, unsafe_allow_html=True)


def handle_user_query(query: str):
    """Handle user query and get agent response."""
    if not query or not query.strip():
        st.warning("Please enter a question.")
        return
        
    if not st.session_state.agent:
        st.error("Agent not initialized. Please check your API key configuration.")
        return

    if not st.session_state.document_processed:
        st.error("Please upload and process a document first.")
        return

    with st.spinner("🤔 Analyzing your question..."):
        try:
            # Add timeout and error handling for API calls
            response = st.session_state.agent.process_query(query.strip())
            
            if not response:
                st.error("No response received. Please try again.")
                return

            # Add to conversation history
            st.session_state.conversation_history.append({
                "user": query,
                "agent": response,
                "timestamp": None
            })

            # Rerun to display new conversation
            st.rerun()

        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                st.error("⚠️ API rate limit reached. Please wait a moment and try again.")
            elif "api" in error_msg.lower():
                st.error(f"⚠️ API Error: {error_msg}")
                st.info("Please check your API key and try again.")
            else:
                st.error(f"Error processing query: {error_msg}")
                st.info("Please try rephrasing your question or refresh the page.")


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">⚖️ Legal Assistant Agent</h1>', unsafe_allow_html=True)
    st.markdown("**Advanced RAG System with Agent Reasoning for Legal Document Analysis**")

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Document Management")

        # API Key status
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            st.success("✅ Google API Key configured")
            if not st.session_state.agent:
                st.session_state.agent = setup_agent()
        else:
            st.error("❌ Google API Key not found")
            st.info("Set GOOGLE_API_KEY in your environment")

        st.markdown("---")

        # Document upload section
        st.markdown("#### Upload Legal Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a legal contract or document for analysis"
        )

        if uploaded_file and uploaded_file != st.session_state.current_document:
            if st.button("📤 Process Document", type="primary"):
                process_document(uploaded_file)

        st.markdown("#### Or Try Sample Document")
        if st.button("📄 Load Sample Contract"):
            load_sample_document()

        st.markdown("---")

        # Document status
        if st.session_state.document_processed:
            st.success(f"📄 Document: {st.session_state.current_document}")

            # Vector store stats
            stats = st.session_state.vector_store_manager.get_stats()
            st.markdown(f"📊 **Document Chunks:** {stats.get('total_documents', 0)}")
        else:
            st.warning("⚠️ No document loaded")

        st.markdown("---")

        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            if st.session_state.agent:
                st.session_state.agent.clear_conversation()
            st.session_state.conversation_history = []
            st.rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h2 class="section-header">💬 Chat with Your Document</h2>', unsafe_allow_html=True)

        # Display conversation
        display_conversation_history()

        # Status message for user input
        if not (st.session_state.document_processed and st.session_state.agent):
            st.info("Please upload a document and ensure API key is configured to start chatting.")

    with col2:
        st.markdown('<h2 class="section-header">💡 Suggested Questions</h2>', unsafe_allow_html=True)

        if st.session_state.document_processed and st.session_state.agent:
            # Get follow-up suggestions
            try:
                suggestions = st.session_state.agent.get_follow_up_suggestions()

                st.markdown("**Common Questions:**")
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggestion_{hash(suggestion)}"):
                        handle_user_query(suggestion)

            except:
                # Default suggestions if agent method fails
                default_suggestions = [
                    "What is the termination clause?",
                    "What are the payment terms?",
                    "What are my obligations?",
                    "What are the liability terms?",
                    "Explain the confidentiality clause",
                ]

                for suggestion in default_suggestions:
                    if st.button(suggestion, key=f"default_{hash(suggestion)}"):
                        handle_user_query(suggestion)

        st.markdown("---")

        # Example queries section
        st.markdown("### 📚 Example Queries")
        example_queries = [
            "📋 **Clause Analysis:**",
            "- What is the termination clause?",
            "- Explain the liability terms",
            "- What are the payment terms?",
            "",
            "🔍 **Comparison:**",
            "- Compare notice vs termination",
            "- What's the difference between...",
            "",
            "📖 **Simplification:**",
            "- Explain this in simple terms",
            "- What are my obligations?",
            "- What risks should I know about?"
        ]

        for query in example_queries:
            st.markdown(query)

        # About section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This Legal Assistant Agent uses:
        - **LangGraph** for agent reasoning (ReAct pattern)
        - **FAISS** for document retrieval
        - **Gemini API** for summarization
        - **Memory** for conversation context

        Perfect for students learning legal documents!
        """)

    # Chat input - must be outside columns
    if st.session_state.document_processed and st.session_state.agent:
        user_query = st.chat_input("Ask me about your legal document...")
        if user_query:
            handle_user_query(user_query)


if __name__ == "__main__":
    main()