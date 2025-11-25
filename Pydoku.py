from copy import deepcopy
from tabulate import tabulate
import random

#ANSI codes
BOLD = "\033[1m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

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

    #Check Row
    if any(board[row][i] == num and i != col for i in range(9)):
        return False

    #Check Column
    if any(board[i][col] == num and i != row for i in range(9)):
        return False

    #Check Box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(N):
    for x in range(9):
        for y in range(9):
            if N[x][y] == 0:
                return (x, y)
    return None

def count_solutions(grid, limit=2):
    #Counts number of solutions up to 'limit'.
    #Stops early if more than 1 solution found.
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
                break
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
    low, high = difficulty_ranges[difficulty]
    removals_needed = random.randint(low, high)
    current_removed = 0
    puzzle = deepcopy(solution)
    #list of all 3×3 boxes
    boxes = [(br, bc) for br in range(3) for bc in range(3)]
    
    while current_removed < removals_needed:
        random.shuffle(boxes)
        for (br, bc) in boxes:
            if current_removed >= removals_needed:
                break

            box_cells = get_box_cells(br, bc)
            random.shuffle(box_cells)
            for (r, c) in box_cells:
                if current_removed >= removals_needed:
                    break

                if puzzle[r][c] == 0:
                    continue  #already removed

                removed_value = puzzle[r][c]
                puzzle[r][c] = 0

                #ensure uniqueness
                if count_solutions(deepcopy(puzzle)) == 1:
                    current_removed += 1
                else:
                    puzzle[r][c] = removed_value
    return puzzle

def display_sudoku(grid, initial_grid=None):
    table = []
    #1.Add Column numbers (Top Row)
    col_numbers = [""] + [f"{CYAN}{i+1}{RESET}" for i in range(9)]
    table.append(col_numbers)

    for r, row in enumerate(grid):
        #2.Add Row number (First Column)
        row_label = f"{CYAN}{r+1}{RESET}"
        
        display_row = [row_label]
        
        for c, val in enumerate(row):
            if val == 0:
                display_row.append("")
            else:
                #Logic: If it was 0 in initial_grid, it means User entered it -> YELLOW
                #If initial_grid is None (e.g. showing solution), just print normally
                if initial_grid and initial_grid[r][c] == 0:
                    display_row.append(f"{YELLOW}{val}{RESET}")
                else:
                    display_row.append(f"{val}") # Default White

        table.append(display_row)
    
    print(tabulate(table, tablefmt="fancy_grid", stralign="center"))

