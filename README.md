# Pydoku

A CLI-based Sudoku game written in Python.  

## Project Description

Pydoku is a command-line Sudoku game where the player chooses a difficulty level and solves the puzzle directly in the terminal.  
The project focuses on clean output formatting, simple puzzle logic, and an easy way for the player to enter moves.

## How the Game Works

### Choosing a Difficulty
When the program starts, it asks the player to select a difficulty level:

- Easy  
- Medium  
- Hard  

The difficulty level determines how many numbers are removed from the complete Sudoku grid.

### Making Moves
After the grid is displayed, the player enters:

- Row  
- Column  
- Value

The board updates after each valid move.

### Deleting a cell

- Player can enter row, column and 0
- The cell gets reset to empty
- Player cannot remove the default cells

### Hint system

- Player can use atmost 3 hints
- It fills the nearest empty cell to top left
- Before that if it finds a wrongly filled cell then it gets corrected
- If the user quits then solution is displayed and program stops running

## How We Generate the Sudoku Grid

### Step 1: Create a Full Solution
A complete 9×9 Sudoku solution is generated.

### Step 2: Remove Numbers Based on Difficulty
- Easy: fewer cells removed  
- Medium: a moderate number removed  
- Hard: many cells removed  

These visible numbers form the puzzle given to the player.

### Step 3: Display With Tabulate
The tabulate module is used to show the grid with neat lines and spacing. 

## What We Learned
While working on this project, we learned:

- How to work with nested lists
- Backtracking algorithm
- How to generate and modify a Sudoku grid
- How to use tabulate for table formatting
- How to handle and validate user input
- How to structure functions and loops

## How to Run the Game

- Install tabulate: pip install tabulate
- Run the file in your terminal: python Pydoku.py
- Make sure you are running the file in the directory in which is present
