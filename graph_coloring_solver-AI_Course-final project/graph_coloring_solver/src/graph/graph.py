"""
Graph class implementation for the Graph Colouring Problem Solver.
"""

class Graph:
    """
    A class representing a graph for the Graph Colouring Problem.
    
    Attributes:
        vertices (int): Number of vertices in the graph.
        adjacency_list (dict): Dictionary representing the adjacency list of the graph.
        colors (dict): Dictionary mapping vertices to their assigned colors.
    """
    
    def __init__(self, vertices=0):
        """
        Initialize a new Graph object.
        
        Args:
            vertices (int): Number of vertices in the graph.
        """
        self.vertices = vertices
        self.adjacency_list = {i: [] for i in range(vertices)}
        self.colors = {}
    
    def add_vertex(self):
        """
        Add a new vertex to the graph.
        
        Returns:
            int: The index of the newly added vertex.
        """
        self.adjacency_list[self.vertices] = []
        self.vertices += 1
        return self.vertices - 1
    
    def add_edge(self, u, v):
        """
        Add an edge between vertices u and v.
        
        Args:
            u (int): First vertex.
            v (int): Second vertex.
            
        Returns:
            bool: True if the edge was added successfully, False otherwise.
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:
            return False
        
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)
            
        return True
    
    def get_neighbors(self, vertex):
        """
        Get all neighbors of a vertex.
        
        Args:
            vertex (int): The vertex to get neighbors for.
            
        Returns:
            list: List of neighboring vertices.
        """
        if vertex in self.adjacency_list:
            return self.adjacency_list[vertex]
        return []
    
    def is_safe_color(self, vertex, color):
        """
        Check if it's safe to assign a color to a vertex.
        
        Args:
            vertex (int): The vertex to check.
            color (int): The color to check.
            
        Returns:
            bool: True if the color can be assigned safely, False otherwise.
        """
        for neighbor in self.adjacency_list[vertex]:
            if neighbor in self.colors and self.colors[neighbor] == color:
                return False
        return True
    
    def assign_color(self, vertex, color):
        """
        Assign a color to a vertex.
        
        Args:
            vertex (int): The vertex to assign a color to.
            color (int): The color to assign.
            
        Returns:
            bool: True if the color was assigned successfully, False otherwise.
        """
        if self.is_safe_color(vertex, color):
            self.colors[vertex] = color
            return True
        return False
    
    def get_color(self, vertex):
        """
        Get the color assigned to a vertex.
        
        Args:
            vertex (int): The vertex to get the color for.
            
        Returns:
            int: The color assigned to the vertex, or None if no color is assigned.
        """
        return self.colors.get(vertex)
    
    def reset_colors(self):
        """
        Reset all color assignments.
        """
        self.colors = {}
    
    def is_valid_coloring(self):
        """
        Check if the current coloring is valid.
        
        Returns:
            bool: True if the coloring is valid, False otherwise.
        """
        for vertex in range(self.vertices):
            if vertex not in self.colors:
                return False
            
            for neighbor in self.adjacency_list[vertex]:
                if neighbor in self.colors and self.colors[vertex] == self.colors[neighbor]:
                    return False
        
        return True
    
    def get_chromatic_number(self):
        """
        Get the chromatic number based on the current coloring.
        
        Returns:
            int: The chromatic number, or 0 if the coloring is not complete.
        """
        if not self.is_valid_coloring():
            return 0
        
        return len(set(self.colors.values()))
    
    def __str__(self):
        """
        String representation of the graph.
        
        Returns:
            str: String representation of the graph.
        """
        result = f"Graph with {self.vertices} vertices\n"
        result += "Adjacency List:\n"
        
        for vertex, neighbors in self.adjacency_list.items():
            result += f"{vertex}: {neighbors}\n"
        
        if self.colors:
            result += "Colors:\n"
            for vertex, color in self.colors.items():
                result += f"Vertex {vertex}: Color {color}\n"
        
        return result
