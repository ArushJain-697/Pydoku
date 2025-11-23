from copy import deepcopy
from tabulate import tabulate
import random

def solve(N):
    emp = find_empty(N)
    if not emp:
        return True

    r, c = emp
    numbers = list(range(1, 10))
    random.shuffle(numbers)  

    for num in numbers:
        if valid(N, num, (r, c)):
            N[r][c] = num  

            if solve(N):
                return True  

            N[r][c] = 0  

    return False


def valid(board, num, pos):
    row, col = pos

    
    if any(board[row][i] == num for i in range(9)):
        return False

    if any(board[i][col] == num for i in range(9)):
        return False

    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def find_empty(N):
    for x in range(9):
        for y in range(9):
            if N[x][y] == 0:
                return (x, y)
    return None

def count_solutions(grid, limit=2):
    """
    Counts number of solutions up to 'limit'.
    Stops early if more than 1 solution found.
    """
    empty = find_empty(grid)
    if not empty:
        return 1
    r, c = empty
    count = 0
    for num in range(1, 10):
        if valid(grid,num,(r,c)):
            grid[r][c] = num
            count += count_solutions(grid, limit)
            if count >= limit:
                break  # more than 1 solution
            grid[r][c] = 0

    grid[r][c] = 0
    return count

difficulty_ranges = {
    "easy":   (32, 40),
    "medium": (41, 48),
    "hard":   (49, 54)
}

def get_box_cells(br, bc):
    cells = []
    for r in range(br * 3, br * 3 + 3):
        for c in range(bc * 3, bc * 3 + 3):
            cells.append((r, c))
    return cells

def make_balanced_puzzle(solution, difficulty):
    # number of removals needed
    low, high = difficulty_ranges[difficulty]
    removals_needed = random.randint(low, high)
    current_removed = 0
    puzzle = deepcopy(solution)
    # list of all 3×3 boxes
    boxes = [(br, bc) for br in range(3) for bc in range(3)]
    while current_removed < removals_needed:
        random.shuffle(boxes)  # random global cycle order
        for (br, bc) in boxes:
            if current_removed >= removals_needed:
                break

            box_cells = get_box_cells(br, bc)
            random.shuffle(box_cells)
            for (r, c) in box_cells:
                if current_removed >= removals_needed:
                    break

                if puzzle[r][c] == 0:
                    continue  # already removed

                removed_value = puzzle[r][c]
                puzzle[r][c] = 0

                # ensure uniqueness
                if count_solutions(deepcopy(puzzle)) == 1:
                    current_removed += 1
                else:
                    puzzle[r][c] = removed_value  # undo
    return puzzle

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
# Game loop
# ---------------------------
def play_game(initial_grid,solution):
    print("\n=== SUDOKU CLI ===\n")
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

        if not valid(grid, v,(r,c)):
            print("Move breaks Sudoku rules.")
            continue

        if v!=solution[r][c]:
            print("Wrong Answer")
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

l = [[0]*9 for _ in range(9)]
solve(l)

# ---------------------------
# MAIN — TESTING REMOVAL PART
# ---------------------------
difficulty = input("Enter difficulty (easy / medium / hard): ").strip().lower()
if difficulty not in difficulty_ranges:
    print("Invalid difficulty.")
    exit()

puzzle = make_balanced_puzzle(l, difficulty)
print("\nGenerated Sudoku Puzzle (" + difficulty + "):\n")

play_game(puzzle,l)                              
                    
          
