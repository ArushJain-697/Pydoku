###Pydoku

A CLI-based Sudoku game written in Python.
It uses the tabulate module to print a neat and readable Sudoku grid on the terminal.

##Project Description

Pydoku is a command-line Sudoku game where the player chooses a difficulty level and solves the puzzle directly in the terminal.
The project focuses on clean output formatting, simple logic, and an easy way for the player to enter moves.

##How the Game Works
Choosing a Difficulty

When the program starts, it asks the player to pick a difficulty level:

Easy

Medium

Hard

The difficulty decides how many numbers are removed from the board.

##Making Moves

After the grid is shown, the player enters:

Row number

Column number

Value to place

The board updates after every valid move.

##How We Generate the Sudoku Grid
#Step 1: Create a Full Solution

We first generate a complete 9×9 Sudoku solution.

#Step 2: Remove Numbers Based on Difficulty

Easy: fewer numbers removed

Medium: moderate amount removed

Hard: many numbers removed

Only these visible numbers are shown to the player.

#Step 3: Display With Tabulate

We use the tabulate module to print the Sudoku grid with clear lines and spacing.

Features

##CLI interface

Three difficulty levels

Nicely formatted board using tabulate

Input validation

Random puzzle generation

##What We Learned

During the project we learned:

Working with nested lists

Creating and modifying a Sudoku board

Using tabulate for cleaner output

Handling and validating user input

Structuring functions and game loops

Writing clearer Python code
