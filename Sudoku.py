from tabulate import tabulate
def display_sudoku(grid):
    table = []
    for i, row in enumerate(grid):
        # Insert row separator every 3 rows except the top
        if i % 3 == 0 and i != 0:
            table.append([""] * 9)

        new_row = []
        for j, n in enumerate(row):
            # Insert column separators every 3 columns except the first
            if j % 3 == 0 and j != 0:
                new_row.append("")
            new_row.append(n)
        table.append(new_row)
    print(tabulate(table, tablefmt="fancy_grid"))

l= [[1,2,3,4,5,6,7,8,9],
    [2,3,4,5,6,7,8,9,1],
    [3,4,5,6,7,8,9,1,2],
    [4,5,6,7,8,9,1,2,3],
    [5,6,7,8,9,1,2,3,4],
    [6,7,8,9,1,2,3,4,5],
    [7,8,9,1,2,3,4,5,6],
    [8,9,1,2,3,4,5,6,7],
    [9,1,2,3,4,5,6,7,8]]

display_sudoku(l)