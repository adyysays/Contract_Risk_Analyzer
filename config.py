"""
Configuration module for AI Contract Risk Analyzer
Handles all environment variables and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")

# App Configuration
APP_TITLE = os.getenv("APP_TITLE", "AI Contract Risk Analyzer Pro")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE", "50"))

# Risk Analysis Configuration
RISK_CATEGORIES = {
    "High": {"emoji": "🔴", "color": "#FF4444", "threshold": 7},
    "Medium": {"emoji": "🟡", "color": "#FFB800", "threshold": 4},
    "Low": {"emoji": "🟢", "color": "#44FF44", "threshold": 0},
}

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "models/embedding-001"

# Genetic Algorithm Configuration
GA_POPULATION_SIZE = 50
GA_GENERATIONS = 20
GA_MUTATION_RATE = 0.1
GA_CROSSOVER_RATE = 0.8

# File Upload Configuration
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]
UPLOAD_FOLDER = "uploaded_files"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
