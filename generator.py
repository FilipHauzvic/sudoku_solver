from sudoku import Sudoku, Difficulty
from solver import Solver
import random
import time

class Generator():
    def __init__(self, difficulty = Difficulty.EASY):
        self.solver = Solver(Sudoku(difficulty))

    def generate(self):
        try:
            solution : Sudoku = self.solver.solve()
        except:
            raise Exception("Failed to generate a solution")
        # solution.print_board()
        # print("-----------------")
        clues = 0
        if solution.difficulty == Difficulty.EASY:
            clues = random.randint(32, 45)
        elif solution.difficulty == Difficulty.MEDIUM:
            clues = random.randint(26, 31)
        elif solution.difficulty == Difficulty.HARD:
            clues = random.randint(22, 25)
        elif solution.difficulty == Difficulty.EXPERT:
            clues = random.randint(17, 21)
        else:
            raise Exception("Invalid difficulty")
        
        while solution.get_number_of_clues() > clues:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if solution.get_cell(row, col) != 0:
                old_value = solution.get_cell(row, col)
                solution.set_cell(row, col, 0)
                tmp_solver = Solver(solution)
                if not tmp_solver.has_only_one_solution():
                    solution.set_cell(row, col, old_value)

        # solution.print_board()
        return solution                
