# Graph Colouring Problem Solver - System Architecture

## Overview
This document outlines the architecture of the Graph Colouring Problem Solver application, which implements both Backtracking Search Algorithm and Genetic Algorithm to solve the graph coloring problem.

## System Components

### 1. Core Components
- **Graph Module**: Responsible for graph representation, manipulation, and validation
- **Algorithm Module**: Contains implementations of both algorithms
- **UI Module**: Handles user interaction and visualization
- **Performance Module**: Manages metrics collection and parameter tuning

### 2. Component Interactions
```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  User Interface │◄────┤ Visualization   │
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────┐     ┌────────┴────────┐
│                 │     │                 │
│  Graph Manager  │────►│ Solution Manager│
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────┐     ┌────────┴────────┐
│  Algorithm      │     │  Performance    │
│  Implementations│────►│  Metrics        │
└─────────────────┘     └─────────────────┘
```

## Module Specifications

### 1. Graph Module
- **Graph Class**: Core data structure for representing graphs
  - Attributes: vertices, edges, adjacency matrix/list
  - Methods: add_vertex(), add_edge(), is_valid_coloring(), etc.
- **GraphIO Class**: Handles graph input/output operations
  - Methods: load_graph(), save_graph(), import_from_format(), etc.

### 2. Algorithm Module
- **BaseAlgorithm Interface**: Common interface for coloring algorithms
  - Methods: solve(), get_solution(), get_metrics()
- **BacktrackingAlgorithm Class**: Implementation of backtracking search
  - Methods: solve(), is_safe(), assign_color(), etc.
- **GeneticAlgorithm Class**: Implementation of genetic algorithm
  - Methods: solve(), initialize_population(), crossover(), mutate(), select(), etc.

### 3. UI Module
- **UserInterface Class**: Main UI controller
  - Methods: run(), handle_input(), display_results()
- **GraphVisualizer Class**: Handles graph visualization
  - Methods: draw_graph(), update_colors(), animate_solution()
- **InputHandler Class**: Processes user inputs
  - Methods: get_graph_input(), get_algorithm_params()

### 4. Performance Module
- **MetricsCollector Class**: Collects and calculates performance metrics
  - Methods: start_timer(), end_timer(), calculate_chromatic_number(), etc.
- **ParameterTuner Class**: Handles parameter tuning for genetic algorithm
  - Methods: tune_parameters(), evaluate_performance(), suggest_parameters()

## Data Flow

1. User inputs graph data through UI
2. Graph Manager validates and creates graph representation
3. User selects algorithm and parameters
4. Selected algorithm processes the graph
5. Solution Manager receives and validates the solution
6. Performance metrics are calculated
7. Results are visualized and presented to the user
8. User can adjust parameters and rerun algorithms

## File Structure

```
graph_coloring_solver/
├── src/
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   └── graph_io.py
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
│   ├── performance/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── parameter_tuner.py
│   └── main.py
├── tests/
│   ├── test_graph.py
│   ├── test_backtracking.py
│   ├── test_genetic.py
│   └── test_visualization.py
├── data/
│   ├── sample_graphs/
│   └── results/
└── docs/
    ├── system_architecture.md
    └── user_guide.md
```

## Technology Stack
- **Programming Language**: Python 3.11
- **UI Framework**: Tkinter/PyQt for desktop application
- **Visualization**: Matplotlib/NetworkX for graph visualization
- **Testing**: Pytest for unit and integration testing

## Implementation Considerations
- Ensure modularity to allow independent development and testing
- Implement clear interfaces between components
- Design for extensibility to add more algorithms in the future
- Focus on performance optimization for large graphs
- Provide comprehensive visualization for educational purposes
