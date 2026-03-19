"""
Main Streamlit Application: AI Contract Risk Analyzer Pro
A production-level contract risk analysis tool with RAG chatbot
"""

import streamlit as st
import os
import logging
from pathlib import Path
import json
import tempfile
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import custom modules
from config import (
    GEMINI_API_KEY, APP_TITLE, MAX_FILE_SIZE_MB,
    ALLOWED_EXTENSIONS, UPLOAD_FOLDER
)
from modules.file_handler import FileHandler
from modules.gemini_client import GeminiClient
from modules.risk_analyzer import RiskAnalyzer
from modules.rag_chatbot import RAGChatbot
from modules.genetic_optimizer import RiskWeightOptimizer
from modules.visualizations import Visualizer
from utils.report_utils import ReportGenerator, TextHighlighter, JSONExporter

# Page configuration
st.set_page_config(
    page_title="AI Contract Risk Analyzer Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --success-color: #44FF44;
        --warning-color: #FFB800;
        --danger-color: #FF4444;
    }
    
    /* Typography */
    h1 {
        color: #1f77b4;
        font-size: 2.5rem !important;
        font-weight: 700;
    }
    
    h2 {
        color: #2c3e50;
        font-size: 1.8rem !important;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #34495e;
        font-size: 1.3rem !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #1f77b4;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebarNav"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if "contract_text" not in st.session_state:
        st.session_state.contract_text = ""
    if "contract_name" not in st.session_state:
        st.session_state.contract_name = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "risk_analysis" not in st.session_state:
        st.session_state.risk_analysis = None
    if "insights" not in st.session_state:
        st.session_state.insights = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    if "processing" not in st.session_state:
        st.session_state.processing = False

init_session_state()

# Initialize Gemini client globally
gemini_client = GeminiClient(GEMINI_API_KEY)
risk_analyzer = RiskAnalyzer()

def show_landing_page():
    """Display landing page with introduction and guide"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("⚖️ AI Contract Risk Analyzer Pro")
        st.markdown("""
        ### Professional Contract Risk Analysis Powered by AI
        
        Leverage advanced AI and machine learning to analyze contracts instantly,
        identify risks, and get actionable recommendations.
        """)
    
    with col2:
        st.markdown("### 🎯")  # Visual balance for layout
    
    # Key features section
    st.markdown("---")
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 📄 Multi-Format Upload
        - PDF, DOCX, CSV, XLSX, TXT
        - Fast processing
        - Secure handling
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Smart Analysis
        - AI-powered risk detection
        - 10-point risk scoring
        - Category classification
        """)
    
    with col3:
        st.markdown("""
        ### 💡 Smart Recommendations
        - Clause rewriting
        - Risk mitigation
        - Explainable AI
        """)
    
    with col4:
        st.markdown("""
        ### 💬 AI Chatbot
        - RAG-based Q&A
        - Contract queries
        - Instant answers
        """)
    
    # How to use section
    st.markdown("---")
    st.markdown("## 📋 How to Use")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **Step 1: Upload**
        
        📁 Click the upload button to select your contract file.
        Supported formats: PDF, DOCX, TXT, CSV, XLSX
        """)
    
    with col2:
        st.markdown("""
        **Step 2: Summarize**
        
        📖 View an AI-generated summary of your contract's key terms and conditions.
        """)
    
    with col3:
        st.markdown("""
        **Step 3: Analyze**
        
        ⚠️ Review detailed risk analysis with scores, categories, and recommendations.
        """)
    
    with col4:
        st.markdown("""
        **Step 4: Chat**
        
        💬 Ask questions about your contract using smart AI-powered search.
        """)
    
    st.markdown("---")
    
    # Getting started CTA
    st.markdown("## 🚀 Get Started Now")
    st.markdown("""
    Use the sidebar menu to navigate to different features:
    - **Upload Contract** - Start analyzing a new contract
    - **Summary** - View contract summary and overview
    - **Risk Analysis** - Deep dive into identified risks
    - **Chatbot** - Ask questions about your contract
    """)


def show_upload_page():
    """Display contract upload interface"""
    st.header("📄 Upload Contract")
    
    st.markdown("""
    Upload your contract document to begin analysis. 
    Supported formats: PDF, DOCX, TXT, CSV, XLSX (Max 50MB)
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=[ext.replace(".", "") for ext in ALLOWED_EXTENSIONS],
            help="Upload your contract document"
        )
    
    with col2:
        st.markdown("")
        st.markdown("")
        st.markdown("**File Info:**")
    
    if uploaded_file is not None:
        try:
            file_size = uploaded_file.size / (1024 * 1024)
            
            if file_size > MAX_FILE_SIZE_MB:
                st.error(f"❌ File size exceeds {MAX_FILE_SIZE_MB}MB limit")
                return
            
            # Save uploaded file
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Show file preview info
            with col2:
                st.markdown(f"✓ **File:** {uploaded_file.name}")
                st.markdown(f"✓ **Size:** {file_size:.2f}MB")
                st.markdown(f"✓ **Type:** {Path(uploaded_file.name).suffix.upper()}")
            
            st.success("✅ File uploaded successfully!")
            
            # Extract text
            with st.spinner("🔄 Processing document..."):
                try:
                    contract_text = FileHandler.extract_text(file_path)
                    st.session_state.contract_text = contract_text
                    st.session_state.contract_name = uploaded_file.name
                    
                    st.info(f"✓ Extracted {len(contract_text)} characters from document")
                    
                    # Show preview
                    with st.expander("📋 Preview Document", expanded=False):
                        st.text_area(
                            "Document Preview (first 1000 characters)",
                            value=contract_text[:1000],
                            height=200,
                            disabled=True
                        )
                    
                    # Process button
                    if st.button("🚀 Process Contract", type="primary", use_container_width=True):
                        st.session_state.processing = True
                
                except Exception as e:
                    logger.error(f"Error uploading file: {e}")
                    st.error(f"❌ Error processing file: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error handling upload: {e}")
            st.error(f"❌ Error: {str(e)}")


