from sudoku import Sudoku, Difficulty
from solver import Solver
import random
import time

class Generator():
    def generate(self, difficulty = Difficulty.EASY):
        # Create a solution from an empty board
        solver = Solver(Sudoku(difficulty))
        try:
            solution : Sudoku = solver.solve()
        except:
            raise Exception("Failed to generate a solution")
        
        clues = 0
        if difficulty == Difficulty.EASY:
            clues = random.randint(32, 45)
        elif difficulty == Difficulty.MEDIUM:
            clues = random.randint(26, 31)
        elif difficulty == Difficulty.HARD:
            clues = random.randint(22, 25)
        elif difficulty == Difficulty.EXPERT:
            clues = random.randint(17, 21)
        else:
            raise Exception("Invalid difficulty")

        for _ in range(81 - clues):
            # Get random cell that is not empty
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while solution.get_cell(row, col) == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)

            solution.set_cell(row, col, 0)
        
        return solution                
