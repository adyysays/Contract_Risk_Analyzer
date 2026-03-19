# Architecture & Design Documentation

## AI Contract Risk Analyzer Pro - System Architecture

This document describes the architecture, design patterns, and technical implementation of the AI Contract Risk Analyzer Pro.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB UI LAYER                        │
│                      (app.py)                                    │
│                                                                   │
│  ┌──────────────┬──────────────┬──────────────┬────────────────┐ │
│  │   Upload     │   Summary    │   Risk Anal. │   Chatbot      │ │
│  │  Contract    │   Page       │   Dashboard  │   Interface    │ │
│  └──────────────┴──────────────┴──────────────┴────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  FILE HANDLER    │ │ GEMINI API       │ │  RAG SYSTEM      │
│  LAYER           │ │  CLIENT          │ │                  │
│                  │ │                  │ │  ┌────────────┐  │
│ • PDF Extract    │ │ • Summarize      │ │  │ Chunking   │  │
│ • DOCX Extract   │ │ • Analyze Risks  │ │  ├────────────┤  │
│ • TXT Extract    │ │ • Generate Text  │ │  │ Embeddings │  │
│ • CSV Extract    │ │ • Answer Q&A     │ │  ├────────────┤  │
│ • XLSX Extract   │ │ • Get Insights   │ │  │ FAISS Index│  │
└──────────────────┘ └──────────────────┘ │  └────────────┘  │
                                            │                  │
                                            │ • Retrieval      │
                                            │ • Q&A Pipeline   │
                                            └──────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              BUSINESS LOGIC & ANALYSIS LAYER                     │
│                                                                   │
│  ┌─────────────────────┬──────────────────┬─────────────────┐   │
│  │  RISK ANALYZER      │ GA OPTIMIZER     │  VISUALIZER     │   │
│  │                     │                  │                 │   │
│  │ • Risk Scoring      │ • Feature Extr.  │ • Charts        │   │
│  │ • Categorization    │ • GA Evolution   │ • Heatmaps      │   │
│  │ • Feature Extract.  │ • Weight Optim.  │ • Distributions │   │
│  │ • Explainability    │                  │ • Tables        │   │
│  └─────────────────────┴──────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA & SESSION LAYER                           │
│                                                                   │
│  • Session State (contract_text, risk_analysis, chat_history)   │
│  • File Storage (uploaded_files/)                               │
│  • Configuration (config.py)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Breakdown

### 1. **app.py** - Main Streamlit Application
The primary user interface orchestrating all other modules.

**Responsibilities:**
- Session state management
- UI rendering (dashboard, pages, components)
- User interaction handling
- Component integration

**Key Functions:**
```python
- init_session_state()      # Initialize session variables
- show_landing_page()        # Home page
- show_upload_page()         # Upload interface
- show_summary_page()        # Summary display
- show_risk_analysis_page()  # Risk dashboard
- show_chatbot_page()        # Chat interface
- main()                     # App entry point
```

---

### 2. **config.py** - Configuration Manager
Centralized configuration and environment variable management.

**Contains:**
- API keys (from .env)
- Application settings
- Risk categorization definitions
- RAG parameters
- GA optimization parameters
- File handling limits

**Purpose:** Single source of truth for all configuration values.

---

### 3. **File Handler Module** (`modules/file_handler.py`)
Handles multi-format document processing.

**Supported Formats:**
- PDF (PyMuPDF)
- DOCX (python-docx)
- TXT (direct read)
- CSV (pandas)
- XLSX (pandas)

**Key Classes:**
```python
FileHandler
├── extract_text_from_pdf()
├── extract_text_from_docx()
├── extract_text_from_txt()
├── extract_text_from_csv()
├── extract_text_from_xlsx()
├── extract_text()           # Router
└── validate_file()          # File validation
```

**Process Flow:**
```
User Upload → File Validation → Format Detection → Text Extraction → Storage
```

---

### 4. **Gemini Client Module** (`modules/gemini_client.py`)
Wrapper for Google Gemini API interactions.

**Key Methods:**
```python
GeminiClient
├── summarize_contract()     # Create summary
├── analyze_risks()          # Extract & analyze risks
├── extract_clauses()        # Find specific clauses
├── answer_question()        # Q&A for RAG
├── rewrite_clause()         # Suggest improvements
└── generate_insights()      # Business analysis
```

**Risk Analysis Output Format:**
```json
{
  "risks": [
    {
      "clause": "original text",
      "category": "Financial",
      "score": 8,
      "explanation": "why risky",
      "suggested_wording": "safer version"
    }
  ]
}
```

---

### 5. **Risk Analyzer Module** (`modules/risk_analyzer.py`)
Analyzes and structures risk data.

**Key Features:**
1. **Risk Scoring Algorithm**
   - Keyword density analysis
   - Ambiguity detection
   - Clause length normalization
   - Obligation strength assessment
   - Negation presence detection

