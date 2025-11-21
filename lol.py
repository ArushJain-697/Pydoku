#!/usr/bin/env python3
"""
sudoku_cli.py

A simple command-line Sudoku game.
Features:
- Difficulty selection (placeholder hook for generator)
- Tabulate-based board display
- Hint (fills one correct cell using internal solver)
- Basic rule-checking and fixed-cell protection

Requires:
    pip install tabulate
"""

from copy import deepcopy
from tabulate import tabulate

N = 9

# ---------------------------
# Solver (backtracking)
# ---------------------------
def is_safe(grid, row, col, num):
    for x in range(N):
        if (grid[row][x] == num or
            grid[x][col] == num or
            grid[row - row % 3 + x // 3][col - col % 3 + x % 3] == num):
            return False
    return True

def solve(grid, row=0, col=0):
    if row == N - 1 and col == N:
        return True
    if col == N:
        row += 1
        col = 0
    if grid[row][col] != 0:
        return solve(grid, row, col + 1)
    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if solve(grid, row, col + 1):
                return True
            grid[row][col] = 0
    return False

# ---------------------------
# Display
# ---------------------------
def display_sudoku(grid):
    table = []
    for i, row in enumerate(grid):
        display_row = [x if x != 0 else " " for x in row]
        table.append(display_row)
    print(tabulate(table, tablefmt="fancy_grid"))

# ---------------------------
# Puzzle generator (placeholder)
# ---------------------------
def get_puzzle_by_difficulty(difficulty: str):
    """
    Placeholder hook.
    Returns (initial_grid, solution_grid).
    Replace with actual generator based on difficulty.
    """
    initial = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    sol = deepcopy(initial)
    solve(sol)
    return initial, sol

# ---------------------------
# Game loop
# ---------------------------
def play_game():
    print("\n=== SUDOKU CLI ===\n")
    
    while True:
        difficulty = input("Choose difficulty (easy / medium / hard) or 'quit' to exit: ").strip().lower()
        if difficulty == "quit":
            print("Bye!")
            return
        if difficulty in ("easy", "medium", "hard"):
            break
        print("Please type one of: easy, medium, hard")

    print(f"\nLoading {difficulty} puzzle...\n")
    initial_grid, solution = get_puzzle_by_difficulty(difficulty)
    grid = deepcopy(initial_grid)
    
    hints_remaining = 3

    display_sudoku(grid)
    print_help(hints_remaining)

    while True:
        cmd = input(f"\nEnter (row col num) | hint ({hints_remaining} left) | quit | help: ").strip().lower()

        if cmd == "quit":
            print("Thanks for playing!")
            return

        if cmd == "help":
            print_help(hints_remaining)
            continue

        if cmd == "hint":
            if hints_remaining <= 0:
                print("No hints remaining!")
                continue
            found = False
            for r in range(9):
                for c in range(9):
                    if grid[r][c] == 0:
                        grid[r][c] = solution[r][c]
                        hints_remaining -= 1
                        print(f"Hint -> Filled ({r+1},{c+1}) with {solution[r][c]} ({hints_remaining} hints left)")
                        display_sudoku(grid)
                        found = True
                        break
                if found:
                    break
            if not found:
                print("No empty cells left!")
            continue

        # Parse move: row col value
        try:
            parts = cmd.split()
            r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
        except:
            print("Invalid format. Type 'help' for instructions.")
            continue

        if not (0 <= r < 9 and 0 <= c < 9 and 1 <= v <= 9):
            print("Row/col must be 1-9, value must be 1-9.")
            continue

        if initial_grid[r][c] != 0:
            print("Cannot change a fixed cell.")
            continue

        if not is_safe(grid, r, c, v):
            print("Move breaks Sudoku rules.")
            continue

        grid[r][c] = v
        display_sudoku(grid)

        # Check win
        if all(cell != 0 for row in grid for cell in row):
            if grid == solution:
                print("\n🎉 Congratulations! You solved the puzzle! 🎉\n")
                return
            else:
                print("Board is full but incorrect. Keep trying!")

def print_help(hints_remaining):
    print(f"""
Commands:
  row col num  -> place number at (row, col). Example: 4 3 9
  hint         -> fills one correct empty cell ({hints_remaining} remaining)
  quit         -> exit the game
  help         -> show this message
""")

if __name__ == "__main__":
    play_game()