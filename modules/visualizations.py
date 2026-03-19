"""
Visualization module for AI Contract Risk Analyzer
Creates charts and visualizations for contract analysis
"""

import logging
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd

logger = logging.getLogger(__name__)


class Visualizer:
    """Creates visualizations for contract analysis"""
    
    @staticmethod
    def create_risk_distribution_chart(risk_analysis: Dict[str, Any]) -> go.Figure:
        """
        Create risk distribution pie/bar chart
        
        Args:
            risk_analysis: Risk analysis results
            
        Returns:
            Plotly figure
        """
        try:
            distribution = risk_analysis.get("risk_distribution", {})
            
            if not distribution or sum(distribution.values()) == 0:
                # Create empty chart
                fig = go.Figure()
                fig.add_annotation(text="No risk data available")
                return fig
            
            colors = {
                "High": "#FF4444",
                "Medium": "#FFB800",
                "Low": "#44FF44"
            }
            
            labels = list(distribution.keys())
            values = list(distribution.values())
            colors_list = [colors.get(label, "#999999") for label in labels]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=labels,
                    y=values,
                    marker=dict(color=colors_list),
                    text=values,
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title="Risk Distribution",
                xaxis_title="Risk Level",
                yaxis_title="Number of Clauses",
                hovermode='x unified',
                template="plotly_white",
                height=400,
                showlegend=False
            )
            
            return fig
        
        except Exception as e:
            logger.error(f"Error creating risk distribution chart: {e}")
            return go.Figure()
    
    @staticmethod
    def create_risk_scores_scatter(risks: List[Dict[str, Any]]) -> go.Figure:
        """
        Create scatter plot of risk scores
        
        Args:
            risks: List of risk dictionaries
            
        Returns:
            Plotly figure
        """
        try:
            if not risks:
                fig = go.Figure()
                fig.add_annotation(text="No risk data available")
                return fig
            
            # Extract data
            clauses = []
            scores = []
            categories = []
            colors_map = {
                "Financial": "#1f77b4",
                "Legal": "#ff7f0e",
                "Operational": "#2ca02c",
                "Compliance": "#d62728",
                "Other": "#9467bd"
            }
            
            for i, risk in enumerate(risks[:20]):  # Limit to first 20
                clauses.append(f"Clause {i+1}")
                scores.append(risk.get("score", 5))
                categories.append(risk.get("category", "Other"))
            
            colors = [colors_map.get(cat, "#999999") for cat in categories]
            
            fig = go.Figure()
            
            for category in set(categories):
                mask = [c == category for c in categories]
                cat_scores = [s for s, m in zip(scores, mask) if m]
                cat_labels = [l for l, m in zip(clauses, mask) if m]
                
                fig.add_trace(go.Scatter(
                    x=cat_labels,
                    y=cat_scores,
                    mode='markers',
                    name=category,
                    marker=dict(
                        size=10,
                        color=colors_map.get(category, "#999999"),
                        opacity=0.8
                    ),
                    hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
                ))
            
            fig.update_layout(
                title="Risk Scores by Clause",
                xaxis_title="Clause",
                yaxis_title="Risk Score (0-10)",
                hovermode='closest',
                template="plotly_white",
                height=400,
                xaxis={'tickangle': 45}
            )
            
            return fig
        
        except Exception as e:
            logger.error(f"Error creating risk scores scatter: {e}")
            return go.Figure()
    
    @staticmethod
    def create_category_distribution(risk_analysis: Dict[str, Any]) -> go.Figure:
        """
        Create risk category distribution chart
        
        Args:
            risk_analysis: Risk analysis results
            
        Returns:
            Plotly figure
        """
        try:
            categories = risk_analysis.get("risk_categories", {})
            
            if not categories:
                fig = go.Figure()
                fig.add_annotation(text="No category data available")
                return fig
            
            category_names = list(categories.keys())
            category_counts = [len(risks) for risks in categories.values()]
            
            colors_list = px.colors.qualitative.Set2
            
            fig = go.Figure(data=[
                go.Bar(
                    x=category_names,
                    y=category_counts,
                    marker=dict(color=colors_list[:len(category_names)]),
                    text=category_counts,
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Clauses: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title="Risk Distribution by Category",
                xaxis_title="Risk Category",
                yaxis_title="Number of Clauses",
                hovermode='x unified',
                template="plotly_white",
                height=400,
                xaxis={'tickangle': 45}
            )
            
            return fig
        
        except Exception as e:
            logger.error(f"Error creating category distribution: {e}")
            return go.Figure()
    
    @staticmethod
    def create_risk_heatmap(risks: List[Dict[str, Any]]) -> go.Figure:
        """
        Create risk heatmap visualization
        
        Args:
            risks: List of risk dictionaries
            
        Returns:
            Plotly figure
        """
        try:
            if not risks:
                fig = go.Figure()
                fig.add_annotation(text="No risk data available")
                return fig
            
            # Create matrix data
            max_clauses = min(len(risks), 15)
            risks_data = risks[:max_clauses]
            
            scores = [r.get("score", 5) for r in risks_data]
            categories = [r.get("category", "Other") for r in risks_data]
            
            # Create a simple heatmap
            z = [[s] for s in scores]
            
            fig = go.Figure(data=go.Heatmap(
                z=z,
                y=[f"Clause {i+1}" for i in range(len(risks_data))],
                x=["Risk Score"],
                colorscale="RdYlGn_r",
                text=scores,
                texttemplate='%{text:.1f}',
                textfont={"size": 10},
                hovertemplate='<b>%{y}</b><br>Score: %{z:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Risk Score Heatmap",
                height=500,
                template="plotly_white"
            )
            
            return fig
        
        except Exception as e:
            logger.error(f"Error creating risk heatmap: {e}")
            return go.Figure()
    
    @staticmethod
    def create_risk_table(risks: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Create a DataFrame of risks for table display
        
        Args:
            risks: List of risk dictionaries
            
        Returns:
            DataFrame for display
        """
        try:
            if not risks:
                return pd.DataFrame(columns=["Clause", "Category", "Score", "Explanation"])
            
            rows = []
            for i, risk in enumerate(risks):
                rows.append({
                    "ID": i + 1,
                    "Clause": risk.get("clause", "")[:100] + "...",
                    "Category": risk.get("category", "Other"),
                    "Score": f"{risk.get('score', 0)}/10",
                    "Explanation": risk.get("explanation", "")[:100] + "...",
                })
            
            return pd.DataFrame(rows)
        
        except Exception as e:
            logger.error(f"Error creating risk table: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def create_metrics_summary(risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create summary metrics for display
        
        Args:
            risk_analysis: Risk analysis results
            
        Returns:
            Dictionary of metrics
        """
        return {
            "overall_risk_score": risk_analysis.get("overall_risk_score", 0),
            "high_risk": risk_analysis.get("high_risk_count", 0),
            "medium_risk": risk_analysis.get("medium_risk_count", 0),
            "low_risk": risk_analysis.get("low_risk_count", 0),
            "total_clauses": risk_analysis.get("total_clauses_analyzed", 0),
        }
