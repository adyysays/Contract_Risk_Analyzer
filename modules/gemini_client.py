"""
Gemini API Client module for AI Contract Risk Analyzer
Handles all interactions with Google Gemini API
"""

import google.generativeai as genai
import logging
import json
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
    
    def summarize_contract(self, text: str) -> str:
        """
        Generate a summary of the contract using Gemini
        
        Args:
            text: Contract text
            
        Returns:
            Contract summary
        """
        try:
            prompt = f"""
            Please provide a comprehensive summary of the following contract. 
            Focus on:
            1. Main parties involved
            2. Key obligations and responsibilities
            3. Payment terms
            4. Termination conditions
            5. Important dates and deadlines
            
            Contract Text:
            {text[:8000]}
            
            Provide a clear, professional summary suitable for executives.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error summarizing contract: {e}")
            raise
    
    def analyze_risks(self, text: str) -> Dict[str, Any]:
        """
        Analyze contract for risks using Gemini
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary containing risk analysis results
        """
        try:
            prompt = f"""
            Analyze the following contract for legal and financial risks.
            For each identified risk, provide:
            1. Risk clause (exact text from contract)
            2. Risk category (Financial, Legal, Operational, Compliance, Other)
            3. Risk score (1-10, where 10 is highest risk)
            4. Explanation (why this clause is risky)
            5. Suggested safer wording
            
            Format your response as a JSON array like this:
            [
                {{
                    "clause": "exact clause text",
                    "category": "Category",
                    "score": 8,
                    "explanation": "why it's risky",
                    "suggested_wording": "safer version"
                }}
            ]
            
            Contract Text:
            {text[:12000]}
            
            Provide only the JSON array, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON from response
            try:
                # Remove markdown code blocks if present
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                
                risks = json.loads(response_text)
                return {"risks": risks, "raw_response": response_text}
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw response for debugging
                logger.warning("Failed to parse JSON response, returning raw text")
                return {"risks": [], "raw_response": response_text, "error": "JSON parsing failed"}
        
        except Exception as e:
            logger.error(f"Error analyzing risks: {e}")
            raise
    
    def extract_clauses(self, text: str, query: str = "") -> List[str]:
        """
        Extract specific clauses from contract
        
        Args:
            text: Contract text
            query: Optional query to find specific clauses
            
        Returns:
            List of extracted clauses
        """
        try:
            if query:
                prompt = f"""
                Find and extract all clauses related to: {query}
                
                Contract Text:
                {text[:8000]}
                
                Provide each clause on a new line, prefixed with "CLAUSE:"
                """
            else:
                prompt = f"""
                Extract the main clauses from this contract.
                Identify clauses such as:
                1. Payment Terms
                2. Termination
                3. Confidentiality
                4. Liability
                5. Dispute Resolution
                6. Warranties
                7. Indemnification
                
                Contract Text:
                {text[:8000]}
                
                Provide each clause on a new line, prefixed with "CLAUSE:"
                """
            
            response = self.model.generate_content(prompt)
            clauses = [line.replace("CLAUSE:", "").strip() 
                      for line in response.text.split("\n") 
                      if "CLAUSE:" in line]
            return clauses
        except Exception as e:
            logger.error(f"Error extracting clauses: {e}")
            raise
    
    def answer_question(self, text: str, question: str, context: str = "") -> str:
        """
        Answer questions about the contract
        
        Args:
            text: Contract text or RAG context
            question: User question
            context: Additional context from RAG
            
        Returns:
            Answer to the question
        """
        try:
            if context:
                prompt = f"""
                Based on the following contract excerpts, answer the user's question.
                
                Contract Context:
                {context[:10000]}
                
                Full Contract (for reference):
                {text[:5000]}
                
                User Question: {question}
                
                Provide a clear, accurate answer based on the contract. If the information 
                is not in the contract, say so clearly.
                """
            else:
                prompt = f"""
                Based on the following contract, answer the user's question.
                
                Contract Text:
                {text[:10000]}
                
                User Question: {question}
                
                Provide a clear, accurate answer based on the contract.
                """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
    
    def rewrite_clause(self, clause: str, improve_type: str = "risk_mitigation") -> str:
        """
        Rewrite a clause to be safer or more favorable
        
        Args:
            clause: Original clause text
            improve_type: Type of improvement (risk_mitigation, clarity, fairness)
            
        Returns:
            Improved clause text
        """
        try:
            if improve_type == "risk_mitigation":
                prompt = f"""
                Rewrite the following contract clause to reduce legal and financial risk 
                while maintaining the essential meaning.
                
                Original Clause:
                {clause}
                
                Provide only the rewritten clause, no explanation.
                """
            elif improve_type == "clarity":
                prompt = f"""
                Rewrite the following contract clause for clarity and simplicity.
                Use plain language while maintaining legal accuracy.
                
                Original Clause:
                {clause}
                
                Provide only the rewritten clause, no explanation.
                """
            else:  # fairness
                prompt = f"""
                Rewrite the following contract clause to be more balanced and fair to both parties.
                
                Original Clause:
                {clause}
                
                Provide only the rewritten clause, no explanation.
                """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error rewriting clause: {e}")
            raise
    
    def generate_insights(self, text: str) -> Dict[str, Any]:
        """
        Generate key insights about the contract
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary containing various insights
        """
        try:
            prompt = f"""
            Analyze this contract and provide key business insights.
            
            Provide insights in the following JSON format:
            {{
                "key_strengths": ["strength 1", "strength 2", ...],
                "key_weaknesses": ["weakness 1", "weakness 2", ...],
                "red_flags": ["flag 1", "flag 2", ...],
                "business_impact": "overall business impact assessment",
                "recommendations": ["recommendation 1", "recommendation 2", ...]
            }}
            
            Contract Text:
            {text[:10000]}
            
            Provide only the JSON object, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            try:
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                
                insights = json.loads(response_text)
                return insights
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON insights response")
                return {
                    "key_strengths": [],
                    "key_weaknesses": [],
                    "red_flags": [],
                    "business_impact": response_text,
                    "recommendations": []
                }
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            raise
