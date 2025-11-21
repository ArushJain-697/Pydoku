from tabulate import tabulate
import random
import copy

# ---------------------------
# SIMPLE BACKTRACKING SOLVER
# ---------------------------
def find_empty(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None

def valid(grid, r, c, num):
    # row
    if num in grid[r]:
        return False
    # col
    for i in range(9):
        if grid[i][c] == num:
            return False
    # box
    br = (r // 3) * 3
    bc = (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == num:
                return False

    return True

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
        if valid(grid, r, c, num):
            grid[r][c] = num
            count += count_solutions(grid, limit)
            if count >= limit:
                break  # more than 1 solution
            grid[r][c] = 0

    grid[r][c] = 0
    return count

# -------------------------------------
# BALANCED REMOVAL ACROSS 3x3 BOXES
# -------------------------------------
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
    puzzle = copy.deepcopy(solution)
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
                if count_solutions(copy.deepcopy(puzzle)) == 1:
                    current_removed += 1
                else:
                    puzzle[r][c] = removed_value  # undo
    return puzzle
# ---------------------------
# TEST INPUT (VALID SOLUTION)
# ---------------------------
solution_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]
# ---------------------------
# MAIN — TESTING REMOVAL PART
# ---------------------------
difficulty = input("Enter difficulty (easy / medium / hard): ").strip().lower()
if difficulty not in difficulty_ranges:
    print("Invalid difficulty.")
    exit()

puzzle = make_balanced_puzzle(solution_grid, difficulty)
print("\nGenerated Sudoku Puzzle (" + difficulty + "):\n")
def display_sudoku(grid):
    printable = []
    for row in grid:
        printable.append([" " if x == 0 else x for x in row])
    print(tabulate(printable, tablefmt="fancy_grid"))
display_sudoku(puzzle)