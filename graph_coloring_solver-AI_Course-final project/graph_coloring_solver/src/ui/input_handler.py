"""
Input handler for the Graph Colouring Problem Solver.
"""

class InputHandler:
    """
    A class for handling user input for the Graph Colouring Problem Solver.
    
    This class provides methods to get graph input from users and process
    algorithm parameters.
    """
    
    def __init__(self):
        """
        Initialize a new InputHandler object.
        """
        pass
    
    def parse_graph_from_adjacency_matrix(self, matrix_str):
        """
        Parse a graph from an adjacency matrix string.
        
        Args:
            matrix_str: String representation of adjacency matrix.
            
        Returns:
            dict: Dictionary with vertices and edges.
        """
        lines = matrix_str.strip().split('\n')
        matrix = []
        
        for line in lines:
            row = [int(x) for x in line.strip().split()]
            matrix.append(row)
        
        # Validate matrix dimensions
        n = len(matrix)
        for row in matrix:
            if len(row) != n:
                return None
        
        # Extract vertices and edges
        vertices = n
        edges = []
        
        for i in range(n):
            for j in range(i+1, n):  # Only consider upper triangle
                if matrix[i][j] == 1:
                    edges.append((i, j))
        
        return {
            'vertices': vertices,
            'edges': edges
        }
    
    def parse_graph_from_edge_list(self, edge_list_str):
        """
        Parse a graph from an edge list string.
        
        Args:
            edge_list_str: String representation of edge list.
            
        Returns:
            dict: Dictionary with vertices and edges.
        """
        lines = edge_list_str.strip().split('\n')
        
        # First line should contain the number of vertices
        try:
            vertices = int(lines[0])
        except ValueError:
            return None
        
        edges = []
        
        # Parse edges
        for i in range(1, len(lines)):
            try:
                u, v = map(int, lines[i].strip().split())
                if 0 <= u < vertices and 0 <= v < vertices:
                    edges.append((u, v))
            except ValueError:
                continue
        
        return {
            'vertices': vertices,
            'edges': edges
        }
    
    def validate_algorithm_params(self, algorithm, params):
        """
        Validate algorithm parameters.
        
        Args:
            algorithm: Algorithm name.
            params: Dictionary of parameters.
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if algorithm == 'backtracking':
            # Validate backtracking parameters
            if 'max_colors' in params:
                try:
                    max_colors = int(params['max_colors'])
                    if max_colors <= 0:
                        return False, "Maximum colors must be positive"
                except ValueError:
                    return False, "Maximum colors must be an integer"
            
            return True, ""
            
        elif algorithm == 'genetic':
            # Validate genetic algorithm parameters
            required_params = ['population_size', 'max_generations', 
                              'crossover_rate', 'mutation_rate']
            
            for param in required_params:
                if param not in params:
                    return False, f"Missing parameter: {param}"
            
            try:
                population_size = int(params['population_size'])
                if population_size <= 0:
                    return False, "Population size must be positive"
            except ValueError:
                return False, "Population size must be an integer"
                
            try:
                max_generations = int(params['max_generations'])
                if max_generations <= 0:
                    return False, "Maximum generations must be positive"
            except ValueError:
                return False, "Maximum generations must be an integer"
                
            try:
                crossover_rate = float(params['crossover_rate'])
                if not 0 <= crossover_rate <= 1:
                    return False, "Crossover rate must be between 0 and 1"
            except ValueError:
                return False, "Crossover rate must be a float"
                
            try:
                mutation_rate = float(params['mutation_rate'])
                if not 0 <= mutation_rate <= 1:
                    return False, "Mutation rate must be between 0 and 1"
            except ValueError:
                return False, "Mutation rate must be a float"
            
            return True, ""
            
        else:
            return False, f"Unknown algorithm: {algorithm}"
    
    def get_default_params(self, algorithm):
        """
        Get default parameters for an algorithm.
        
        Args:
            algorithm: Algorithm name.
            
        Returns:
            dict: Dictionary of default parameters.
        """
        if algorithm == 'backtracking':
            return {
                'max_colors': None  # Use maximum possible colors
            }
        elif algorithm == 'genetic':
            return {
                'population_size': 50,
                'max_generations': 100,
                'crossover_rate': 0.8,
                'mutation_rate': 0.2,
                'elite_size': 5
            }
        else:
            return {}
