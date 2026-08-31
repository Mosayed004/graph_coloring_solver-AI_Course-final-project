"""
Base algorithm interface for the Graph Colouring Problem Solver.
"""

from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    """
    Abstract base class for graph coloring algorithms.
    
    This class defines the interface that all graph coloring algorithms must implement.
    """
    
    @abstractmethod
    def solve(self, graph, max_colors=None):
        """
        Solve the graph coloring problem for the given graph.
        
        Args:
            graph: The graph to color.
            max_colors: Maximum number of colors to use (optional).
            
        Returns:
            bool: True if a valid coloring was found, False otherwise.
        """
        pass
    
    @abstractmethod
    def get_solution(self):
        """
        Get the solution found by the algorithm.
        
        Returns:
            dict: A mapping of vertices to colors.
        """
        pass
    
    @abstractmethod
    def get_metrics(self):
        """
        Get performance metrics for the algorithm.
        
        Returns:
            dict: A dictionary of performance metrics.
        """
        pass