def show_summary_page():
    """Display contract summary"""
    st.header("📖 Contract Summary")
    
    if not st.session_state.contract_text:
        st.warning("⚠️ No contract uploaded yet. Please upload a contract first.")
        return
    
    # Show contract info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contract", st.session_state.contract_name.split("/")[-1])
    with col2:
        st.metric("Text Length", f"{len(st.session_state.contract_text)} chars")
    with col3:
        st.metric("Words", f"{len(st.session_state.contract_text.split())}")
    
    st.markdown("---")
    
    # Generate summary if not exists
    if not st.session_state.summary:
        if st.button("Generate Summary", type="primary", use_container_width=True):
            with st.spinner("🤖 Generating summary using AI..."):
                try:
                    summary = gemini_client.summarize_contract(st.session_state.contract_text)
                    st.session_state.summary = summary
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")
    
    # Display summary
    if st.session_state.summary:
        st.markdown("### 📝 AI-Generated Summary")
        st.markdown(st.session_state.summary)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Summary"):
                st.success("✓ Summary copied to clipboard!")
        with col2:
            if st.button("↓ Download Summary"):
                st.download_button(
                    label="Download as TXT",
                    data=st.session_state.summary,
                    file_name=f"summary_{st.session_state.contract_name}.txt",
                    mime="text/plain"
                )