2. **Feature Extraction** (for GA optimization)
   ```python
   features = {
       "keyword_density": 0.15,
       "ambiguity": 0.08,
       "clause_length": 0.45,
       "obligation_strength": 0.22,
       "negation_presence": 0.05
   }
   ```

3. **Risk Categorization**
   - High Risk (score >= 7)
   - Medium Risk (4 <= score < 7)
   - Low Risk (score < 4)

**Key Methods:**
```python
RiskAnalyzer
├── analyze_risk()           # Process raw risk data
├── calculate_risk_score()   # Score calculation
├── extract_risk_features()  # Feature extraction
├── get_risk_level()         # Category determination
├── get_risk_color()         # UI color coding
└── generate_risk_summary()  # Text summary
```

---

### 6. **RAG Chatbot Module** (`modules/rag_chatbot.py`)
Implements Retrieval-Augmented Generation for intelligent Q&A.

**Component Breakdown:**

**TextChunker:**
- Splits contract into overlapping segments
- Configurable chunk size and overlap
- Preserves context between chunks

**SimpleEmbedder:**
- Creates embeddings using TF-based approach
- Vocabulary building from corpus
- Vector normalization

**RAGChatbot:**
```python
RAGChatbot
├── build_index()            # Create FAISS index
├── retrieve_relevant_chunks() # Semantic search
├── answer_question()        # Generate answer
└── get_answered_questions() # Sample questions
```

**RAG Pipeline:**
```
User Query
    ↓
Embed Query
    ↓
Search FAISS Index
    ↓
Retrieve Top-5 Chunks
    ↓
Create Context
    ↓
Gemini API (Generate Answer)
    ↓
Return Answer + Sources
```

---

### 7. **Genetic Algorithm Module** (`modules/genetic_optimizer.py`)
Advanced weight optimization using evolutionary computation.

**Algorithm:**
1. **Population:** 50 weight configurations
2. **Genes:** Risk feature weights
3. **Fitness Function:** Minimize MSE between predicted and actual scores
4. **Evolution:** 20 generations
5. **Operations:** 
   - Crossover (blend parent weights)
   - Mutation (add Gaussian noise)
   - Selection (tournament selection)

**Optimization Process:**
```
Initial Random Weights
    ↓
Evaluate Fitness (MSE)
    ↓
Selection (Best performers)
    ↓
Crossover & Mutation
    ↓
New Generation
    ↓
Repeat 20 times
    ↓
Return Optimized Weights
```

**Output:**
```python
{
    "keyword_density": 1.2,
    "ambiguity": 1.5,
    "clause_length": 0.9,
    "obligation_strength": 1.8,
    "negation_presence": 0.7
}
```

---

### 8. **Visualization Module** (`modules/visualizations.py`)
Creates interactive Plotly charts and visualizations.

**Charts:**
1. **Risk Distribution** - Bar chart of risk levels
2. **Risk Scores Scatter** - Individual clause scores
3. **Category Distribution** - Risks by business category
4. **Risk Heatmap** - Visual risk intensity
5. **Risk Table** - Detailed clause data

**Visualizer Methods:**
```python
Visualizer
├── create_risk_distribution_chart()
├── create_risk_scores_scatter()
├── create_category_distribution()
├── create_risk_heatmap()
├── create_risk_table()
└── create_metrics_summary()
```

---

### 9. **Report Utilities** (`utils/report_utils.py`)
Report generation and formatting utilities.

**Classes:**

**ReportGenerator:**
- JSON report generation
- Text report formatting
- Multi-format export support

**TextHighlighter:**
- HTML highlighting of risky clauses
- Context extraction around clauses

**JSONExporter:**
- Export analysis as JSON
- Include chat history
- Full result archiving

---

## 🔄 Data Flow Diagrams

### Upload & Processing Flow
```
User selects file
    ↓
File validation (size, format)
    ↓
Save to uploaded_files/
    ↓
FileHandler.extract_text()
    ↓
Store in session_state.contract_text
    ↓
Ready for analysis
```

### Risk Analysis Flow
```
User clicks "Analyze Risks"
    ↓
GeminiClient.analyze_risks(contract_text)
    ↓
Gemini API processes contract
    ↓
Returns JSON with risk data
    ↓
RiskAnalyzer.analyze_risk() structures data
    ↓
Calculate metrics and categorize
    ↓
Store in session_state.risk_analysis
    ↓
Visualizer creates charts
    ↓
Display dashboard
```

### RAG Chatbot Flow
```
First load: build_index()
    ↓
Chunk contract text
    ↓
Build vocabulary
    ↓
Create embeddings for chunks
    ↓
Build FAISS L2 index
    ↓
Ready for queries

User asks question
    ↓
Embed question
    ↓
FAISS search (L2 distance)
    ↓
Retrieve top-5 chunks with scores
    ↓
Create context from chunks
    ↓
GeminiClient.answer_question() with context
    ↓
Return answer + source citations
```

---

## 💾 Session State Management

