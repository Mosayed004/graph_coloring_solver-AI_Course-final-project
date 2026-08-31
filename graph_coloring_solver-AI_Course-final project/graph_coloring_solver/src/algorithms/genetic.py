"""
Genetic Algorithm implementation for the Graph Colouring Problem Solver.
"""

import time
import random
from src.algorithms.base_algorithm import BaseAlgorithm

class GeneticAlgorithm(BaseAlgorithm):
    """
    Implementation of the Genetic Algorithm for graph coloring.
    
    This algorithm evolves a population of colorings over generations using
    genetic operations such as crossover and mutation.
    """
    
    def __init__(self, population_size=50, max_generations=100, 
                 crossover_rate=0.8, mutation_rate=0.2, elite_size=5):
        """
        Initialize a new GeneticAlgorithm object.
        
        Args:
            population_size (int): Size of the population.
            max_generations (int): Maximum number of generations.
            crossover_rate (float): Probability of crossover.
            mutation_rate (float): Probability of mutation.
            elite_size (int): Number of elite individuals to preserve.
        """
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        
        self.solution = {}
        self.metrics = {
            'execution_time': 0,
            'generations': 0,
            'chromatic_number': 0,
            'final_fitness': 0,
            'best_fitness_history': []
        }
        self.max_colors = None
    
    def solve(self, graph, max_colors=None):
        """
        Solve the graph coloring problem for the given graph using genetic algorithm.
        
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
            'generations': 0,
            'chromatic_number': 0,
            'final_fitness': 0,
            'best_fitness_history': []
        }
        
        # If max_colors is not specified, use the number of vertices as an upper bound
        self.max_colors = max_colors if max_colors is not None else graph.vertices
        
        # Reset graph colors
        graph.reset_colors()
        
        # Start timing
        start_time = time.time()
        
        # Initialize population
        population = self._initialize_population(graph)
        
        # Evolve population
        best_individual = None
        best_fitness = -1
        
        for generation in range(self.max_generations):
            self.metrics['generations'] = generation + 1
            
            # Evaluate fitness
            fitness_scores = [self._calculate_fitness(individual, graph) for individual in population]
            
            # Track best individual
            max_fitness_idx = fitness_scores.index(max(fitness_scores))
            if fitness_scores[max_fitness_idx] > best_fitness:
                best_fitness = fitness_scores[max_fitness_idx]
                best_individual = population[max_fitness_idx].copy()
            
            self.metrics['best_fitness_history'].append(best_fitness)
            
            # Check if we found a valid solution
            if best_fitness == 1.0:
                break
            
            # Select parents for next generation
            parents = self._selection(population, fitness_scores)
            
            # Create next generation
            next_generation = []
            
            # Elitism: keep the best individuals
            sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
            for i in range(self.elite_size):
                next_generation.append(population[sorted_indices[i]].copy())
            
            # Crossover and mutation
            while len(next_generation) < self.population_size:
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)
                
                if random.random() < self.crossover_rate:
                    child = self._crossover(parent1, parent2)
                else:
                    child = parent1.copy()
                
                if random.random() < self.mutation_rate:
                    child = self._mutation(child, graph)
                
                next_generation.append(child)
            
            population = next_generation
        
        # End timing
        end_time = time.time()
        self.metrics['execution_time'] = end_time - start_time
        
        # Apply the best solution to the graph
        if best_individual:
            for vertex, color in best_individual.items():
                graph.assign_color(vertex, color)
            
            self.solution = best_individual
            self.metrics['chromatic_number'] = len(set(best_individual.values()))
            self.metrics['final_fitness'] = best_fitness
            
            return graph.is_valid_coloring()
        
        return False
    
    def _initialize_population(self, graph):
        """
        Initialize a random population of colorings.
        
        Args:
            graph: The graph to color.
            
        Returns:
            list: A list of dictionaries representing colorings.
        """
        population = []
        
        for _ in range(self.population_size):
            individual = {}
            for vertex in range(graph.vertices):
                # Assign a random color to each vertex
                individual[vertex] = random.randint(1, self.max_colors)
            population.append(individual)
        
        return population
    
    def _calculate_fitness(self, individual, graph):
        """
        Calculate the fitness of an individual.
        
        The fitness is based on the number of conflicts in the coloring.
        A conflict occurs when adjacent vertices have the same color.
        
        Args:
            individual: A dictionary mapping vertices to colors.
            graph: The graph being colored.
            
        Returns:
            float: The fitness score (0 to 1, where 1 is best).
        """
        conflicts = 0
        total_edges = 0
        
        for vertex in range(graph.vertices):
            neighbors = graph.get_neighbors(vertex)
            total_edges += len(neighbors)
            
            for neighbor in neighbors:
                if individual[vertex] == individual[neighbor]:
                    conflicts += 1
        
        # Divide by 2 because each edge is counted twice
        total_edges //= 2
        conflicts //= 2
        
        # Fitness is inversely proportional to the number of conflicts
        if total_edges == 0:
            return 1.0  # No edges means no conflicts
        
        return 1.0 - (conflicts / total_edges)
    
    def _selection(self, population, fitness_scores):
        """
        Select individuals for reproduction using tournament selection.
        
        Args:
            population: The current population.
            fitness_scores: The fitness scores of the population.
            
        Returns:
            list: Selected individuals.
        """
        selected = []
        tournament_size = 3
        
        for _ in range(self.population_size):
            # Select random individuals for tournament
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Select the best individual from the tournament
            winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
            selected.append(population[winner_idx])
        
        return selected
    
    def _crossover(self, parent1, parent2):
        """
        Perform crossover between two parents.
        
        Args:
            parent1: First parent.
            parent2: Second parent.
            
        Returns:
            dict: Child individual.
        """
        child = {}
        crossover_point = random.randint(1, len(parent1) - 1)
        
        for vertex in range(len(parent1)):
            if vertex < crossover_point:
                child[vertex] = parent1[vertex]
            else:
                child[vertex] = parent2[vertex]
        
        return child
    
    def _mutation(self, individual, graph):
        """
        Perform mutation on an individual.
        
        Args:
            individual: The individual to mutate.
            graph: The graph being colored.
            
        Returns:
            dict: Mutated individual.
        """
        mutated = individual.copy()
        
        # Select a random vertex to mutate
        vertex = random.randint(0, len(individual) - 1)
        
        # Assign a new random color
        current_color = mutated[vertex]
        new_color = current_color
        
        while new_color == current_color:
            new_color = random.randint(1, self.max_colors)
        
        mutated[vertex] = new_color
        
        return mutated
    
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
