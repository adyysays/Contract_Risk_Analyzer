# AI Contract Risk Analyzer Pro

A production-level web application built with **Python** and **Streamlit** for intelligent contract analysis using AI. This tool helps legal professionals and business teams analyze contracts quickly, identify risks, and get actionable recommendations.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

---

## 🌟 Features

### Core Features

1. **Contract Upload & Processing**
   - Support for multiple file formats: PDF, DOCX, TXT, CSV, XLSX
   - Fast document processing with multi-format extraction
   - File size validation (max 50MB)
   - Secure file handling

2. **AI-Powered Contract Summarization**
   - Automated summary generation using Google Gemini API
   - Key terms and conditions extraction
   - Executive-friendly formatting

3. **Advanced Risk Analysis**
   - Intelligent risk detection and scoring (0-10 scale)
   - Risk categorization (Financial, Legal, Operational, Compliance)
   - Explainable AI - understand why clauses are risky
   - Clause rewriting with safer alternatives
   - Risk metrics and distribution analysis

4. **RAG-Based Chatbot**
   - Semantic search using FAISS vector database
   - Real-time Q&A about contract details
   - Context-aware answers based on contract content
   - Chat history tracking

5. **Natural-Inspired Optimization**
   - Genetic Algorithm (DEAP) for weight optimization
   - Feature importance: keyword density, ambiguity, clause length, obligation strength
   - Dynamic risk scoring calibration

6. **Professional Dashboard UI/UX**
   - Modern, intuitive dashboard design
   - Real-time loading indicators
   - Interactive visualizations with Plotly
   - Responsive design
   - Dark/Light mode compatible

---

## 🏗️ Project Structure

```
Contract Risk Analyzer/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and environment variables
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
│
├── modules/                        # Core business logic modules
│   ├── __init__.py
│   ├── file_handler.py            # Multi-format file extraction
│   ├── gemini_client.py           # Google Gemini API client
│   ├── risk_analyzer.py           # Risk analysis engine
│   ├── rag_chatbot.py             # RAG chatbot implementation
│   ├── genetic_optimizer.py       # GA-based weight optimization
│   └── visualizations.py          # Chart and visualization utilities
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── report_utils.py            # Report generation and formatting
│
└── uploaded_files/                # Temporary storage for uploaded documents
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))
- 4GB RAM minimum (8GB recommended)
- 500MB disk space

### Installation

1. **Clone the repository**
```bash
cd "Contract Risk Analyzer"
```

2. **Create Python virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Upload Contract
- Click **"Upload Contract"** in the sidebar
- Select a contract file (PDF, DOCX, TXT, CSV, or XLSX)
- The document will be automatically processed and text extracted

### Step 2: View Summary
- Go to **"Summary"** section
- Click "Generate Summary" to create an AI-powered overview
- Review key terms, obligations, and conditions
- Download or copy the summary

### Step 3: Analyze Risks
- Navigate to **"Risk Analysis"** section
- Click "Analyze Risks" to run comprehensive risk detection
- View risk metrics and distribution charts
- Review detailed risk breakdown with explanations
- See suggested improvements for risky clauses

### Step 4: Chat with Contract
- Open the **"Chatbot"** section
- Ask questions about the contract
- View AI responses with source citations
- Explore sample questions for guidance

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
GEMINI_API_KEY=your_gemini_api_key

# App Configuration
APP_TITLE=AI Contract Risk Analyzer Pro
DEBUG=False
MAX_FILE_SIZE=50  # MB

# GA Configuration
GA_POPULATION_SIZE=50
GA_GENERATIONS=20
GA_MUTATION_RATE=0.1
GA_CROSSOVER_RATE=0.8
```

### Configuration File (config.py)

Key settings in `config.py`:

```python
RISK_CATEGORIES = {
    "High": {"emoji": "🔴", "color": "#FF4444", "threshold": 7},
    "Medium": {"emoji": "🟡", "color": "#FFB800", "threshold": 4},
    "Low": {"emoji": "🟢", "color": "#44FF44", "threshold": 0},
}

CHUNK_SIZE = 1000        # RAG chunk size
CHUNK_OVERLAP = 200      # RAG overlap
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]
```

---

## 🤖 How It Works

### Risk Analysis Engine

1. **Text Extraction**: Multi-format document processing
2. **AI Analysis**: Gemini API analyzes contract clauses
3. **Risk Scoring**: Features extracted:
   - Keyword density
   - Ambiguity level
   - Clause length
   - Obligation strength
   - Negation presence
4. **Risk Categorization**: Clauses classified by risk type
5. **Recommendations**: Safer clause rewording suggested

### RAG Chatbot

1. **Chunking**: Contract text split into overlapping segments
2. **Embeddings**: Simple TF-based embeddings for each chunk
3. **Indexing**: FAISS vector database for fast retrieval
4. **Retrieval**: Top-5 relevant chunks retrieved for queries
5. **Generation**: Gemini API generates answers with context

### Genetic Algorithm Optimization

Optimize risk scoring weights using evolutionary computation:

- **Population**: 50 weight configurations
- **Generations**: 20 iterations
- **Fitness**: MSE between predicted and actual scores
- **Features**: Weighted combination of risk features
- **Output**: Optimized weights for improved accuracy

---

## 📊 Visualization Examples

### Dashboard Metrics
- Overall Risk Score (0-10)
- High/Medium/Low Risk Clause Counts
- Safe Clause Percentage

### Charts
- **Risk Distribution**: Bar chart of risk levels
- **Risk by Category**: Category-wise distribution
- **Risk Scores**: Individual clause scores
- **Risk Heatmap**: Visual risk intensity map

---

## 🎯 API Reference

### FileHandler
```python
from modules.file_handler import FileHandler

# Extract text from any supported format
text = FileHandler.extract_text("contract.pdf")

# Validate file
FileHandler.validate_file("contract.pdf", max_size_mb=50)
```

### GeminiClient
```python
from modules.gemini_client import GeminiClient

client = GeminiClient(api_key="your_key")

# Summarize
summary = client.summarize_contract(text)

# Analyze risks
risks = client.analyze_risks(text)

# Answer questions
answer = client.answer_question(text, question)
```

### RiskAnalyzer
```python
from modules.risk_analyzer import RiskAnalyzer

analyzer = RiskAnalyzer()

# Analyze risks
analysis = analyzer.analyze_risk(risks_data)

# Calculate score
score = analyzer.calculate_risk_score(clause_text)

# Extract features for GA
features = analyzer.extract_risk_features(clause_text)
```

### RAGChatbot
```python
from modules.rag_chatbot import RAGChatbot

chatbot = RAGChatbot(gemini_client)

# Build index
chatbot.build_index(contract_text)

# Answer question
answer, sources = chatbot.answer_question("What are the payment terms?")
```

---

## 🧬 Genetic Algorithm

The GA optimizer fine-tunes risk scoring weights:

```python
from modules.genetic_optimizer import RiskWeightOptimizer

optimizer = RiskWeightOptimizer(
    risk_features_list=features,
    risk_scores_list=scores,
    population_size=50,
    generations=20
)

optimized = optimizer.optimize()
```

**Features Optimized:**
- `keyword_density` - Frequency of risk keywords
- `ambiguity` - Presence of vague language
- `clause_length` - Clause length normalization
- `obligation_strength` - Strong/weak obligation indicators
- `negation_presence` - Negative provisions (e.g., "no liability")

---

## 📦 Dependencies

Core libraries:
- **streamlit** - Web UI framework
- **google-generativeai** - Gemini API client
- **PyMuPDF** - PDF processing
- **python-docx** - DOCX processing
- **pandas** - Data manipulation
- **faiss-cpu** - Vector similarity search
- **deap** - Genetic algorithms
- **plotly** - Interactive visualizations
- **scikit-learn** - ML utilities

See `requirements.txt` for complete dependency list with versions.

---

## 🔒 Security Considerations

1. **API Key Management**
   - Store Gemini API key in `.env` file
   - Never commit `.env` to version control
   - Use environment variables for production

2. **File Handling**
   - Files automatically saved to `uploaded_files/` directory
   - Size limit enforced (50MB default)
   - Supported formats validated

3. **Data Privacy**
   - Contract text sent to Gemini API for analysis
   - No persistent storage of contract content
   - Session-based data handling

4. **Error Handling**
   - Comprehensive logging throughout
   - User-friendly error messages
   - Graceful failure modes

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Create `.env` file with your API key
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Issue: File upload fails
**Solution**: Ensure file is under 50MB and in supported format (PDF, DOCX, TXT, CSV, XLSX)

### Issue: Slow performance
**Solution**: 
- Use smaller contract documents (<100KB)
- Increase system RAM to 8GB+
- Close other applications

### Issue: API errors
**Solution**: 
- Verify Gemini API key is valid
- Check internet connection
- Ensure API quota not exceeded

---

## 📈 Performance Tips

1. **Optimize File Size**: Compress contracts before uploading
2. **Batch Processing**: Process multiple contracts sequentially
3. **Caching**: Session state caches results to avoid reprocessing
4. **RAG Index**: Built once, reused for multiple queries
5. **GA Optimization**: Run during off-peak hours

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional file format support
- Custom risk category definitions
- Multi-language support
- Advanced NLP models
- Custom trained risk models

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👨‍💼 Author & Support

Created as a production-level enterprise tool for contract analysis.

**Features Implemented:**
✅ Multi-format file handling
✅ AI-powered summarization
✅ Risk analysis with explainable AI
✅ RAG-based chatbot
✅ Genetic algorithm optimization
✅ Professional dashboard UI
✅ Error handling & logging
✅ Modular, clean code architecture

---

## 🔗 Resources

- [Google Gemini API Docs](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS Documentation](https://faiss.ai/)
- [DEAP Documentation](https://deap.readthedocs.io/)
- [Plotly Documentation](https://plotly.com/python/)

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error logs in terminal
3. Verify configuration files
4. Ensure all dependencies are installed

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
