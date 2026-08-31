# Graph Colouring Problem Solver

This application implements a Graph Colouring Problem Solver using both the Backtracking Search Algorithm and a Genetic Algorithm.

## Overview

The Graph Coloring Problem is a well-known combinatorial optimization challenge that involves assigning colors to the vertices of a graph in such a way that no two adjacent vertices share the same color. The minimum number of colors required to achieve this is known as the chromatic number of the graph.

This project delivers a versatile and user-friendly Graph Coloring Problem Solver that demonstrates the strengths of both the Backtracking Search Algorithm and the Genetic Algorithm.

## Features

- **User-Defined Graphs**: Input graphs with specified vertices and edges
- **Multiple Input Methods**: Support for adjacency matrix and edge list formats
- **Dual Algorithm Support**: 
  - Backtracking Search Algorithm for systematic exploration
  - Genetic Algorithm for evolutionary optimization
- **Interactive User Interface**: Intuitive interface for graph input, algorithm selection, and result visualization
- **Solution Visualization**: Visual representation of the graph with colored vertices
- **Performance Metrics**: Metrics to measure solution quality and computational time
- **Parameter Tuning**: Adjustable parameters for the genetic algorithm

## Project Structure

```
graph_coloring_solver/
├── src/
│   ├── graph/
│   │   ├── __init__.py
│   │   └── graph.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base_algorithm.py
│   │   ├── backtracking.py
│   │   └── genetic.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── interface.py
│   │   ├── visualizer.py
│   │   └── input_handler.py
│   └── main.py
├── docs/
│   └── system_architecture.md
└── README.md
```

## Requirements

- Python 3.11 or higher
- Required packages:
  - tkinter
  - matplotlib
  - networkx

## Installation

1. Ensure Python 3.11 or higher is installed
2. Install required packages:
   ```
   pip install matplotlib networkx
   ```
3. Run the application:
   ```
   python src/main.py
   ```

## Usage

1. Launch the application
2. Input a graph using either adjacency matrix or edge list format
3. Click "Create Graph" to visualize the graph
4. Select an algorithm (Backtracking or Genetic) and set parameters
5. Click "Run Algorithm" to find a valid coloring
6. View the results and the colored graph

## Algorithms

### Backtracking Search Algorithm

The Backtracking Search Algorithm is a systematic exploration approach that examines different color assignments for each vertex. It works by recursively trying out colors and backtracking when conflicts arise. This algorithm explores the solution space while intelligently pruning paths that lead to infeasible colorings.

### Genetic Algorithm

The Genetic Algorithm is an optimization technique inspired by natural selection. In this context, we represent potential colorings as chromosomes. The algorithm evolves a population of colorings over generations using genetic operations such as crossover and mutation. The fittest colorings, those with fewer conflicts, are more likely to be passed to the next generation.

## License

This project is provided for educational purposes.
