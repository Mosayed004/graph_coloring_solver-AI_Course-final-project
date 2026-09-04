# 🎨 Graph Coloring Problem Solver (AI Constraint Satisfaction GUI)

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg?logo=python)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-68A063.svg)]()
[![Graph Library](https://img.shields.io/badge/NetworkX-Graph%20Theory-blue.svg?logo=networkx)](https://networkx.org/)
[![AI CSP](https://img.shields.io/badge/AI-Constraint%20Satisfaction-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> An interactive graphical desktop application implementing Artificial Intelligence Constraint Satisfaction Problem (CSP) algorithms to solve the NP-complete Graph Vertex Coloring problem. Built using Python, Tkinter, NetworkX, and Matplotlib.

---

## 📌 Problem Overview

The **Graph Coloring Problem (GCP)** is a canonical NP-hard problem in discrete mathematics and artificial intelligence:
> Given an undirected graph $G = (V, E)$, assign a color to each vertex $v \in V$ such that no two adjacent vertices share the same color ($c(u) \neq c(v)$ for all $(u, v) \in E$), while minimizing the total number of colors used (the **chromatic number** $\chi(G)$).

Applications include compiler register allocation, frequency assignment in telecommunications, university exam timetabling, and air traffic scheduling.

---

## ✨ Features & Interactive GUI Capabilities

- **🖥️ Full Interactive Desktop Canvas:** Built with `tkinter` and `FigureCanvasTkAgg` in a responsive 1200x800 workspace.
- **🕸️ Dynamic Graph Creation:**
  - Add, move, and connect vertices with real-time visual feedback.
  - Generate randomized connected graphs with customizable vertex and edge densities.
- **🧠 Intelligent AI Solvers & Heuristics:**
  - **Backtracking Search:** Exhaustive recursive exploration with pruning.
  - **MRV Heuristic (Minimum Remaining Values / Most Constrained Variable):** Prioritizes vertices with the fewest legal color choices.
  - **Degree Heuristic:** Breaks ties by selecting vertices involved in the highest number of constraints on remaining uncolored variables.
  - **Forward Checking:** Proactively reduces color domains of neighboring vertices to detect early dead-ends.
  - **Greedy / Welsh-Powell Heuristics:** Rapid polynomial-time approximation.
- **📊 Real-time Analytics & Animation:**
  - Visual step-by-step coloring animation showing algorithm decisions.
  - Performance metrics display: Execution time (ms), iterations/backtracks count, and minimum colors achieved.

---

## 🏗️ Repository Layout

```
graph_coloring_solver-AI_Course-final-project/
├── graph_coloring_solver-AI_Course-final project/
│   ├── Final.py                   # Main executable desktop GUI application
│   ├── G C.docx                   # Project documentation & theoretical report
│   ├── Graph Colour.zip           # Standalone source package
│   ├── Graph Colour/              # Additional resources & test matrices
│   ├── PROJECT 1/                 # Initial prototyping and baseline code
│   └── workspace.code-workspace   # VS Code workspace settings
```

---

## 🚀 Getting Started & How to Run

### Prerequisites
Ensure Python 3.8+ is installed with the following packages:
```bash
pip install networkx matplotlib numpy
```
*(Tkinter comes pre-installed with standard Python distributions on Windows).*

### Launching the Application
```bash
cd "graph_coloring_solver-AI_Course-final project"
python Final.py
```

### Usage Workflow in the GUI:
1. Use the control panel to generate a sample graph or click on the canvas to add nodes.
2. Select your desired AI heuristic (e.g., Backtracking + MRV + Degree Heuristic).
3. Click **Solve** to visualize the optimal coloring and view performance metrics!

---

## 👤 Author

Developed by **Mohamed Sayed** ([@Mosayed004](https://github.com/Mosayed004)).
Licensed under the **MIT License**.
