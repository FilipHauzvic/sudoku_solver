from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

class Sudoku():
    def __init__(self, difficulty = Difficulty.MEDIUM):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.valid_values = [[[val for val in range(1, 10)] for i in range(9)] for j in range(9)]
        self.difficulty = difficulty

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=" ")
            print()

    def get_board(self):
        return self.board

    def set_cell(self, row, col, value):
        self.update_valid_values(row, col, value, self.get_cell(row, col))
        self.board[row][col] = value

    def get_cell(self, row, col):
        return self.board[row][col]

    def update_valid_values(self, row, col, value, old_value):
        if value in range(1, 10):
            for i in range(9):
                if value in self.valid_values[row][i]:
                    self.valid_values[row][i].remove(value)
                if value in self.valid_values[i][col]:
                    self.valid_values[i][col].remove(value)
            start_row = row - row % 3
            start_col = col - col % 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if value in self.valid_values[i][j]:
                        self.valid_values[i][j].remove(value)
        elif value == 0:
            if old_value == 0:
                return
            for i in range(9):
                if old_value not in self.valid_values[row][i]:
                    self.valid_values[row][i].append(old_value)
                if old_value not in self.valid_values[i][col]:
                    self.valid_values[i][col].append(old_value)
            start_row = row - row % 3
            start_col = col - col % 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if old_value not in self.valid_values[i][j]:
                        self.valid_values[i][j].append(old_value)
        else:
            raise Exception("Invalid value")


    def copy_board(self, board):
        for i in range(9):
            for j in range(9):
                self.set_cell(i, j, board.get_cell(i, j))

    def row_contains(self, row, value):
        for i in range(9):
            if self.board[row][i] == value:
                return True
        return False
    
    def col_contains(self, col, value):
        for i in range(9):
            if self.board[i][col] == value:
                return True
        return False
    
    def box_contains(self, row, col, value):
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == value:
                    return True
        return False
    
    def is_valid(self):
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) != 0:
                    if self.row_contains(i, self.get_cell(i, j)) or self.col_contains(j, self.get_cell(i, j)) or self.box_contains(i, j, self.get_cell(i, j)):
                        return False
        return True
    
    def can_set(self, row, col, value):
        return value in self.valid_values[row][col]

    def can_solve(self):
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) == 0:
                    if len(self.valid_values[i][j]) == 0:
                        return False
        return True

    def is_solved(self):
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) == 0:
                    return False
        return True
    
    def get_number_of_clues(self):
        clues = 0
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) != 0:
                    clues += 1
        return clues