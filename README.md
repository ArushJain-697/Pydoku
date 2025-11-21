# Pydoku

A CLI-based Sudoku game written in Python.  
It uses the tabulate module to print a clean and readable Sudoku grid on the terminal.

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

## Features

- Command-line interface  
- Three difficulty levels  
- Cleanly formatted board using tabulate  
- Input validation  
- Random Sudoku puzzle generation  

## What We Learned

While working on this project, we learned:

- How to work with nested lists  
- How to generate and modify a Sudoku grid  
- How to use tabulate for table formatting  
- How to handle and validate user input  
- How to structure functions and loops  
- How to write cleaner Python code  

## How to Run the Game

- Install tabulate: pip install tabulate
- Run the file in your terminal: python Pydoku.py
- Make sure all the files are present where you are running the file
