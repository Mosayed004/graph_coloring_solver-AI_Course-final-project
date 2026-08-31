from __future__ import annotations

import argparse
import random
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import streamlit as st
except ModuleNotFoundError:
    st = None

import matplotlib.pyplot as plt
import networkx as nx
import unittest

Colouring = Dict[int, int]


class Graph:
    def __init__(self):
        self.adj: Dict[int, List[int]] = defaultdict(list)

    @classmethod
    def from_edges(cls, edges: List[Tuple[int, int]]) -> "Graph":
        g = cls()
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def add_edge(self, u: int, v: int):
        if v not in self.adj[u]:
            self.adj[u].append(v)
            self.adj[v].append(u)

    def vertices(self) -> List[int]:
        return list(self.adj)

    def order(self) -> int:
        return len(self.adj)


class BacktrackingSolver:
    def __init__(self, graph: Graph):
        self.g = graph
        self.vs = sorted(graph.vertices(), key=lambda v: len(graph.adj[v]), reverse=True)
        self.n = len(self.vs)

    def solve(self) -> Tuple[Colouring, int]:
        colours = 1
        assignment: Colouring = {}

        def safe(v: int, c: int) -> bool:
            return all(assignment.get(n) != c for n in self.g.adj[v])

        def dfs(i: int) -> bool:
            if i == self.n:
                return True
            v = self.vs[i]
            for c in range(colours):
                if safe(v, c):
                    assignment[v] = c
                    if dfs(i + 1):
                        return True
                    assignment.pop(v)
            return False

        while not dfs(0):
            colours += 1
            assignment.clear()
        return assignment, colours


