"""
Risk Analyzer module for AI Contract Risk Analyzer
Analyzes contract risks and provides detailed risk metrics
"""

import logging
import json
import re
from typing import Dict, List, Tuple, Any
from collections import Counter
import numpy as np

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """Analyzes contract risks and generates risk metrics"""
    
    # Risk scoring weights (can be optimized by genetic algorithm)
    DEFAULT_WEIGHTS = {
        "liability": 2.0,
        "limitation": 1.8,
        "indemnification": 1.9,
        "termination": 1.5,
        "force_majeure": 1.2,
        "confidentiality": 1.6,
        "warranty": 1.7,
        "penalty": 2.0,
        "arbitration": 1.3,
        "assignment": 1.4,
    }
    
    RISK_KEYWORDS = {
        "liability": ["liability", "liable", "liable for", "be responsible", "responsible for"],
        "limitation": ["limitation", "limited to", "limit liability", "except", "excludes"],
        "indemnification": ["indemnify", "indemnification", "hold harmless", "defend"],
        "termination": ["terminate", "termination", "cancel", "cancellation", "end this"],
        "force_majeure": ["force majeure", "act of god", "unforeseeable", "beyond control"],
        "confidentiality": ["confidential", "confidentiality", "proprietary", "secret", "non-disclosure"],
        "warranty": ["warrant", "warranty", "guarantee", "guaranteed", "assured"],
        "penalty": ["penalty", "penalize", "fine", "breach", "violation"],
        "arbitration": ["arbitration", "arbitrate", "dispute", "resolved", "waive"],
        "assignment": ["assign", "assignment", "re-assign", "subcontract", "delegate"],
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize Risk Analyzer
        
        Args:
            weights: Optional custom weights for risk scoring
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
    
    def analyze_risk(self, risks_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and structure risk data from Gemini API response
        
        Args:
            risks_data: Risk analysis from Gemini API
            
        Returns:
            Structured risk analysis with metrics
        """
        try:
            risks = risks_data.get("risks", [])
            
            if not risks:
                # Return empty analysis if no risks found
                return {
                    "overall_risk_score": 0,
                    "high_risk_count": 0,
                    "medium_risk_count": 0,
                    "low_risk_count": 0,
                    "risks": [],
                    "risk_distribution": {"High": 0, "Medium": 0, "Low": 0},
                    "top_risks": [],
                    "risk_categories": {}
                }
            
            # Ensure risks are proper dicts
            processed_risks = []
            for risk in risks:
                if isinstance(risk, str):
                    continue
                if isinstance(risk, dict):
                    processed_risks.append(risk)
            
            if not processed_risks:
                return {
                    "overall_risk_score": 0,
                    "high_risk_count": 0,
                    "medium_risk_count": 0,
                    "low_risk_count": 0,
                    "risks": [],
                    "risk_distribution": {"High": 0, "Medium": 0, "Low": 0},
                    "top_risks": [],
                    "risk_categories": {}
                }
            
            # Calculate metrics
            scores = [risk.get("score", 5) for risk in processed_risks]
            overall_score = np.mean(scores) if scores else 0
            
            # Categorize risks
            high_count = sum(1 for r in processed_risks if r.get("score", 5) >= 7)
            medium_count = sum(1 for r in processed_risks if 4 <= r.get("score", 5) < 7)
            low_count = sum(1 for r in processed_risks if r.get("score", 5) < 4)
            
            # Get top risks
            top_risks = sorted(processed_risks, key=lambda x: x.get("score", 0), reverse=True)[:5]
            
            # Categorize by type
            risk_categories = {}
            for risk in processed_risks:
                category = risk.get("category", "Other")
                if category not in risk_categories:
                    risk_categories[category] = []
                risk_categories[category].append(risk)
            
            return {
                "overall_risk_score": round(overall_score, 2),
                "high_risk_count": high_count,
                "medium_risk_count": medium_count,
                "low_risk_count": low_count,
                "total_clauses_analyzed": len(processed_risks),
                "risks": processed_risks,
                "risk_distribution": {
                    "High": high_count,
                    "Medium": medium_count,
                    "Low": low_count
                },
                "top_risks": top_risks,
                "risk_categories": risk_categories
            }
        except Exception as e:
            logger.error(f"Error analyzing risk: {e}")
            raise
    
    def calculate_risk_score(self, clause_text: str) -> float:
        """
        Calculate risk score for a clause based on keywords and patterns
        
        Args:
            clause_text: Text of the clause
            
        Returns:
            Risk score (0-10)
        """
        score = 0
        clause_lower = clause_text.lower()
        
        # Count keyword matches
        for category, keywords in self.RISK_KEYWORDS.items():
            weight = self.weights.get(category, 1.0)
            for keyword in keywords:
                count = clause_lower.count(keyword)
                score += count * weight * 0.5
        
        # Analyze clause characteristics
        # Long clauses tend to be riskier
        word_count = len(clause_text.split())
        if word_count > 200:
            score += 1
        elif word_count > 100:
            score += 0.5
        
        # Check for ambiguous language
        ambiguous_words = ["may", "should", "might", "could", "possibly", "subject to"]
        ambiguous_count = sum(clause_lower.count(word) for word in ambiguous_words)
        score += ambiguous_count * 0.3
        
        # Check for strong obligation language
        obligation_words = ["shall", "must", "required", "must comply", "required to"]
        obligation_count = sum(clause_lower.count(word) for word in obligation_words)
        score += obligation_count * 0.5
        
        # Normalize score to 0-10 scale
        score = min(10, max(0, score))
        return round(score, 2)
    
    def extract_risk_features(self, clause_text: str) -> Dict[str, float]:
        """
        Extract risk features from a clause for genetic algorithm optimization
        
        Args:
            clause_text: Text of the clause
            
        Returns:
            Dictionary of risk features
        """
        features = {}
        clause_lower = clause_text.lower()
        
        # Feature 1: Keyword density
        keyword_count = 0
        for keywords in self.RISK_KEYWORDS.values():
            for keyword in keywords:
                keyword_count += clause_lower.count(keyword)
        
        word_count = len(clause_text.split())
        features["keyword_density"] = keyword_count / max(word_count, 1)
        
        # Feature 2: Ambiguity score
        ambiguous_words = ["may", "should", "might", "could", "possibly", "subject to"]
        ambiguous_count = sum(clause_lower.count(word) for word in ambiguous_words)
        features["ambiguity"] = ambiguous_count / max(word_count, 1)
        
        # Feature 3: Clause length (normalized)
        features["clause_length"] = min(word_count / 200, 1.0)
        
        # Feature 4: Obligation strength
        obligation_words = ["shall", "must", "required", "must comply"]
        obligation_count = sum(clause_lower.count(word) for word in obligation_words)
        features["obligation_strength"] = obligation_count / max(word_count, 1)
        
        # Feature 5: Negation presence (e.g., "not responsible", "no liability")
        negation_count = clause_lower.count("not ") + clause_lower.count("no ")
        features["negation_presence"] = negation_count / max(word_count, 1)
        
        return features
    
    def get_risk_level(self, score: float) -> str:
        """
        Get risk level based on score
        
        Args:
            score: Risk score (0-10)
            
        Returns:
            Risk level (High, Medium, Low)
        """
        if score >= 7:
            return "High"
        elif score >= 4:
            return "Medium"
        else:
            return "Low"
    
    def get_risk_color(self, score: float) -> str:
        """
        Get color for risk visualization
        
        Args:
            score: Risk score (0-10)
            
        Returns:
            Hex color code
        """
        if score >= 7:
            return "#FF4444"  # Red
        elif score >= 4:
            return "#FFB800"  # Orange
        else:
            return "#44FF44"  # Green
    
    def generate_risk_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a text summary of risk analysis
        
        Args:
            analysis: Risk analysis results
            
        Returns:
            Summary text
        """
        overall_score = analysis.get("overall_risk_score", 0)
        high_count = analysis.get("high_risk_count", 0)
        medium_count = analysis.get("medium_risk_count", 0)
        total = analysis.get("total_clauses_analyzed", 0)
        
        summary = f"""
        **Risk Analysis Summary**
        
        Overall Risk Score: {overall_score}/10
        Total Clauses Analyzed: {total}
        
        Risk Distribution:
        - High Risk Clauses: {high_count}
        - Medium Risk Clauses: {medium_count}
        - Low Risk Clauses: {analysis.get('low_risk_count', 0)}
        
        """
        
        if high_count > 0:
            summary += f"\n⚠️ **Important:** Found {high_count} high-risk clause(s) that require immediate attention.\n"
        
        return summary.strip()