def show_risk_analysis_page():
    """Display risk analysis dashboard"""
    st.header("⚠️ Risk Analysis")
    
    if not st.session_state.contract_text:
        st.warning("⚠️ No contract uploaded yet. Please upload a contract first.")
        return
    
    # Analyze risks if not exists
    if st.session_state.risk_analysis is None:
        if st.button("🔍 Analyze Risks", type="primary", use_container_width=True):
            with st.spinner("🤖 Analyzing risks using AI..."):
                try:
                    raw_analysis = gemini_client.analyze_risks(st.session_state.contract_text)
                    analyzed = risk_analyzer.analyze_risk(raw_analysis)
                    st.session_state.risk_analysis = analyzed
                    st.rerun()
                except Exception as e:
                    logger.error(f"Error analyzing risks: {e}")
                    st.error(f"❌ Error analyzing risks: {str(e)}")
    
    # Display risk metrics
    if st.session_state.risk_analysis:
        analysis = st.session_state.risk_analysis
        
        col1, col2, col3, col4 = st.columns(4)
        
        risk_score = analysis.get("overall_risk_score", 0)
        score_color = "#FF4444" if risk_score >= 7 else "#FFB800" if risk_score >= 4 else "#44FF44"
        
        with col1:
            st.metric(
                "🎯 Overall Risk Score",
                f"{risk_score}/10",
                delta=None,
                help="0-10 scale where 10 is highest risk"
            )
        
        with col2:
            st.metric(
                "🔴 High Risk",
                analysis.get("high_risk_count", 0),
                help="Clauses requiring immediate attention"
            )
        
        with col3:
            st.metric(
                "🟡 Medium Risk",
                analysis.get("medium_risk_count", 0),
                help="Clauses requiring review"
            )
        
        with col4:
            st.metric(
                "🟢 Low Risk",
                analysis.get("low_risk_count", 0),
                help="Clauses with minimal risk"
            )
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                Visualizer.create_risk_distribution_chart(analysis),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                Visualizer.create_category_distribution(analysis),
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Risk table
        st.markdown("### 📋 Detailed Risk Analysis")
        
        risks = analysis.get("risks", [])
        
        if risks:
            # Create risk table
            table_data = Visualizer.create_risk_table(risks)
            st.dataframe(table_data, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Detailed risk breakdown
            st.markdown("### 🔍 High-Risk Clauses")
            
            high_risks = [r for r in risks if r.get("score", 0) >= 7]
            
            if high_risks:
                for i, risk in enumerate(high_risks[:5], 1):
                    with st.expander(f"🔴 Clause {i}: {risk.get('category', 'Unknown')} (Score: {risk.get('score', 0)}/10)"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("**Original Clause:**")
                            st.warning(risk.get("clause", ""))
                            
                            st.markdown("**Why It's Risky:**")
                            st.info(risk.get("explanation", ""))
                        
                        with col2:
                            st.markdown("**Suggested Improvement:**")
                            st.success(risk.get("suggested_wording", ""))
                            
                            if st.button(f"📋 Copy", key=f"copy_{i}"):
                                st.success("✓ Copied to clipboard!")
            else:
                st.success("✅ No high-risk clauses found!")
        
        # Get insights
        if st.session_state.insights is None:
            if st.button("💡 Get Business Insights", use_container_width=True):
                with st.spinner("🤖 Generating insights..."):
                    try:
                        insights = gemini_client.generate_insights(st.session_state.contract_text)
                        st.session_state.insights = insights
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error generating insights: {str(e)}")


def show_chatbot_page():
    """Display RAG chatbot interface"""
    st.header("💬 Smart Contract Chatbot")
    
    if not st.session_state.contract_text:
        st.warning("⚠️ No contract uploaded yet. Please upload a contract first.")
        return
    
    # Initialize chatbot if needed
    if st.session_state.chatbot is None:
        with st.spinner("🔄 Initializing RAG index..."):
            try:
                st.session_state.chatbot = RAGChatbot(gemini_client)
                st.session_state.chatbot.build_index(st.session_state.contract_text)
                st.success("✓ Chatbot ready!")
            except Exception as e:
                st.error(f"❌ Error initializing chatbot: {str(e)}")
                return
    
    # Chat interface
    st.markdown("### Ask Questions About Your Contract")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
        st.markdown("---")
    
    # Sample questions
    with st.expander("📚 Sample Questions", expanded=not st.session_state.chat_history):
        sample_questions = st.session_state.chatbot.get_answered_questions(sample_size=5)
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                st.session_state.chat_input = question
                st.rerun()
    
    # Chat input
    user_input = st.chat_input("Ask a question about the contract...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    answer, retrieved_chunks = st.session_state.chatbot.answer_question(user_input)
                    st.markdown(answer)
                    
                    # Add to history
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    
                    # Show sources
                    with st.expander("📚 Sources", expanded=False):
                        for i, (chunk, score) in enumerate(retrieved_chunks, 1):
                            st.markdown(f"**Source {i}** (relevance: {score:.2%})")
                            st.text(chunk[:300] + "..." if len(chunk) > 300 else chunk)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def main():
    """Main application"""
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## ⚖️ Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select a page:",
            ["🏠 Home", "📄 Upload Contract", "📖 Summary", "⚠️ Risk Analysis", "💬 Chatbot"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Sidebar info
        if st.session_state.contract_name:
            st.markdown("### 📊 Current Contract")
            st.info(f"**{st.session_state.contract_name.split('/')[-1]}**")
            
            if st.button("🔄 Reset Analysis", use_container_width=True):
                st.session_state.contract_text = ""
                st.session_state.contract_name = ""
                st.session_state.summary = ""
                st.session_state.risk_analysis = None
                st.session_state.insights = None
                st.session_state.chat_history = []
                st.session_state.chatbot = None
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### ℹ️ About
        AI Contract Risk Analyzer Pro uses advanced AI to analyze contracts,
        identify risks, and provide recommendations.
        
        **Version:** 1.0  
        **Powered by:** Google Gemini & Python
        """)
    
    # Page routing
    if page == "🏠 Home":
        show_landing_page()
    elif page == "📄 Upload Contract":
        show_upload_page()
    elif page == "📖 Summary":
        show_summary_page()
    elif page == "⚠️ Risk Analysis":
        show_risk_analysis_page()
    elif page == "💬 Chatbot":
        show_chatbot_page()


if __name__ == "__main__":
    main()