#Game loop
def play_game(initial_grid, solution):
    grid = deepcopy(initial_grid)
    
    hints_remaining = 5

    #Display initial state
    display_sudoku(grid, initial_grid)
    print_help(hints_remaining)

    while True:
        cmd = input(f"\n{BOLD}Enter (row col num) | hint ({hints_remaining} left) | quit | help:{RESET} ").strip().lower()

        if cmd == "quit":
            print(f"{BOLD}Thanks for playing!{RESET}")
            print(tabulate(solution, tablefmt="fancy_grid", stralign="center"))
            return

        if cmd == "help":
            print_help(hints_remaining)
            continue
        
        if cmd == "secret":
            display_sudoku(solution)
            continue

        #---HINT LOGIC---
        if cmd == "hint":
            if hints_remaining <= 0:
                print(f"{BOLD}No hints remaining!{RESET}")
                continue
            
            found_action = False
            
            #Priority 1: Fix Mistakes
            for r in range(9):
                for c in range(9):
                    #If cell is filled (not 0) AND incorrect
                    if grid[r][c] != 0 and grid[r][c] != solution[r][c]:
                        print(f"{BOLD}Hint → Found a mistake at ({r+1},{c+1}). Fixing {grid[r][c]} to {solution[r][c]}.{RESET}")
                        grid[r][c] = solution[r][c]
                        hints_remaining -= 1 
                        found_action = True
                        display_sudoku(grid, initial_grid)
                        if all(cell != 0 for row in grid for cell in row):
                            if grid == solution:
                                print(f"\n{BOLD}🎉 Congratulations! You solved the puzzle! 🎉{RESET}\n")
                                return
                        break
                if found_action: break
            
            #Priority 2: Fill Empty Cell
            if not found_action:
                for r in range(9):
                    for c in range(9):
                        if grid[r][c] == 0:
                            grid[r][c] = solution[r][c]
                            print(f"{BOLD}Hint → Filled empty cell ({r+1},{c+1}) with {solution[r][c]}{RESET}")
                            hints_remaining -= 1
                            found_action = True
                            display_sudoku(grid, initial_grid)
                            if all(cell != 0 for row in grid for cell in row):
                                if grid == solution:
                                    print(f"\n{BOLD}🎉 Congratulations! You solved the puzzle! 🎉{RESET}\n")
                                    return
                            break
                    if found_action: break
            
            if found_action:
                print(f"{BOLD}({hints_remaining} hints left){RESET}")
            else:
                print(f"{BOLD}Puzzle is already solved or no hints available.{RESET}")
            continue

        #---INPUT PARSING---
        try:
            parts = cmd.split()
            if len(parts) != 3:
                raise ValueError
            r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
        except:
            print(f"{BOLD}Invalid format. Use: row col num (e.g., '4 5 9'){RESET}")
            continue

        #---CHECKS---
        #Allow 0 to delete a number, otherwise 1-9
        if not (0 <= r < 9 and 0 <= c < 9 and 0 <= v <= 9):
            print(f"{BOLD}Row/col must be 1-9. Value must be 1-9 (or 0 to clear).{RESET}")
            continue

        elif initial_grid[r][c] != 0:
            print(f"{BOLD}Cannot change a fixed cell (part of original puzzle).{RESET}")
            continue

        #Only validate if v is not 0 (because 0 is just clearing)
        elif v != 0 and not valid(grid, v, (r, c)):
            print(f"{BOLD}Invalid Move: {v} already exists in that Row, Column, or Box.{RESET}")
            continue

        #---EXECUTE MOVE (REPLACE/ADD/DELETE)---
        grid[r][c] = v  # This works for both adding AND replacing!
        display_sudoku(grid, initial_grid)

        #---WIN / FULL CHECK---
        #Only check if board is full (no 0s)
        if all(cell != 0 for row in grid for cell in row):
            if grid == solution:
                print(f"\n{BOLD}🎉 Congratulations! You solved the puzzle! 🎉{RESET}\n")
                return
            else:
                #Calculate errors
                errors = sum(1 for r in range(9) for c in range(9) if grid[r][c] != solution[r][c])
                print(f"\n{BOLD}⚠️ Board is full, but incorrect! You have {errors} errors.{RESET}")
                print(f"{BOLD}Use 'hint' or overwrite the wrong numbers to fix them.{RESET}")
                #Loop continues automatically... user can type "row col num" to fix

def print_help(hints_remaining):
    print(f"""{BOLD}
Commands:
  row col num  → place number at (row, col). Example: 4 3 9
  row col 0    → delete number at (row,col). Example: 4 3 0
  row col new  → replace number at (row,col). Example 4 3 5
  hint         → fix a mistake OR fill an empty cell ({hints_remaining} remaining)
  quit         → exit the game
  help         → show this message
{RESET}""")

#MAIN
print(f"\n{BOLD}=================== SUDOKU CLI ===================={RESET}\n")
l = [[0]*9 for _ in range(9)]
solve(l)

difficulty = input(f"{BOLD}Enter difficulty (easy / medium / hard):{RESET} ").strip().lower()
if difficulty not in difficulty_ranges:
    print(f"{BOLD}Invalid difficulty. Defaulting to easy.{RESET}")
    difficulty = "easy"

puzzle = make_balanced_puzzle(l, difficulty)
print(f"\n{BOLD}Generated Sudoku Puzzle ({difficulty}):{RESET}\n")

play_game(puzzle, l)