Streamlit session state maintains state across reruns:

```python
st.session_state.contract_text       # Full contract text
st.session_state.contract_name       # File name
st.session_state.summary             # AI summary
st.session_state.risk_analysis       # Risk analysis results
st.session_state.insights            # Business insights
st.session_state.chat_history        # Chat message history
st.session_state.chatbot             # RAGChatbot instance
st.session_state.processing          # Processing flag
```

**Benefits:**
- Avoid reprocessing on reruns
- Persistent data across interactions
- Efficient resource usage

---

## 🔒 Error Handling Strategy

**Three-Level Error Handling:**

1. **File Validation Layer**
   - Size limits enforced
   - Format validation
   - Clear error messages

2. **API Layer**
   - Retry logic for transient failures
   - Graceful fallback for API errors
   - User-friendly error display

3. **Application Layer**
   - Try-except in all major functions
   - Logging for debugging
   - Informative user feedback

**Logging:**
```python
logger = logging.getLogger(__name__)
logger.error("Error message")      # Log errors
logger.info("Info message")        # Log info
```

---

## 🎨 UI/UX Design Principles

### Design Goals
1. **Professional** - SaaS product appearance
2. **Intuitive** - Easy to navigate
3. **Responsive** - Works on different screen sizes
4. **Accessible** - Clear feedback and help
5. **Interactive** - Engaging visualizations

### Key UI Components

**Sidebar Navigation:**
- Clean radio button menu
- Current contract info
- Reset button
- Help documentation links

**Dashboard Metrics:**
- Large, readable numbers
- Color-coded risk levels
- Key statistics at a glance

**Expandable Sections:**
- High-risk clauses in expanders
- Original + improved wording
- Copy button for convenience

**Chart Visualizations:**
- Interactive Plotly charts
- Hover tooltips
- Mobile-friendly sizing

---

## 🚀 Performance Optimization

### Optimization Strategies

1. **Caching**
   - Session state caches results
   - Avoid redundant API calls
   - Reuse embeddings

2. **Chunking**
   - Process large contracts in chunks
   - Reduce memory usage
   - Faster processing

3. **Lazy Loading**
   - Initialize RAG index on demand
   - Load visualizations only when needed
   - Defer expensive computations

4. **Resource Management**
   - Limit API calls
   - Reuse FAISS index
   - Clean up temporary files

### Performance Benchmarks
- File Upload: < 5 seconds for 100KB PDF
- Summarization: ~10 seconds (Gemini API)
- Risk Analysis: ~15 seconds per contract
- Chatbot Query: ~3 seconds with retrieval

---

## 🧪 Testing Strategy

**Unit Testing:**
- Module-level function tests
- Error condition handling
- Edge case validation

**Integration Testing:**
- End-to-end workflows
- Multiple file formats
- API integration

**UI Testing:**
- Streamlit component tests
- Interaction flows
- State management

---

## 📊 Scalability Considerations

### Current Limitations
- Single-user Streamlit instance
- In-memory session state
- Local file storage

### Future Scalability
- Multi-user architecture (Docker + cloud)
- Database backend for persistence
- Asynchronous job queue for long tasks
- Distributed embeddings storage

---

## 🔐 Security Architecture

**Layers:**

1. **API Key Security**
   - Stored in .env (not in code)
   - Environment variable injection
   - No logging of sensitive data

2. **File Handling**
   - Temporary storage in uploaded_files/
   - File type validation
   - Size limits enforced
   - Encrypted storage (optional)

3. **Data Privacy**
   - Contract data not persisted
   - No external logging
   - In-memory session only
   - Optional data retention policies

---

## 📝 Code Quality Standards

**Implemented:**
- ✅ Type hints in all functions
- ✅ Comprehensive docstrings
- ✅ Error handling and logging
- ✅ Modular architecture
- ✅ DRY principles
- ✅ Clear function naming
- ✅ Comments for complex logic

**Follows:**
- PEP 8 style guide
- Python naming conventions
- SOLID principles
- Clean code practices

---

## 🔗 Integration Points

### External Services
1. **Google Gemini API**
   - Summarization
   - Risk analysis
   - Q&A answering
   - Insight generation

### Libraries & Frameworks
1. **Streamlit** - Web UI
2. **PyMuPDF** - PDF processing
3. **python-docx** - DOCX processing
4. **pandas** - Data processing
5. **FAISS** - Vector search
6. **DEAP** - Genetic algorithms
7. **Plotly** - Visualizations
8. **scikit-learn** - ML utilities

---

## 📈 Future Enhancements

**Planned Features:**
- [ ] Custom risk models
- [ ] Multi-language support
- [ ] Advanced NLP models
- [ ] Team collaboration features
- [ ] Report scheduling
- [ ] Clause template library
- [ ] Compliance checking
- [ ] Integration with legal databases

---

**Architecture Version:** 1.0  
**Last Updated:** March 2026  
**Status:** Production Ready ✅
