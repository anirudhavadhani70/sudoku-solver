
import numpy as np
import tkinter as tk
from tkinter import messagebox


class SudokuSolver:
    def __init__(self, board):
        self.board = board

    # Function to check if placing a number in a given cell is valid
    def is_valid(self, num, row, col):
        # Check if the number is not already in the row, column, or 3x3 subgrid
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[subgrid_row_start + i][subgrid_col_start + j] == num:
                    return False
        return True

    # Backtracking function to solve the Sudoku board
    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # Find empty cell
                    for num in range(1, 10):
                        if self.is_valid(num, row, col):
                            self.board[row][col] = num
                            if self.solve():
                                return True
                            self.board[row][col] = 0  # Backtrack
                    return False
        return True


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = np.zeros((9, 9), dtype=int)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    # Create the 9x9 Sudoku grid using Entry widgets
    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=3, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.cells[row][col] = entry

    # Retrieve the current values from the Entry widgets
    def get_board(self):
        for row in range(9):
            for col in range(9):
                val = self.cells[row][col].get()
                if val.isdigit():
                    self.board[row][col] = int(val)
                else:
                    self.board[row][col] = 0

    # Update the grid with the solved Sudoku board
    def update_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(self.board[row][col]))

    # Function to clear the grid
    def clear_grid(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
        self.board = np.zeros((9, 9), dtype=int)

    # Solve the Sudoku puzzle and update the grid
    def solve_sudoku(self):
        self.get_board()
        solver = SudokuSolver(self.board)
        if solver.solve():
            self.update_board()
            messagebox.showinfo("Success", "Sudoku Solved!")
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku puzzle.")

    # Create buttons for solving and clearing the grid
    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku, font=("Arial", 14))
        solve_button.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid, font=("Arial", 14))
        clear_button.grid(row=9, column=5, columnspan=4, padx=10, pady=10)


# Main loop to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
