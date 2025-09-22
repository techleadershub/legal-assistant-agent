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

# Premium CSS for Agentic AI Interface
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Premium Header */
.main-header {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    letter-spacing: -0.02em;
}

.main-subtitle {
    font-size: 1.2rem;
    font-weight: 400;
    text-align: center;
    margin-bottom: 3rem;
    color: #64748b;
    opacity: 0.9;
}

/* Premium Section Headers */
.section-header {
    font-size: 1.75rem;
    font-weight: 600;
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
    color: #1e293b;
    position: relative;
    padding-left: 1rem;
}

.section-header::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 2px;
}

/* Premium Chat Messages */
.chat-message {
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.3s ease;
}

.chat-message:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 2rem;
    position: relative;
}

.user-message::before {
    content: '👤';
    position: absolute;
    left: -2.5rem;
    top: 1.5rem;
    font-size: 1.2rem;
}

.assistant-message {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    color: #1e293b;
    margin-right: 2rem;
    border: 1px solid rgba(102, 126, 234, 0.1);
    position: relative;
}

.assistant-message::before {
    content: '🤖';
    position: absolute;
    right: -2.5rem;
    top: 1.5rem;
    font-size: 1.2rem;
}

/* Premium Suggestion Buttons */
.suggestion-button {
    margin: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 0.9rem;
    color: #475569;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.suggestion-button:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* Premium Stats Container */
.stats-container {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1.5rem;
    border-radius: 16px;
    margin: 1.5rem 0;
    border: 1px solid rgba(102, 126, 234, 0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

/* Premium Sidebar */
.css-1d391kg {
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    border-right: 1px solid rgba(102, 126, 234, 0.1);
}

/* Premium Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    font-size: 0.9rem;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Premium File Uploader */
.stFileUploader > div {
    border: 2px dashed #cbd5e1;
    border-radius: 16px;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    transition: all 0.3s ease;
}

.stFileUploader > div:hover {
    border-color: #667eea;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

/* Premium Status Messages */
.stInfo {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
    border: 1px solid #3b82f6 !important;
    color: #1e40af !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1) !important;
}

.stSuccess {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
    border: 1px solid #22c55e !important;
    color: #166534 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(34, 197, 94, 0.1) !important;
}

.stError {
    background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%) !important;
    border: 1px solid #ef4444 !important;
    color: #dc2626 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1) !important;
}

.stWarning {
    background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%) !important;
    border: 1px solid #f59e0b !important;
    color: #d97706 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1) !important;
}

/* Premium Chat Input */
.stChatInput > div {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
}

.stChatInput > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15) !important;
}

/* Premium Text */
.stMarkdown p {
    color: #1e293b !important;
    line-height: 1.6 !important;
}

/* Premium Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

/* Premium Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-message {
    animation: fadeInUp 0.5s ease-out;
}

/* Premium Loading Spinner */
.stSpinner > div {
    border-top-color: #667eea !important;
}

/* Premium Metrics */
.metric-container {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1.5rem;
    border-radius: 16px;
    margin: 1rem 0;
    border: 1px solid rgba(102, 126, 234, 0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 500;
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
            
            # Clear conversation history for new document
            st.session_state.conversation_history = []
            if st.session_state.agent:
                st.session_state.agent.clear_conversation()

            st.success(f"✅ Successfully processed {uploaded_file.name}")
            st.info(f"📊 Created {len(enhanced_docs)} document chunks for analysis")
            st.info("🔄 Conversation history cleared for new document")
            
            # Rerun to update UI immediately
            st.rerun()

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
            
            # Clear conversation history for new document
            st.session_state.conversation_history = []
            if st.session_state.agent:
                st.session_state.agent.clear_conversation()

            st.success("✅ Sample contract loaded successfully!")
            st.info(f"📊 Created {len(enhanced_docs)} document chunks for analysis")
            st.info("🔄 Conversation history cleared for new document")
            
            # Rerun to update UI immediately
            st.rerun()

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

    # Premium Header
    st.markdown('<h1 class="main-header">⚖️ Legal Assistant Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Advanced ReAct Agentic AI System for Intelligent Legal Document Analysis</p>', unsafe_allow_html=True)

    # Premium Sidebar
    with st.sidebar:
        st.markdown("### 🚀 Document Management")

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

        if uploaded_file and uploaded_file.name != st.session_state.current_document:
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
        st.markdown('<h2 class="section-header">🤖 Intelligent Document Analysis</h2>', unsafe_allow_html=True)

        # Display conversation
        display_conversation_history()

        # Status message for user input
        if not (st.session_state.document_processed and st.session_state.agent):
            st.info("Please upload a document and ensure API key is configured to start chatting.")

    with col2:
        st.markdown('<h2 class="section-header">🎯 Smart Suggestions</h2>', unsafe_allow_html=True)

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
        st.markdown("### 🧠 ReAct Agent Capabilities")
        example_queries = [
            "🧠 **Intelligent Analysis:**",
            "- What is the termination clause?",
            "- Explain the liability terms",
            "- What are the payment terms?",
            "",
            "🔍 **Advanced Reasoning:**",
            "- Compare notice vs termination",
            "- What's the difference between...",
            "",
            "🎯 **Contextual Understanding:**",
            "- Explain this in simple terms",
            "- What are my obligations?",
            "- What risks should I know about?"
        ]

        for query in example_queries:
            st.markdown(query)

        # About section
        st.markdown("---")
        st.markdown("### ⚡ Agentic AI Technology")
        st.markdown("""
        **Advanced ReAct Agent Architecture:**
        - **🧠 LangGraph** - Intelligent reasoning & decision making
        - **🔍 FAISS** - Semantic document retrieval
        - **🤖 Gemini API** - Advanced language understanding
        - **💾 Memory** - Contextual conversation awareness
        - **🎯 Multi-Tool** - Orchestrated AI capabilities

        **Beyond Simple RAG - True Agentic Intelligence!**
        """)

    # Chat input - must be outside columns
    if st.session_state.document_processed and st.session_state.agent:
        user_query = st.chat_input("🤖 Ask your intelligent legal assistant...")
        if user_query:
            handle_user_query(user_query)


if __name__ == "__main__":
    main()