"""
Main user interface for the Graph Colouring Problem Solver.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import os

from src.graph.graph import Graph
from src.algorithms.backtracking import BacktrackingAlgorithm
from src.algorithms.genetic import GeneticAlgorithm
from src.ui.visualizer import GraphVisualizer
from src.ui.input_handler import InputHandler

class UserInterface:
    """
    Main user interface class for the Graph Colouring Problem Solver.
    
    This class provides a graphical user interface for users to input graphs,
    select algorithms, and visualize solutions.
    """
    
    def __init__(self, root):
        """
        Initialize a new UserInterface object.
        
        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Graph Colouring Problem Solver")
        self.root.geometry("1200x800")
        
        self.graph = None
        self.visualizer = GraphVisualizer()
        self.input_handler = InputHandler()
        
        self._create_widgets()
        self._create_menu()
        
    def _create_menu(self):
        """
        Create the menu bar.
        """
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Graph", command=self._new_graph)
        file_menu.add_command(label="Load Graph", command=self._load_graph)
        file_menu.add_command(label="Save Graph", command=self._save_graph)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Help", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _create_widgets(self):
        """
        Create the main widgets for the interface.
        """
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel for input
        left_panel = ttk.LabelFrame(main_frame, text="Graph Input", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create right panel for visualization
        right_panel = ttk.LabelFrame(main_frame, text="Graph Visualization", padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create bottom panel for algorithm selection and execution
        bottom_panel = ttk.LabelFrame(main_frame, text="Algorithm Control", padding="10")
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Graph input widgets
        self._create_input_widgets(left_panel)
        
        # Graph visualization widgets
        self._create_visualization_widgets(right_panel)
        
        # Algorithm control widgets
        self._create_algorithm_widgets(bottom_panel)
    
    def _create_input_widgets(self, parent):
        """
        Create widgets for graph input.
        
        Args:
            parent: Parent widget.
        """
        # Input method selection
        input_method_frame = ttk.Frame(parent)
        input_method_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_method_frame, text="Input Method:").pack(side=tk.LEFT)
        
        self.input_method = tk.StringVar(value="matrix")
        ttk.Radiobutton(input_method_frame, text="Adjacency Matrix", 
                        variable=self.input_method, value="matrix").pack(side=tk.LEFT)
        ttk.Radiobutton(input_method_frame, text="Edge List", 
                        variable=self.input_method, value="edge_list").pack(side=tk.LEFT)
        
        # Input text area
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(input_frame, text="Enter graph data:").pack(anchor=tk.W)
        
        self.input_text = tk.Text(input_frame, height=10, width=40)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Example button
        example_button = ttk.Button(parent, text="Load Example", command=self._load_example)
        example_button.pack(fill=tk.X, pady=5)
        
        # Create graph button
        create_button = ttk.Button(parent, text="Create Graph", command=self._create_graph)
        create_button.pack(fill=tk.X, pady=5)
    
    def _create_visualization_widgets(self, parent):
        """
        Create widgets for graph visualization.
        
        Args:
            parent: Parent widget.
        """
        # Create a frame for the matplotlib figure
        self.fig_frame = ttk.Frame(parent)
        self.fig_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create initial empty figure
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title("No Graph Loaded")
        ax.axis('off')
        
        # Embed the figure in the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Save visualization button
        save_button = ttk.Button(parent, text="Save Visualization", command=self._save_visualization)
        save_button.pack(fill=tk.X, pady=5)
    
    def _create_algorithm_widgets(self, parent):
        """
        Create widgets for algorithm control.
        
        Args:
            parent: Parent widget.
        """
        # Create a frame for algorithm selection
        algo_frame = ttk.Frame(parent)
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="Algorithm:").pack(side=tk.LEFT)
        
        self.algorithm = tk.StringVar(value="backtracking")
        ttk.Radiobutton(algo_frame, text="Backtracking", 
                        variable=self.algorithm, value="backtracking",
                        command=self._update_param_frame).pack(side=tk.LEFT)
        ttk.Radiobutton(algo_frame, text="Genetic Algorithm", 
                        variable=self.algorithm, value="genetic",
                        command=self._update_param_frame).pack(side=tk.LEFT)
        
        # Create a frame for algorithm parameters
        self.param_frame = ttk.LabelFrame(parent, text="Algorithm Parameters", padding="10")
        self.param_frame.pack(fill=tk.X, pady=5)
        
        # Initialize parameter widgets
        self._update_param_frame()
        
        # Create a frame for execution buttons
        exec_frame = ttk.Frame(parent)
        exec_frame.pack(fill=tk.X, pady=5)
        
        # Run algorithm button
        run_button = ttk.Button(exec_frame, text="Run Algorithm", command=self._run_algorithm)
        run_button.pack(side=tk.LEFT, padx=5)
        
        # Reset colors button
        reset_button = ttk.Button(exec_frame, text="Reset Colors", command=self._reset_colors)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        self.results_frame.pack(fill=tk.X, pady=5)
        
        self.results_text = tk.Text(self.results_frame, height=5, width=40)
        self.results_text.pack(fill=tk.X)
        self.results_text.config(state=tk.DISABLED)
    
    def _update_param_frame(self):
        """
        Update the parameter frame based on the selected algorithm.
        """
        # Clear existing widgets
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        
        algorithm = self.algorithm.get()
        
        if algorithm == "backtracking":
            # Backtracking parameters
            ttk.Label(self.param_frame, text="Max Colors:").grid(row=0, column=0, sticky=tk.W)
            
            self.max_colors_var = tk.StringVar(value="")
            max_colors_entry = ttk.Entry(self.param_frame, textvariable=self.max_colors_var)
            max_colors_entry.grid(row=0, column=1, sticky=tk.W)
            
            ttk.Label(self.param_frame, text="(Leave empty to use maximum possible)").grid(
                row=0, column=2, sticky=tk.W)
            
        elif algorithm == "genetic":
            # Genetic algorithm parameters
            params = [
                ("Population Size:", "population_size", "50"),
                ("Max Generations:", "max_generations", "100"),
                ("Crossover Rate:", "crossover_rate", "0.8"),
                ("Mutation Rate:", "mutation_rate", "0.2"),
                ("Elite Size:", "elite_size", "5")
            ]
            
            self.genetic_params = {}
            
            for i, (label, param, default) in enumerate(params):
                ttk.Label(self.param_frame, text=label).grid(row=i, column=0, sticky=tk.W)
                
                var = tk.StringVar(value=default)
                self.genetic_params[param] = var
                
                entry = ttk.Entry(self.param_frame, textvariable=var)
                entry.grid(row=i, column=1, sticky=tk.W)
    
    def _new_graph(self):
        """
        Create a new empty graph.
        """
        self.input_text.delete(1.0, tk.END)
        self._reset_results()
        
        if self.graph:
            self.graph.reset_colors()
            self._update_visualization()
    
    def _load_example(self):
        """
        Load an example graph.
        """
        if self.input_method.get() == "matrix":
            example = "0 1 0 1 1\n1 0 1 0 1\n0 1 0 1 1\n1 0 1 0 1\n1 1 1 1 0"
        else:
            example = "5\n0 1\n0 3\n0 4\n1 2\n1 4\n2 3\n2 4\n3 4"
        
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, example)
    
    def _create_graph(self):
        """
        Create a graph from the input data.
        """
        input_data = self.input_text.get(1.0, tk.END)
        
        if self.input_method.get() == "matrix":
            graph_data = self.input_handler.parse_graph_from_adjacency_matrix(input_data)
        else:
            graph_data = self.input_handler.parse_graph_from_edge_list(input_data)
        
        if not graph_data:
            messagebox.showerror("Error", "Invalid graph data")
            return
        
        # Create the graph
        self.graph = Graph(graph_data['vertices'])
        
        for u, v in graph_data['edges']:
            self.graph.add_edge(u, v)
        
        # Update visualization
        self._update_visualization()
        self._reset_results()
        
        messagebox.showinfo("Success", f"Graph created with {self.graph.vertices} vertices and {len(graph_data['edges'])} edges")
    
    def _update_visualization(self):
        """
        Update the graph visualization.
        """
        if not self.graph:
            return
        
        # Clear the figure frame
        for widget in self.fig_frame.winfo_children():
            widget.destroy()
        
        # Draw the graph
        fig, ax = self.visualizer.draw_graph(self.graph)
        
        # Embed the figure in the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _save_visualization(self):
        """
        Save the current visualization to a file.
        """
        if not self.graph:
            messagebox.showerror("Error", "No graph to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            self.visualizer.save_figure(filename)
            messagebox.showinfo("Success", f"Visualization saved to {filename}")
    
    def _load_graph(self):
        """
        Load a graph from a file.
        """
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'vertices' not in data or 'edges' not in data:
                messagebox.showerror("Error", "Invalid graph file format")
                return
            
            # Create the graph
            self.graph = Graph(data['vertices'])
            
            for u, v in data['edges']:
                self.graph.add_edge(u, v)
            
            # Update visualization
            self._update_visualization()
            self._reset_results()
            
            messagebox.showinfo("Success", f"Graph loaded from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {str(e)}")
    
    def _save_graph(self):
        """
        Save the current graph to a file.
        """
        if not self.graph:
            messagebox.showerror("Error", "No graph to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            # Collect edges
            edges = []
            for u in range(self.graph.vertices):
                for v in self.graph.get_neighbors(u):
                    if u < v:  # Add each edge only once
                        edges.append([u, v])
            
            data = {
                'vertices': self.graph.vertices,
                'edges': edges
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            messagebox.showinfo("Success", f"Graph saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")
    
    def _run_algorithm(self):
        """
        Run the selected algorithm on the current graph.
        """
        if not self.graph:
            messagebox.showerror("Error", "No graph to color")
            return
        
        algorithm_name = self.algorithm.get()
        
        if algorithm_name == "backtracking":
            # Get parameters
            max_colors = None
            if self.max_colors_var.get():
                try:
                    max_colors = int(self.max_colors_var.get())
                    if max_colors <= 0:
                        messagebox.showerror("Error", "Maximum colors must be positive")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Maximum colors must be an integer")
                    return
            
            # Create and run algorithm
            algorithm = BacktrackingAlgorithm()
            success = algorithm.solve(self.graph, max_colors)
            
        elif algorithm_name == "genetic":
            # Get parameters
            params = {}
            for param, var in self.genetic_params.items():
                try:
                    if param in ['population_size', 'max_generations', 'elite_size']:
                        value = int(var.get())
                    else:
                        value = float(var.get())
                    params[param] = value
                except ValueError:
                    messagebox.showerror("Error", f"Invalid value for {param}")
                    return
            
            # Validate parameters
            valid, error = self.input_handler.validate_algorithm_params('genetic', params)
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            # Create and run algorithm
            algorithm = GeneticAlgorithm(
                population_size=params['population_size'],
                max_generations=params['max_generations'],
                crossover_rate=params['crossover_rate'],
                mutation_rate=params['mutation_rate'],
                elite_size=params['elite_size']
            )
            success = algorithm.solve(self.graph)
        
        # Update visualization
        self._update_visualization()
        
        # Display results
        if success:
            self._display_results(algorithm)
        else:
            messagebox.showerror("Error", "Failed to find a valid coloring")
    
    def _reset_colors(self):
        """
        Reset the colors of the current graph.
        """
        if not self.graph:
            return
        
        self.graph.reset_colors()
        self._update_visualization()
        self._reset_results()
    
    def _display_results(self, algorithm):
        """
        Display the results of the algorithm.
        
        Args:
            algorithm: The algorithm that was run.
        """
        metrics = algorithm.get_metrics()
        
        # Enable text widget for editing
        self.results_text.config(state=tk.NORMAL)
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Display results
        self.results_text.insert(tk.END, f"Chromatic Number: {metrics['chromatic_number']}\n")
        self.results_text.insert(tk.END, f"Execution Time: {metrics['execution_time']:.4f} seconds\n")
        
        if isinstance(algorithm, BacktrackingAlgorithm):
            self.results_text.insert(tk.END, f"Backtracks: {metrics['backtracks']}\n")
        elif isinstance(algorithm, GeneticAlgorithm):
            self.results_text.insert(tk.END, f"Generations: {metrics['generations']}\n")
            self.results_text.insert(tk.END, f"Final Fitness: {metrics['final_fitness']:.4f}\n")
        
        # Disable text widget for editing
        self.results_text.config(state=tk.DISABLED)
    
    def _reset_results(self):
        """
        Reset the results display.
        """
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def _show_about(self):
        """
        Show the about dialog.
        """
        messagebox.showinfo(
            "About",
            "Graph Colouring Problem Solver\n\n"
            "This application solves the Graph Colouring Problem using "
            "both the Backtracking Search Algorithm and a Genetic Algorithm."
        )
    
    def _show_help(self):
        """
        Show the help dialog.
        """
        help_text = (
            "Graph Colouring Problem Solver Help\n\n"
            "1. Input a graph using either adjacency matrix or edge list format.\n"
            "2. Click 'Create Graph' to visualize the graph.\n"
            "3. Select an algorithm and set its parameters.\n"
            "4. Click 'Run Algorithm' to find a valid coloring.\n"
            "5. View the results and the colored graph.\n\n"
            "Adjacency Matrix Format:\n"
            "Enter a square matrix where 1 indicates an edge and 0 indicates no edge.\n\n"
            "Edge List Format:\n"
            "First line: number of vertices\n"
            "Subsequent lines: pairs of vertices forming edges."
        )
        
        messagebox.showinfo("Help", help_text)
    
    def run(self):
        """
        Run the user interface.
        """
        self.root.mainloop()
