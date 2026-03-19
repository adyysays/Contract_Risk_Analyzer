"""
Utilities module for AI Contract Risk Analyzer
Helper functions for PDF generation, formatting, etc.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates summary reports for contracts"""
    
    @staticmethod
    def generate_json_report(contract_name: str, 
                           summary: str,
                           risk_analysis: Dict[str, Any],
                           insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a JSON report
        
        Args:
            contract_name: Name of the contract
            summary: Contract summary
            risk_analysis: Risk analysis results
            insights: Business insights
            
        Returns:
            Dictionary containing report data
        """
        report = {
            "metadata": {
                "contract_name": contract_name,
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "summary": summary,
            "risk_analysis": {
                "overall_risk_score": risk_analysis.get("overall_risk_score", 0),
                "high_risk_count": risk_analysis.get("high_risk_count", 0),
                "medium_risk_count": risk_analysis.get("medium_risk_count", 0),
                "low_risk_count": risk_analysis.get("low_risk_count", 0),
                "total_clauses": risk_analysis.get("total_clauses_analyzed", 0),
                "distribution": risk_analysis.get("risk_distribution", {}),
                "top_risks": risk_analysis.get("top_risks", [])[:5]
            },
            "insights": insights,
            "recommendations": insights.get("recommendations", [])
        }
        
        return report
    
    @staticmethod
    def format_report_text(report: Dict[str, Any]) -> str:
        """
        Format report as readable text
        
        Args:
            report: Report dictionary
            
        Returns:
            Formatted text report
        """
        text = f"""
{'='*80}
AI CONTRACT RISK ANALYZER - REPORT
{'='*80}

Generated: {report['metadata']['generated_at']}
Contract: {report['metadata']['contract_name']}

{'='*80}
EXECUTIVE SUMMARY
{'='*80}

{report['summary'][:500]}...

{'='*80}
RISK ANALYSIS SUMMARY
{'='*80}

Overall Risk Score: {report['risk_analysis']['overall_risk_score']}/10

Risk Distribution:
  - High Risk Clauses: {report['risk_analysis']['high_risk_count']}
  - Medium Risk Clauses: {report['risk_analysis']['medium_risk_count']}
  - Low Risk Clauses: {report['risk_analysis']['low_risk_count']}
  - Total Clauses Analyzed: {report['risk_analysis']['total_clauses']}

Top Risk Categories:
"""
        
        # Add top risks
        for i, risk in enumerate(report['risk_analysis']['top_risks'][:5], 1):
            if isinstance(risk, dict):
                text += f"\n{i}. {risk.get('category', 'Unknown')} - Score: {risk.get('score', 0)}/10"
        
        text += f"""

{'='*80}
KEY INSIGHTS
{'='*80}

Strengths:
"""
        
        for strength in report['insights'].get('key_strengths', [])[:3]:
            text += f"\n✓ {strength}"
        
        text += f"\n\nWeaknesses:\n"
        
        for weakness in report['insights'].get('key_weaknesses', [])[:3]:
            text += f"\n✗ {weakness}"
        
        text += f"\n\nRed Flags:\n"
        
        for flag in report['insights'].get('red_flags', [])[:3]:
            text += f"\n⚠ {flag}"
        
        text += f"""

{'='*80}
RECOMMENDATIONS
{'='*80}

"""
        
        for i, rec in enumerate(report['recommendations'][:5], 1):
            text += f"\n{i}. {rec}"
        
        text += f"\n\n{'='*80}\n"
        
        return text


class TextHighlighter:
    """Utility for highlighting risky clauses in text"""
    
    @staticmethod
    def highlight_clauses(text: str, risky_clauses: List[str]) -> str:
        """
        Highlight risky clauses in contract text (for HTML)
        
        Args:
            text: Original contract text
            risky_clauses: List of risky clause texts
            
        Returns:
            HTML with highlighted clauses
        """
        highlighted_text = text
        
        for clause in risky_clauses:
            if clause and len(clause) > 10:  # Only highlight substantial clauses
                highlighted = f'<mark style="background-color: #FFB800;">{clause}</mark>'
                # Escape special regex characters in clause
                import re
                escaped_clause = re.escape(clause)
                highlighted_text = re.sub(escaped_clause, highlighted, highlighted_text)
        
        return highlighted_text
    
    @staticmethod
    def extract_clause_context(text: str, clause: str, context_size: int = 100) -> str:
        """
        Extract clause with surrounding context
        
        Args:
            text: Full contract text
            clause: Clause to find
            context_size: Characters of context on each side
            
        Returns:
            Clause with context
        """
        import re
        pattern = f".{{0,{context_size}}}{re.escape(clause)}.{{0,{context_size}}}"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            return match.group(0)
        return clause


class JSONExporter:
    """Utility for exporting analysis results as JSON"""
    
    @staticmethod
    def export_analysis(contract_name: str,
                       summary: str,
                       risk_analysis: Dict[str, Any],
                       insights: Dict[str, Any],
                       chat_history: List[Dict[str, str]] = None) -> str:
        """
        Export all analysis as JSON string
        
        Args:
            contract_name: Name of contract
            summary: Contract summary
            risk_analysis: Risk analysis results
            insights: Business insights
            chat_history: Chat conversation history
            
        Returns:
            JSON string of all data
        """
        export_data = {
            "contract_name": contract_name,
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "risk_analysis": risk_analysis,
            "insights": insights,
            "chat_history": chat_history or []
        }
        
        return json.dumps(export_data, indent=2, default=str)
