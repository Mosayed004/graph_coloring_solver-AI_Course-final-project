import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import time
import math

class GraphColoringSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring Problem Solver")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Graph data
        self.graph = nx.Graph()
        self.vertex_positions = {}
        self.colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF3", 
                       "#FF8C33", "#8C33FF", "#33FF8C", "#FF338C"]
        self.coloring_solution = {}
        self.max_colors = 4
        self.chromatic_number = 0
        self.execution_time = 0
        # Performance data for genetic algorithm
        self.fitness_history = []
        self.avg_fitness_history = []
        
        # Create UI
        self.create_ui()
        
        # Initialize with an empty graph
        self.update_graph_display()

    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        controls_frame = ttk.LabelFrame(main_frame, text="Controls")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Graph editing controls
        graph_edit_frame = ttk.LabelFrame(controls_frame, text="Graph Selection")
        graph_edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Graph shape selection
        ttk.Label(graph_edit_frame, text="Graph Shape:").pack(anchor=tk.W, padx=5, pady=2)
        self.shape_var = tk.StringVar(value="Petersen")
        shape_combo = ttk.Combobox(graph_edit_frame, textvariable=self.shape_var, 
                                  values=["Cycle", "Wheel", "Complete", "Petersen", "Random"], 
                                  state="readonly")
        shape_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # Number of vertices (for applicable graphs)
        ttk.Label(graph_edit_frame, text="Number of Vertices:").pack(anchor=tk.W, padx=5, pady=2)
        self.num_vertices_var = tk.IntVar(value=5)
        ttk.Spinbox(graph_edit_frame, from_=3, to=20, textvariable=self.num_vertices_var, width=5).pack(anchor=tk.W, padx=5, pady=2)
        
        # Clear graph
        ttk.Button(graph_edit_frame, text="Clear Graph", command=self.clear_graph).pack(fill=tk.X, padx=5, pady=2)
        
        # Algorithm settings
        algo_frame = ttk.LabelFrame(controls_frame, text="Algorithm Settings")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Algorithm selection
        ttk.Label(algo_frame, text="Algorithm:").pack(anchor=tk.W, padx=5, pady=2)
        self.algorithm_var = tk.StringVar(value="backtracking")
        algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var, 
                                      values=["backtracking", "genetic"], state="readonly")
        algorithm_combo.pack(fill=tk.X, padx=5, pady=2)
        algorithm_combo.bind("<<ComboboxSelected>>", self.toggle_algorithm_settings)
        
        # Max colors
        color_frame = ttk.Frame(algo_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(color_frame, text="Max Colors:").pack(side=tk.LEFT)
        self.max_colors_var = tk.IntVar(value=4)
        ttk.Spinbox(color_frame, from_=1, to=10, textvariable=self.max_colors_var, width=5, 
                   command=lambda: setattr(self, 'max_colors', self.max_colors_var.get())).pack(side=tk.LEFT, padx=5)
        
        # Genetic algorithm parameters
        self.genetic_frame = ttk.LabelFrame(algo_frame, text="Genetic Algorithm Parameters")
        self.genetic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Population size
        pop_frame = ttk.Frame(self.genetic_frame)
        pop_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(pop_frame, text="Population Size:").pack(side=tk.LEFT)
        self.population_size_var = tk.IntVar(value=50)
        ttk.Spinbox(pop_frame, from_=10, to=200, textvariable=self.population_size_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Generations
        gen_frame = ttk.Frame(self.genetic_frame)
        gen_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(gen_frame, text="Generations:").pack(side=tk.LEFT)
        self.generations_var = tk.IntVar(value=100)
        ttk.Spinbox(gen_frame, from_=10, to=500, textvariable=self.generations_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Mutation rate
        mut_frame = ttk.Frame(self.genetic_frame)
        mut_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(mut_frame, text="Mutation Rate:").pack(side=tk.LEFT)
        self.mutation_rate_var = tk.DoubleVar(value=0.1)
        ttk.Spinbox(mut_frame, from_=0.01, to=0.5, increment=0.01, textvariable=self.mutation_rate_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Elitism count
        elite_frame = ttk.Frame(self.genetic_frame)
        elite_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(elite_frame, text="Elitism Count:").pack(side=tk.LEFT)
        self.elitism_count_var = tk.IntVar(value=5)
        ttk.Spinbox(elite_frame, from_=0, to=20, textvariable=self.elitism_count_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Run algorithm
        run_frame = ttk.LabelFrame(controls_frame, text="Run")
        run_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(run_frame, text="Solve Graph Coloring", command=self.solve_graph_coloring).pack(fill=tk.X, padx=5, pady=5)
        
        # Results 
        results_frame = ttk.LabelFrame(controls_frame, text="Results")
        results_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chromatic_label = ttk.Label(results_frame, text="Chromatic Number: N/A")
        self.chromatic_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.time_label = ttk.Label(results_frame, text="Execution Time: N/A")
        self.time_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.status_label = ttk.Label(results_frame, text="Status: Ready")
        self.status_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Right panel for visualizations
        vis_frame = ttk.Frame(main_frame)
        vis_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Graph display area
        graph_frame = ttk.LabelFrame(vis_frame, text="Graph Visualization")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Matplotlib figure for graph visualization
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.graph_canvas = FigureCanvasTkAgg(self.figure, graph_frame)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Performance plot area
        perf_frame = ttk.LabelFrame(vis_frame, text="Genetic Algorithm Performance")
        perf_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Matplotlib figure for performance plot
        self.perf_figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.perf_ax = self.perf_figure.add_subplot(111)
        self.perf_canvas = FigureCanvasTkAgg(self.perf_figure, perf_frame)
        self.perf_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Set up canvas interactions for graph
        self.graph_canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.graph_canvas.mpl_connect('motion_notify_event', self.on_canvas_drag)
        self.graph_canvas.mpl_connect('button_release_event', self.on_canvas_release)

        # Initial state
        self.toggle_algorithm_settings(None)
        self.update_performance_plot()
        
    def toggle_algorithm_settings(self, event):
        if self.algorithm_var.get() == "genetic":
            self.genetic_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.genetic_frame.pack_forget()
    
    def update_graph_display(self):
        self.ax.clear()
        
        # If we have positions
        if len(self.vertex_positions) < len(self.graph.nodes):
            # Generate positions for new nodes
            for node in self.graph.nodes:
                if node not in self.vertex_positions:
                    self.vertex_positions[node] = (random.uniform(0.1, 0.9), random.uniform(0.1, 0.9))
                    
        # Draw the graph
        node_colors = [self.coloring_solution.get(node, '#CCCCCC') for node in self.graph.nodes]
        nx.draw(
            self.graph,
            pos=self.vertex_positions,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_weight='bold',
            ax=self.ax
        )
        
        self.figure.tight_layout()
        self.graph_canvas.draw()
        
    def update_performance_plot(self):
        self.perf_ax.clear()
        
        if self.fitness_history:
            generations = range(len(self.fitness_history))
            self.perf_ax.plot(generations, self.fitness_history, 'b-', label='Best Fitness')
            self.perf_ax.plot(generations, self.avg_fitness_history, 'r--', label='Average Fitness')
            self.perf_ax.set_xlabel('Generation')
            self.perf_ax.set_ylabel('Fitness Score')
            self.perf_ax.set_title('Genetic Algorithm Performance')
            self.perf_ax.grid(True)
            self.perf_ax.legend()
        else:
            self.perf_ax.text(0.5, 0.5, 'No performance data available', 
                             horizontalalignment='center', verticalalignment='center')
            self.perf_ax.set_xlabel('Generation')
            self.perf_ax.set_ylabel('Fitness Score')
            self.perf_ax.set_title('Genetic Algorithm Performance')
        
        self.perf_figure.tight_layout()
        self.perf_canvas.draw_idle()
        self.perf_canvas.flush_events()
        
    def clear_graph(self):
        self.graph.clear()
        self.vertex_positions.clear()
        self.coloring_solution.clear()
        self.fitness_history.clear()
        self.avg_fitness_history.clear()
        self.update_graph_display()
        self.update_performance_plot()
        self.chromatic_label.config(text="Chromatic Number: N/A")
        self.time_label.config(text="Execution Time: N/A")
        self.status_label.config(text="Status: Ready")
        
    def add_sample_graph(self, shape, num_vertices):
        # Clear existing graph
        self.graph.clear()
        self.vertex_positions.clear()
        self.coloring_solution.clear()
        self.fitness_history.clear()
        self.avg_fitness_history.clear()
        
        # Generate graph based on selected shape
        if shape == "Cycle":
            self.graph = nx.cycle_graph(num_vertices)
            vertices = list(range(num_vertices))
        elif shape == "Wheel":
            self.graph = nx.wheel_graph(num_vertices)
            vertices = list(range(num_vertices))
        elif shape == "Complete":
            self.graph = nx.complete_graph(num_vertices)
            vertices = list(range(num_vertices))
        elif shape == "Petersen":
            self.graph = nx.petersen_graph()
            vertices = list(range(10))  # Petersen graph has 10 vertices
            num_vertices = 10
        else:  # Random
            self.graph = nx.erdos_renyi_graph(num_vertices, 0.5)
            vertices = list(range(num_vertices))
        
        # Relabel nodes to use letters for better readability
        mapping = {i: chr(65 + i) for i in range(num_vertices)}  # A, B, C, ...
        self.graph = nx.relabel_nodes(self.graph, mapping)
        vertices = list(self.graph.nodes)
        
        # Calculate positions for a circular layout
        angle = 2 * math.pi / num_vertices
        radius = 0.4
        center_x, center_y = 0.5, 0.5
        
        for i, v in enumerate(vertices):
            x = center_x + radius * math.cos(i * angle - math.pi/2)
            y = center_y + radius * math.sin(i * angle - math.pi/2)
            self.vertex_positions[v] = (x, y)
        
        # For Wheel graph, place the central vertex (node 0) in the center
        if shape == "Wheel" and num_vertices > 3:
            self.vertex_positions[vertices[0]] = (center_x, center_y)
            for i, v in enumerate(vertices[1:], 1):
                x = center_x + radius * math.cos((i-1) * angle - math.pi/2)
                y = center_y + radius * math.sin((i-1) * angle - math.pi/2)
                self.vertex_positions[v] = (x, y)
        
        self.update_graph_display()
        
    def on_canvas_click(self, event):
        if event.xdata is None or event.ydata is None:
            return
        for node, (x, y) in self.vertex_positions.items():
            display_x, display_y = self.ax.transData.transform((x, y))
            event_display_x, event_display_y = self.ax.transData.transform((event.xdata, event.ydata))
            distance = math.sqrt((display_x - event_display_x)**2 + (display_y - event_display_y)**2)
            if distance < 15:
                self.dragging = True
                self.dragged_node = node
                return
                
    def on_canvas_drag(self, event):
        if hasattr(self, 'dragging') and self.dragging and event.xdata is not None and event.ydata is not None:
            self.vertex_positions[self.dragged_node] = (event.xdata, event.ydata)
            self.update_graph_display()
            
    def on_canvas_release(self, event):
        self.dragging = False
        self.dragged_node = None

    def solve_graph_coloring(self):
        # Generate the graph based on selected shape
        shape = self.shape_var.get()
        num_vertices = self.num_vertices_var.get()
        
        if shape == "Petersen":
            num_vertices = 10  # Petersen graph is fixed
        elif num_vertices < 3:
            messagebox.showwarning("Warning", "Number of vertices must be at least 3.")
            return
            
        self.add_sample_graph(shape, num_vertices)
        
        self.max_colors = self.max_colors_var.get()
        algorithm = self.algorithm_var.get()
        
        self.status_label.config(text="Status: Running...")
        self.root.update()
        
        start_time = time.time()
        
        if algorithm == "backtracking":
            solution, chromatic_number = self.backtracking_coloring()
        else:
            solution, chromatic_number = self.genetic_coloring()
            
        end_time = time.time()
        self.execution_time = end_time - start_time
        
        if solution:
            self.coloring_solution = solution
            self.chromatic_number = chromatic_number
            self.chromatic_label.config(text=f"Chromatic Number: {chromatic_number}")
            self.time_label.config(text=f"Execution Time: {self.execution_time:.4f} seconds")
            self.status_label.config(text="Status: Solution found")
        else:
            self.status_label.config(text="Status: No solution found")
            
        self.update_graph_display()
        self.update_performance_plot()
    
    def backtracking_coloring(self):
        vertices = sorted(self.graph.nodes(), key=lambda x: len(list(self.graph.neighbors(x))), reverse=True)
        colors = {}
        available_colors = list(range(1, self.max_colors + 1))
        
        def is_safe(vertex, color):
            for neighbor in self.graph.neighbors(vertex):
                if neighbor in colors and colors[neighbor] == color:
                    return False
            return True
        
        def backtrack(vertex_index):
            if vertex_index == len(vertices):
                return True
            vertex = vertices[vertex_index]
            for color in available_colors:
                if is_safe(vertex, color):
                    colors[vertex] = color
                    if backtrack(vertex_index + 1):
                        return True
                    colors[vertex] = 0
            return False
        
        if backtrack(0):
            solution = {vertex: self.colors[color-1] for vertex, color in colors.items()}
            chromatic_number = len(set(colors.values()))
            return solution, chromatic_number
        else:
            messagebox.showwarning("Warning", f"No solution found with {self.max_colors} colors. Try increasing the maximum number of colors.")
            return None, 0
    
    def genetic_coloring(self):
        population_size = self.population_size_var.get()
        generations = self.generations_var.get()
        mutation_rate = self.mutation_rate_var.get()
        elitism_count = self.elitism_count_var.get()
        
        vertices = list(self.graph.nodes())
        num_vertices = len(vertices)
        
        population = [[random.randint(1, self.max_colors) for _ in range(num_vertices)] for _ in range(population_size)]
        
        def fitness(chromosome):
            conflicts = 0
            for edge in self.graph.edges():
                i = vertices.index(edge[0])
                j = vertices.index(edge[1])
                if chromosome[i] == chromosome[j]:
                    conflicts += 1
            colors_used = len(set(chromosome))
            if conflicts > 0:
                return 1 / (1 + conflicts * 10 + colors_used)
            return 1 / (1 + colors_used)
        
        def selection(population):
            tournament_size = 3
            selected = []
            for _ in range(len(population)):
                tournament = random.sample(population, tournament_size)
                winner = max(tournament, key=fitness)
                selected.append(winner)
            return selected
        
        def crossover(parent1, parent2):
            child = []
            for i in range(len(parent1)):
                if random.random() < 0.5:
                    child.append(parent1[i])
                else:
                    child.append(parent2[i])
            return child
        
        def mutate(chromosome):
            for i in range(len(chromosome)):
                if random.random() < mutation_rate:
                    chromosome[i] = random.randint(1, self.max_colors)
            return chromosome
        
        best_chromosome = None
        best_fitness = -1
        self.fitness_history = []
        self.avg_fitness_history = []
        
        for generation in range(generations):
            population_fitness = [(chromosome, fitness(chromosome)) for chromosome in population]
            population_fitness.sort(key=lambda x: x[1], reverse=True)
            current_best_fitness = population_fitness[0][1]
            # Calculate average fitness
            avg_fitness = sum(fitness for _, fitness in population_fitness) / len(population_fitness)
            if current_best_fitness > best_fitness:
                best_chromosome = population_fitness[0][0]
                best_fitness = current_best_fitness
            self.fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            if best_fitness > 0.5:
                break
            new_population = [population_fitness[i][0] for i in range(min(elitism_count, len(population)))]
            selected = selection([x[0] for x in population_fitness])
            while len(new_population) < population_size:
                parent1 = random.choice(selected)
                parent2 = random.choice(selected)
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_population.append(child)
            population = new_population
            if generation % 10 == 0:
                self.status_label.config(text=f"Status: Generation {generation}/{generations}")
                self.update_performance_plot()
                self.root.update()
        
        # Final update to ensure the last fitness values are plotted
        self.update_performance_plot()
        
        if best_chromosome:
            solution = {vertex: self.colors[best_chromosome[i]-1 % len(self.colors)] for i, vertex in enumerate(vertices)}
            chromatic_number = len(set(best_chromosome))
            return solution, chromatic_number
        else:
            messagebox.showwarning("Warning", "Genetic algorithm did not find a valid solution. Try increasing the number of generations or adjusting parameters.")
            return None, 0

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringSolver(root)
    root.mainloop()