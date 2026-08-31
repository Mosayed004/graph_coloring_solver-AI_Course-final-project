"""
Backtracking Search Algorithm implementation for the Graph Colouring Problem Solver.
"""

import time
from src.algorithms.base_algorithm import BaseAlgorithm

class BacktrackingAlgorithm(BaseAlgorithm):
    """
    Implementation of the Backtracking Search Algorithm for graph coloring.
    
    This algorithm systematically explores the solution space by trying different
    color assignments for each vertex and backtracking when conflicts arise.
    """
    
    def __init__(self):
        """
        Initialize a new BacktrackingAlgorithm object.
        """
        self.solution = {}
        self.metrics = {
            'execution_time': 0,
            'backtracks': 0,
            'chromatic_number': 0,
            'vertices_colored': 0
        }
        self.max_colors = None
    
    def solve(self, graph, max_colors=None):
        """
        Solve the graph coloring problem for the given graph using backtracking.
        
        Args:
            graph: The graph to color.
            max_colors: Maximum number of colors to use (optional).
            
        Returns:
            bool: True if a valid coloring was found, False otherwise.
        """
        # Reset metrics and solution
        self.solution = {}
        self.metrics = {
            'execution_time': 0,
            'backtracks': 0,
            'chromatic_number': 0,
            'vertices_colored': 0
        }
        
        # If max_colors is not specified, use the number of vertices as an upper bound
        self.max_colors = max_colors if max_colors is not None else graph.vertices
        
        # Reset graph colors
        graph.reset_colors()
        
        # Start timing
        start_time = time.time()
        
        # Start the recursive backtracking
        result = self._color_graph_util(graph, 0)
        
        # End timing
        end_time = time.time()
        self.metrics['execution_time'] = end_time - start_time
        
        if result:
            # Store the solution
            self.solution = graph.colors.copy()
            self.metrics['chromatic_number'] = graph.get_chromatic_number()
            self.metrics['vertices_colored'] = len(self.solution)
        
        return result
    
    def _color_graph_util(self, graph, vertex):
        """
        Utility function for recursive backtracking.
        
        Args:
            graph: The graph being colored.
            vertex: The current vertex to color.
            
        Returns:
            bool: True if coloring is possible, False otherwise.
        """
        # If all vertices are colored, return True
        if vertex == graph.vertices:
            return True
        
        # Try different colors for the current vertex
        for color in range(1, self.max_colors + 1):
            # Check if assignment of color is safe
            if graph.is_safe_color(vertex, color):
                # Assign the color
                graph.assign_color(vertex, color)
                
                # Recur to assign colors to the rest of the vertices
                if self._color_graph_util(graph, vertex + 1):
                    return True
                
                # If assigning color doesn't lead to a solution, backtrack
                graph.colors.pop(vertex, None)
                self.metrics['backtracks'] += 1
        
        # If no color can be assigned, return False
        return False
    
    def get_solution(self):
        """
        Get the solution found by the algorithm.
        
        Returns:
            dict: A mapping of vertices to colors.
        """
        return self.solution
    
    def get_metrics(self):
        """
        Get performance metrics for the algorithm.
        
        Returns:
            dict: A dictionary of performance metrics.
        """
        return self.metrics