class GASolver:
    def __init__(
        self,
        graph: Graph,
        pop: int = 100,
        gens: int = 300,
        cx_rate: float = 0.8,
        mut_rate: float = 0.02,
        seed: Optional[int] = None,
    ):
        self.g = graph
        self.n = graph.order()
        self.pop = pop
        self.gens = gens
        self.cx = cx_rate
        self.mut = mut_rate
        self.rnd = random.Random(seed)
        self.history: List[int] = []

    def _rand_ind(self, k: int) -> List[int]:
        return [self.rnd.randrange(k) for _ in range(self.n)]

    def _conflicts(self, ind: List[int]) -> int:
        return sum(
            1
            for v in range(self.n)
            for n in self.g.adj[v]
            if v < n and ind[v] == ind[n]
        )

    def _select(self, pop: List[List[int]], fits: List[int]) -> List[int]:
        best = None
        for _ in range(3):
            i = self.rnd.randrange(self.pop)
            if best is None or fits[i] < fits[best]:
                best = i
        return pop[best][:]

    def _cross(self, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        if self.rnd.random() > self.cx or self.n < 2:
            return a[:], b[:]
        pt = self.rnd.randrange(1, self.n - 1)
        return a[:pt] + b[pt:], b[:pt] + a[pt:]

    def _mutate(self, ind: List[int], k: int):
        for i in range(self.n):
            if self.rnd.random() < self.mut:
                ind[i] = self.rnd.randrange(k)

    def solve(self) -> Tuple[Colouring, int, List[int]]:
        k = self.n
        pop = [self._rand_ind(k) for _ in range(self.pop)]
        best = pop[0]
        best_fit = self._conflicts(best)

        for _ in range(self.gens):
            fits = [self._conflicts(ind) for ind in pop]
            for ind, f in zip(pop, fits):
                if f < best_fit:
                    best, best_fit = ind[:], f
            self.history.append(best_fit)
            if best_fit == 0:
                break
            new: List[List[int]] = []
            while len(new) < self.pop:
                p1, p2 = self._select(pop, fits), self._select(pop, fits)
                c1, c2 = self._cross(p1, p2)
                self._mutate(c1, k)
                self._mutate(c2, k)
                new.extend([c1, c2])
            pop = new[: self.pop]

        palette: Dict[int, int] = {}
        nxt = 0
        colouring: Colouring = {}
        for v, c in enumerate(best):
            if c not in palette:
                palette[c] = nxt
                nxt += 1
            colouring[v] = palette[c]
        return colouring, nxt, self.history


def valid(graph: Graph, col: Colouring) -> bool:
    return all(col[u] != col[v] for u in graph.vertices() for v in graph.adj[u])

def read_edges(path: str | Path):
    edges: List[Tuple[int, int]] = []
    with open(path) as f:
        for ln in f:
            p = ln.strip().split()
            if len(p) == 2:
                edges.append(tuple(map(int, p)))
    return Graph.from_edges(edges)

def draw_graph(g: Graph, col: Colouring, fitness: Optional[List[int]] = None):
    fig, ax = plt.subplots(1, 2 if fitness else 1, figsize=(8, 4))
    if fitness:
        ax0, ax1 = ax
    else:
        ax0 = ax
    nx_g = nx.Graph()
    nx_g.add_nodes_from(g.vertices())
    nx_g.add_edges_from((u, v) for u in g.adj for v in g.adj[u] if u < v)
    nx.draw_networkx(nx_g, node_color=[col[v] for v in nx_g], cmap=plt.cm.Set3, ax=ax0)
    ax0.set_axis_off()
    ax0.set_title("Coloured graph")
    if fitness:
        ax1.plot(fitness)
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Conflicts")
        ax1.set_title("GA fitness")
    plt.tight_layout()
    plt.show()

def launch_ui():
    if st is None:
        print("Streamlit غير مثبت. ثبِّته ثم جرّب --ui")
        return
    st.title("Graph Colouring Solver")
    uploaded = st.file_uploader("Upload edge list (u v per line)")
    algo = st.radio("Algorithm", ["Backtracking", "Genetic Algorithm"])
    if algo == "Genetic Algorithm":
        pop = st.slider("Population", 50, 400, 150, 50)
        gens = st.slider("Generations", 100, 1000, 300, 100)
        mut = st.slider("Mutation rate", 0.0, 0.1, 0.02, 0.01)
    if st.button("Run"):
        if uploaded is None:
            st.warning("Please upload a file.")
            return
        g = read_edges(uploaded)
        if algo == "Backtracking":
            col, k = BacktrackingSolver(g).solve()
            st.write(f"Chromatic number: {k}")
            draw_graph(g, col)
        else:
            col, k, hist = GASolver(g, pop, gens, mut_rate=mut).solve()
            st.write(f"Colours used: {k}")
            draw_graph(g, col, hist)

class _Tests(unittest.TestCase):
    def setUp(self):
        self.g = Graph.from_edges([(0, 1), (1, 2), (2, 0), (0, 3)])

    def test_backtracking(self):
        col, k = BacktrackingSolver(self.g).solve()
        self.assertTrue(valid(self.g, col))
        self.assertEqual(k, 3)

    def test_ga(self):
        col, k, hist = GASolver(self.g, pop=60, gens=400, seed=42).solve()
        self.assertTrue(valid(self.g, col))
        self.assertLessEqual(k, 3)
        self.assertGreaterEqual(len(hist), 1)

def main(argv: Optional[List[str]] = None):
    p = argparse.ArgumentParser(description="Graph Colouring Solver")
    p.add_argument("--input", help="Edge list file (default: built-in example)")
    p.add_argument("--algo", choices=["bt", "ga"], default="bt", help="Algorithm")
    p.add_argument("--population", type=int, default=150, help="GA population")
    p.add_argument("--generations", type=int, default=300, help="GA generations")
    p.add_argument("--mutation", type=float, default=0.02, help="GA mutation rate")
    p.add_argument("--ui", action="store_true", help="Launch Streamlit app")
    p.add_argument("--test", action="store_true", help="Run internal tests")
    args = p.parse_args(argv)

    if args.test:
        unittest.main(argv=[sys.argv[0]], exit=False)
        return
    if args.ui:
        launch_ui()
        return
    g = read_edges(args.input) if args.input else Graph.from_edges([(0, 1), (1, 2), (2, 0), (0, 3)])
    t0 = time.time()
    if args.algo == "bt":
        col, k = BacktrackingSolver(g).solve()
        fitness = None
    else:
        col, k, fitness = GASolver(
            g,
            pop=args.population,
            gens=args.generations,
            mut_rate=args.mutation,
        ).solve()
    dt = time.time() - t0
    print(f"Colours used: {k}\tRuntime: {dt:.3f}s")
    draw_graph(g, col, fitness)

if __name__ == "__main__":
    main()
