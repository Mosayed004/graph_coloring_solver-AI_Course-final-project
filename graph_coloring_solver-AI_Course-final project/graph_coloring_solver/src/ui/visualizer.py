"""
Graph visualizer for the Graph Colouring Problem Solver.
"""

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors

class GraphVisualizer:
    """
    A class for visualizing graphs and their colorings.
    
    This class provides methods to draw graphs with colored vertices
    and to animate the coloring process.
    """
    
    def __init__(self):
        """
        Initialize a new GraphVisualizer object.
        """
        self.fig = None
        self.ax = None
        self.graph = None
        self.pos = None
        self.color_map = ['#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', 
                          '#FF00FF', '#00FFFF', '#FFA500', '#800080', '#008000']
        
    def _extend_color_map(self, num_colors):
        """
        Extend the color map if more colors are needed.
        
        Args:
            num_colors: Number of colors needed.
        """
        if num_colors <= len(self.color_map):
            return
            
        # Add more colors from matplotlib's color maps
        additional_colors = list(mcolors.CSS4_COLORS.values())
        self.color_map.extend(additional_colors)
        
    def draw_graph(self, graph, title="Graph Coloring"):
        """
        Draw a graph with its current coloring.
        
        Args:
            graph: The graph to draw.
            title: Title for the plot.
            
        Returns:
            tuple: Figure and axes objects.
        """
        # Create a NetworkX graph
        G = nx.Graph()
        
        # Add nodes
        for v in range(graph.vertices):
            G.add_node(v)
        
        # Add edges
        for v in range(graph.vertices):
            for neighbor in graph.get_neighbors(v):
                if v < neighbor:  # Add each edge only once
                    G.add_edge(v, neighbor)
        
        # Create figure and axes
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_title(title)
        self.graph = G
        
        # Calculate positions for nodes
        self.pos = nx.spring_layout(G)
        
        # Get colors for nodes
        node_colors = []
        max_color = 0
        
        for v in range(graph.vertices):
            color = graph.get_color(v)
            if color is None:
                node_colors.append('#CCCCCC')  # Gray for uncolored nodes
            else:
                max_color = max(max_color, color)
                node_colors.append(self.color_map[color % len(self.color_map)])
        
        # Ensure we have enough colors
        self._extend_color_map(max_color + 1)
        
        # Draw the graph
        nx.draw(G, self.pos, with_labels=True, node_color=node_colors, 
                node_size=500, font_size=10, font_weight='bold', ax=self.ax)
        
        return self.fig, self.ax
    
    def update_colors(self, graph):
        """
        Update the colors of the graph visualization.
        
        Args:
            graph: The graph with updated colors.
            
        Returns:
            tuple: Figure and axes objects.
        """
        if self.fig is None or self.ax is None:
            return self.draw_graph(graph)
        
        # Clear the axes
        self.ax.clear()
        
        # Get colors for nodes
        node_colors = []
        max_color = 0
        
        for v in range(graph.vertices):
            color = graph.get_color(v)
            if color is None:
                node_colors.append('#CCCCCC')  # Gray for uncolored nodes
            else:
                max_color = max(max_color, color)
                node_colors.append(self.color_map[color % len(self.color_map)])
        
        # Ensure we have enough colors
        self._extend_color_map(max_color + 1)
        
        # Draw the graph
        nx.draw(self.graph, self.pos, with_labels=True, node_color=node_colors, 
                node_size=500, font_size=10, font_weight='bold', ax=self.ax)
        
        self.fig.canvas.draw()
        
        return self.fig, self.ax
    
    def save_figure(self, filename):
        """
        Save the current figure to a file.
        
        Args:
            filename: Name of the file to save to.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.fig is None:
            return False
            
        self.fig.savefig(filename)
        return True
    
    def show(self):
        """
        Show the current figure.
        """
        if self.fig is not None:
            plt.show()
    
    def close(self):
        """
        Close the current figure.
        """
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
