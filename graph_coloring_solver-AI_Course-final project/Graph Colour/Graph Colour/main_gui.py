import tkinter as tk
from tkinter import messagebox
import random

# ===== BACKTRACKING FUNCTIONS =====
def bIsSafe(arrGraph, arrColors, iVertex, iColor):
    for iNeighbor in range(len(arrGraph)):
        if arrGraph[iVertex][iNeighbor] == 1 and arrColors[iNeighbor] == iColor:
            return False
    return True

def bBacktrackColoring(arrGraph, iMaxColors, arrColors, iVertex=0):
    if iVertex == len(arrGraph):
        return True

    for iColor in range(1, iMaxColors + 1):
        if bIsSafe(arrGraph, arrColors, iVertex, iColor):
            arrColors[iVertex] = iColor
            if bBacktrackColoring(arrGraph, iMaxColors, arrColors, iVertex + 1):
                return True
            arrColors[iVertex] = 0  # backtrack
    return False

def arrSolveGraphColoring_Backtracking(arrGraph, iMaxColors):
    arrColors = [0] * len(arrGraph)
    if bBacktrackColoring(arrGraph, iMaxColors, arrColors):
        return arrColors
    else:
        return None

# ===== GENETIC FUNCTIONS =====
def arrCreateChromosome(iNumVertices, iMaxColors):
    return [random.randint(1, iMaxColors) for _ in range(iNumVertices)]

def iFitness(arrGraph, arrChromosome):
    iConflicts = 0
    for i in range(len(arrGraph)):
        for j in range(i + 1, len(arrGraph)):
            if arrGraph[i][j] == 1 and arrChromosome[i] == arrChromosome[j]:
                iConflicts += 1
    return iConflicts

def arrSelectParents(arrPopulation, arrFitness):
    arrSorted = sorted(zip(arrPopulation, arrFitness), key=lambda x: x[1])
    return arrSorted[0][0], arrSorted[1][0]

def arrCrossover(arrParent1, arrParent2):
    iPoint = random.randint(1, len(arrParent1) - 2)
    return arrParent1[:iPoint] + arrParent2[iPoint:]

def arrMutate(arrChromosome, iMaxColors, fMutationRate=0.1):
    for i in range(len(arrChromosome)):
        if random.random() < fMutationRate:
            arrChromosome[i] = random.randint(1, iMaxColors)
    return arrChromosome

def arrSolveGraphColoring_Genetic(arrGraph, iMaxColors, iPopulationSize=100, iMaxGenerations=1000):
    iNumVertices = len(arrGraph)
    arrPopulation = [arrCreateChromosome(iNumVertices, iMaxColors) for _ in range(iPopulationSize)]

    for _ in range(iMaxGenerations):
        arrFitnessValues = [iFitness(arrGraph, chrom) for chrom in arrPopulation]
        if 0 in arrFitnessValues:
            return arrPopulation[arrFitnessValues.index(0)]

        arrNewPopulation = []
        for _ in range(iPopulationSize):
            parent1, parent2 = arrSelectParents(arrPopulation, arrFitnessValues)
            child = arrCrossover(parent1, parent2)
            arrNewPopulation.append(arrMutate(child, iMaxColors))

        arrPopulation = arrNewPopulation

    return None

# ===== GUI =====
def run_solver():
    try:
        iVertices = int(entry_vertices.get())
        iMaxColors = int(entry_colors.get())
        sEdges = entry_edges.get().strip()
        arrGraph = [[0]*iVertices for _ in range(iVertices)]

        if sEdges:
            lstEdges = sEdges.split(',')
            for edge in lstEdges:
                i1, i2 = map(int, edge.strip().split('-'))
                arrGraph[i1][i2] = 1
                arrGraph[i2][i1] = 1

        sAlgo = algo_var.get()
        if sAlgo == "Backtracking":
            arrResult = arrSolveGraphColoring_Backtracking(arrGraph, iMaxColors)
        else:
            arrResult = arrSolveGraphColoring_Genetic(arrGraph, iMaxColors)

        if arrResult:
            messagebox.showinfo("Result", f"Coloring successful:\n{arrResult}")
        else:
            messagebox.showerror("Error", "No valid coloring found.")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Window
window = tk.Tk()
window.title("Graph Coloring Solver")

tk.Label(window, text="Number of Vertices:").grid(row=0, column=0, sticky="w")
entry_vertices = tk.Entry(window)
entry_vertices.grid(row=0, column=1)

tk.Label(window, text="Number of Colors:").grid(row=1, column=0, sticky="w")
entry_colors = tk.Entry(window)
entry_colors.grid(row=1, column=1)

tk.Label(window, text="Edges (e.g. 0-1,1-2):").grid(row=2, column=0, sticky="w")
entry_edges = tk.Entry(window)
entry_edges.grid(row=2, column=1)

tk.Label(window, text="Algorithm:").grid(row=3, column=0, sticky="w")
algo_var = tk.StringVar(value="Backtracking")
tk.OptionMenu(window, algo_var, "Backtracking", "Genetic").grid(row=3, column=1)

tk.Button(window, text="Solve", command=run_solver, bg="lightblue").grid(row=4, column=0, columnspan=2, pady=10)

window.mainloop()