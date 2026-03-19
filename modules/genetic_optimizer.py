"""
Genetic Algorithm module for optimizing risk scoring weights
Uses DEAP library for evolutionary optimization
"""

import logging
from typing import Dict, List, Tuple
import numpy as np
from deap import base, creator, tools, algorithms
import random

logger = logging.getLogger(__name__)


class RiskWeightOptimizer:
    """Uses Genetic Algorithm to optimize risk scoring weights"""
    
    def __init__(self, risk_features_list: List[Dict[str, float]], 
                 risk_scores_list: List[float],
                 population_size: int = 50,
                 generations: int = 20):
        """
        Initialize Risk Weight Optimizer
        
        Args:
            risk_features_list: List of feature dictionaries for clauses
            risk_scores_list: Corresponding risk scores (ground truth)
            population_size: GA population size
            generations: Number of generations to evolve
        """
        self.risk_features_list = risk_features_list
        self.risk_scores_list = risk_scores_list
        self.population_size = population_size
        self.generations = generations
        
        # Features to optimize weights for
        self.feature_names = [
            "keyword_density",
            "ambiguity",
            "clause_length",
            "obligation_strength",
            "negation_presence"
        ]
        
        self.best_weights = None
        self.best_fitness = None
    
    def calculate_predicted_score(self, features: Dict[str, float], 
                                  weights: List[float]) -> float:
        """
        Calculate predicted risk score using feature weights
        
        Args:
            features: Feature dictionary
            weights: Weight values for each feature
            
        Returns:
            Predicted risk score (0-10)
        """
        score = 0
        for i, feature_name in enumerate(self.feature_names):
            if feature_name in features and i < len(weights):
                score += features[feature_name] * weights[i]
        
        # Normalize to 0-10 scale
        score = min(10, max(0, score * 3))  # Scale factor
        return score
    
    def fitness_function(self, weights: Tuple[float, ...]) -> Tuple[float,]:
        """
        Calculate fitness of a weight configuration
        Lower MSE = higher fitness
        
        Args:
            weights: Weight values to evaluate
            
        Returns:
            Tuple containing fitness score (for minimization)
        """
        if not self.risk_features_list or not self.risk_scores_list:
            return (float('inf'),)
        
        mse = 0
        for features, actual_score in zip(self.risk_features_list, self.risk_scores_list):
            predicted_score = self.calculate_predicted_score(features, list(weights))
            mse += (predicted_score - actual_score) ** 2
        
        mse = mse / len(self.risk_scores_list)
        
        # Return as tuple for DEAP (minimize MSE)
        return (mse,)
    
    def optimize(self) -> Dict[str, float]:
        """
        Run genetic algorithm to optimize weights
        
        Returns:
            Dictionary of optimized weights
        """
        try:
            # Clear any existing DEAP definitions
            if hasattr(creator, "FitnessMin"):
                del creator.FitnessMin
            if hasattr(creator, "Individual"):
                del creator.Individual
            
            # Define fitness and individual
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize
            creator.create("Individual", list, fitness=creator.FitnessMin)
            
            toolbox = base.Toolbox()
            
            # Attribute generation: weights between 0.5 and 2.5
            toolbox.register("weight", random.uniform, 0.5, 2.5)
            
            # Individual and population
            toolbox.register("individual", tools.initRepeat, creator.Individual,
                           toolbox.weight, n=len(self.feature_names))
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            
            # Genetic operators
            toolbox.register("evaluate", self.fitness_function)
            toolbox.register("mate", tools.cxBlend, alpha=0.5)
            toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
            toolbox.register("select", tools.selTournament, tournsize=3)
            
            # Bounds for weights
            toolbox.decorate("mate", tools.DeltaPenality(
                lambda x: all(0.5 <= xi <= 2.5 for xi in x), (float('inf'),)))
            toolbox.decorate("mutate", tools.DeltaPenality(
                lambda x: all(0.5 <= xi <= 2.5 for xi in x), (float('inf'),)))
            
            # Create initial population
            pop = toolbox.population(n=self.population_size)
            
            # Run algorithm
            pop, logbook = algorithms.eaSimple(
                pop, toolbox,
                cxpb=0.7,  # Crossover probability
                mutpb=0.2,  # Mutation probability
                ngen=self.generations,
                verbose=False
            )
            
            # Get best individual
            best_ind = tools.selBest(pop, k=1)[0]
            self.best_weights = dict(zip(self.feature_names, best_ind))
            self.best_fitness = best_ind.fitness.values[0]
            
            logger.info(f"GA Optimization completed. Best MSE: {self.best_fitness:.4f}")
            
            return self.best_weights
        
        except Exception as e:
            logger.error(f"Error during GA optimization: {e}")
            return {}
    
    def get_optimized_weights_dict(self) -> Dict[str, float]:
        """
        Get optimized weights as dictionary
        
        Returns:
            Dictionary of optimized weights
        """
        if self.best_weights is None:
            return {}
        return self.best_weights.copy()
    
    def get_optimization_report(self) -> str:
        """
        Generate report on optimization results
        
        Returns:
            Formatted report string
        """
        if self.best_weights is None:
            return "Optimization not yet performed."
        
        report = "**Genetic Algorithm Optimization Report**\n\n"
        report += f"Best MSE Achieved: {self.best_fitness:.4f}\n\n"
        report += "Optimized Feature Weights:\n"
        
        for feature, weight in sorted(self.best_weights.items(), 
                                     key=lambda x: x[1], reverse=True):
            report += f"- {feature}: {weight:.3f}\n"
        
        return report


class ClauseOptimizer:
    """Optimizes clause risk scoring using GA-derived weights"""
    
    def __init__(self, risk_analyzer):
        """
        Initialize Clause Optimizer
        
        Args:
            risk_analyzer: RiskAnalyzer instance
        """
        self.risk_analyzer = risk_analyzer
    
    def optimize_clause_weights(self, clauses: List[str], 
                               manual_scores: List[float]) -> Dict[str, float]:
        """
        Optimize clause scoring weights based on manual annotations
        
        Args:
            clauses: List of clause texts
            manual_scores: Manual risk scores for each clause
            
        Returns:
            Optimized weights dictionary
        """
        try:
            # Extract features from clauses
            features_list = []
            for clause in clauses:
                features = self.risk_analyzer.extract_risk_features(clause)
                features_list.append(features)
            
            # Create optimizer
            optimizer = RiskWeightOptimizer(
                risk_features_list=features_list,
                risk_scores_list=manual_scores,
                population_size=50,
                generations=20
            )
            
            # Run optimization
            optimized_weights = optimizer.optimize()
            
            return optimized_weights
        
        except Exception as e:
            logger.error(f"Error optimizing clause weights: {e}")
            return {}
