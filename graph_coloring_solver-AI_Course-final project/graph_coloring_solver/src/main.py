"""
Main module for the Graph Colouring Problem Solver.
"""

import tkinter as tk
from src.ui.interface import UserInterface

def main():
    """
    Main entry point for the application.
    """
    root = tk.Tk()
    app = UserInterface(root)
    app.run()

if __name__ == "__main__":
    main()
