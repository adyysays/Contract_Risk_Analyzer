"""
Verification Script for AI Contract Risk Analyzer Pro
Run this to verify all dependencies and configuration are correct
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def verify_python_version():
    """Verify Python version"""
    print("✓ Checking Python Version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def verify_env_file():
    """Verify .env file exists"""
    print("✓ Checking .env File...")
    
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
            if "GEMINI_API_KEY" in content and "your_key" not in content.lower():
                print("  ✓ .env file found with API key configured")
                return True
            else:
                print("  ✗ .env file missing GEMINI_API_KEY or contains placeholder")
                return False
    else:
        print("  ✗ .env file not found")
        print("    Run: cp .env.example .env")
        return False

def verify_project_structure():
    """Verify project structure"""
    print("✓ Checking Project Structure...")
    
    required_files = [
        "app.py",
        "config.py",
        "requirements.txt",
        "modules/__init__.py",
        "modules/file_handler.py",
        "modules/gemini_client.py",
        "modules/risk_analyzer.py",
        "modules/rag_chatbot.py",
        "modules/genetic_optimizer.py",
        "modules/visualizations.py",
        "utils/__init__.py",
        "utils/report_utils.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (MISSING)")
            all_exist = False
    
    return all_exist

def verify_dependencies():
    """Verify all dependencies are installed"""
    print("✓ Checking Dependencies...")
    
    required_packages = {
        "streamlit": "Web UI framework",
        "google.generativeai": "Gemini API client",
        "fitz": "PDF processing (PyMuPDF)",
        "docx": "DOCX processing",
        "pandas": "Data manipulation",
        "numpy": "Numerical computing",
        "sklearn": "Machine learning (scikit-learn)",
        "plotly": "Interactive visualizations",
        "faiss": "Vector similarity search",
        "deap": "Genetic algorithms",
    }
    
    missing = []
    
    for package, description in required_packages.items():
        try:
            if package == "fitz":
                import fitz
            elif package == "docx":
                import docx
            elif package == "sklearn":
                import sklearn
            else:
                __import__(package)
            
            print(f"  ✓ {package:20} - {description}")
        except ImportError:
            print(f"  ✗ {package:20} - {description} (MISSING)")
            missing.append(package)
    
    return len(missing) == 0, missing

def verify_imports():
    """Verify custom modules can be imported"""
    print("✓ Checking Custom Modules...")
    
    modules_to_import = [
        ("config", "Configuration"),
        ("modules.file_handler", "File Handler"),
        ("modules.gemini_client", "Gemini Client"),
        ("modules.risk_analyzer", "Risk Analyzer"),
        ("modules.rag_chatbot", "RAG Chatbot"),
        ("modules.genetic_optimizer", "GA Optimizer"),
        ("modules.visualizations", "Visualizations"),
        ("utils.report_utils", "Report Utils"),
    ]
    
    all_ok = True
    
    for module_name, description in modules_to_import:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name:30} - {description}")
        except Exception as e:
            print(f"  ✗ {module_name:30} - {description}")
            print(f"    Error: {str(e)}")
            all_ok = False
    
    return all_ok

def verify_api_key():
    """Verify Gemini API key is configured"""
    print("✓ Checking Gemini API Key...")
    
    try:
        from config import GEMINI_API_KEY
        
        if GEMINI_API_KEY and GEMINI_API_KEY != "":
            key_preview = GEMINI_API_KEY[:20] + "..." if len(GEMINI_API_KEY) > 20 else GEMINI_API_KEY
            print(f"  ✓ API Key configured: {key_preview}")
            return True
        else:
            print("  ✗ API Key is empty")
            return False
    except Exception as e:
        print(f"  ✗ Error reading API Key: {str(e)}")
        return False

def main():
    """Run all verification checks"""
    print_header("AI Contract Risk Analyzer Pro - Verification")
    
    results = {
        "Python Version": verify_python_version(),
        "Project Structure": verify_project_structure(),
        ".env File": verify_env_file(),
        "API Key": verify_api_key(),
    }
    
    deps_ok, missing_deps = verify_dependencies()
    results["Dependencies"] = deps_ok
    
    results["Custom Modules"] = verify_imports()
    
    # Print summary
    print_header("Verification Summary")
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10} - {check}")
        if not passed:
            all_passed = False
    
    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("Run: pip install -r requirements.txt")
    
    print_header("Result")
    
    if all_passed:
        print("✓ ALL CHECKS PASSED!")
        print("\nYour AI Contract Risk Analyzer Pro is ready to use!")
        print("Run: streamlit run app.py")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above and run this script again.")
        print("\nFor help, see:")
        print("  - SETUP.md (detailed setup instructions)")
        print("  - QUICKSTART.md (quick start guide)")
        print("  - README.md (full documentation)")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
