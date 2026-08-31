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

# Example usage
if __name__ == "__main__":
    arrGraph = [
        [0, 1, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0]
    ]
    iMaxColors = 3
    arrResult = arrSolveGraphColoring_Backtracking(arrGraph, iMaxColors)
    if arrResult:
        print("Coloring result:", arrResult)
    else:
        print("No valid coloring found with", iMaxColors, "colors.")
