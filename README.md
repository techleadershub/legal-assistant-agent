# Legal Assistant Agent ⚖️

An advanced RAG (Retrieval-Augmented Generation) system with agent reasoning for legal document analysis. Perfect for students and professionals to understand complex legal documents in plain English.

## 🌐 Live Demo

**Deploy to Streamlit Cloud**: Follow the [Deployment Guide](DEPLOYMENT.md) to deploy your own instance.

## 🌟 Features

### Core Functionality
- **Document Upload & Processing**: Upload PDF legal documents for analysis
- **Intelligent Clause Retrieval**: Find specific clauses using vector search
- **Plain English Summarization**: Convert complex legal language to student-friendly explanations
- **Conversational Memory**: Remember context for follow-up questions
- **Agent Reasoning**: Uses LangGraph ReAct pattern for intelligent decision-making

### Advanced Capabilities
- **Clause Comparison**: Compare different clauses and highlight differences
- **Risk Analysis**: Identify potential risks and obligations
- **Follow-up Suggestions**: Smart suggestions for related questions
- **Multiple Summary Styles**: Student-friendly, executive, bullet-points, technical

## 🏗️ Architecture

```
Legal Assistant Agent
├── LangGraph Agent (ReAct Pattern)
│   ├── Reasoning → Decides what tools to use
│   ├── Retrieval Tool → Searches document chunks
│   ├── Summarizer Tool → Simplifies legal language
│   └── Memory → Maintains conversation context
├── Document Processing Pipeline
│   ├── PDF Text Extraction
│   ├── Clause Identification
│   └── Text Chunking
├── FAISS Vector Store
│   └── Semantic Search & Retrieval
└── Streamlit UI
    ├── Document Upload
    ├── Chat Interface
    └── Conversation History
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API Key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Legal Assistant Agent"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Upload a legal document or try the sample contract
   - Start asking questions!

## 📋 Usage Examples

### Basic Queries
- "What is the termination clause?"
- "What are the payment terms?"
- "Explain the liability section in simple terms"

### Advanced Analysis
- "What are my obligations under this contract?"
- "What risks should I be aware of?"
- "Compare the notice period with termination terms"

### Follow-up Questions
- "Can you simplify that explanation?"
- "What happens if I don't comply?"
- "How does this compare to standard contracts?"

## 🧪 Testing

### Run All Tests
```bash
cd tests
python test_legal_assistant.py
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component functionality
- **End-to-End Tests**: Complete workflow testing

### Sample Test Scenarios
```bash
# Test document processing
python -c "from tests.test_legal_assistant import TestDocumentProcessor; import unittest; unittest.main()"

# Test vector store operations
python -c "from tests.test_legal_assistant import TestVectorStoreManager; import unittest; unittest.main()"

# Test agent reasoning
python -c "from tests.test_legal_assistant import TestLegalAssistantAgent; import unittest; unittest.main()"
```

## 📁 Project Structure

```
Legal Assistant Agent/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── data/
│   ├── sample_docs/               # Sample legal documents
│   └── vectorstore/               # FAISS vector store persistence
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── legal_agent.py         # LangGraph agent implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── retrieval_tool.py      # Document retrieval tool
│   │   └── summarizer_tool.py     # Gemini-based summarization tool
│   ├── memory/
│   │   ├── __init__.py
│   │   └── conversation_memory.py # Conversation context management
│   └── utils/
│       ├── __init__.py
│       ├── document_processor.py  # PDF processing and chunking
│       └── vector_store.py        # FAISS vector store management
└── tests/
    └── test_legal_assistant.py    # Comprehensive test suite
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
GEMINI_MODEL=gemini-2.0-flash-exp
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Customization Options
- **Chunk Size**: Modify `chunk_size` in `DocumentProcessor`
- **Vector Store**: Switch from FAISS to other vector databases
- **LLM Model**: Change Gemini model version
- **Memory Settings**: Adjust `max_turns` and `max_context_tokens`

## 🎯 Demo Scenarios

### For Students
1. Upload a sample employment contract
2. Ask: "What are my rights as an employee?"
3. Follow up: "What notice period do I need to give?"
4. Request: "Explain this in simpler terms"

### For Professionals
1. Upload a service agreement
2. Ask: "What are the liability limitations?"
3. Analyze: "What are the key business risks?"
4. Compare: "How do payment terms compare to industry standards?"

### For Recruiters/Interviews
1. Load sample contract using the demo button
2. Show agent reasoning in action
3. Demonstrate memory with follow-up questions
4. Explain the difference from simple RAG systems

## 🆚 Comparison with Simple RAG

| Feature | Simple RAG | Legal Assistant Agent |
|---------|------------|----------------------|
| **Query Processing** | Direct retrieval | Intelligent reasoning |
| **Tool Selection** | Fixed approach | Dynamic tool selection |
| **Context Awareness** | Limited | Full conversation memory |
| **Response Style** | Generic | Tailored (student, executive, etc.) |
| **Follow-up Handling** | Poor | Excellent with context |
| **Legal Specialization** | None | Clause identification, risk analysis |

## 🚨 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: Google API Key not found
Solution: Ensure .env file exists with valid GOOGLE_API_KEY
```

**2. Import Errors**
```
Error: ModuleNotFoundError
Solution: pip install -r requirements.txt
```

**3. PDF Processing Issues**
```
Error: No text extracted from PDF
Solution: Ensure PDF is text-based, not scanned images
```

**4. Vector Store Errors**
```
Error: FAISS index not found
Solution: Re-upload document to rebuild vector store
```

## 🔮 Future Enhancements

- [ ] Multi-document comparison
- [ ] Contract template generation
- [ ] Export analysis reports
- [ ] Integration with legal databases
- [ ] Mobile-responsive UI
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain**: For the agent framework
- **LangGraph**: For the ReAct pattern implementation
- **Google Gemini**: For the summarization capabilities
- **FAISS**: For efficient vector search
- **Streamlit**: For the user interface

---

**Built with ❤️ for legal education and accessibility**