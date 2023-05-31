from sudoku import Sudoku
import random
import time

class Solver():
    def __init__(self, sudoku : Sudoku):
        self.open = [sudoku]

    def solve(self):
        while len(self.open) > 0:
            current = self.open.pop()
            # current.print_board()
            # print("-----------------")
            # time.sleep(1)
            if current.is_solved():
                return current
            else:
                self.expand(current)
        raise Exception("No solution found")

    def has_only_one_solution(self):
        count = 0
        while len(self.open) > 0:
            current = self.open.pop()
            if current.is_solved():
                count += 1
                if count > 1:
                    return False
            else:
                self.expand(current)
        return True

    def expand(self, sudoku : Sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku.get_cell(i, j) == 0:
                    for val in random.sample(sudoku.valid_values[i][j], len(sudoku.valid_values[i][j])):
                        if sudoku.can_set(i, j, val):
                            new_sudoku = Sudoku()
                            new_sudoku.copy_board(sudoku)
                            new_sudoku.set_cell(i, j, val)
                            if new_sudoku.can_solve():
                                self.open.append(new_sudoku)
                    return