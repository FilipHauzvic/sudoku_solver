from sudoku import Sudoku, Difficulty
from generator import Generator
import threading

import tkinter as tk
from tkinter import ttk
import tkinter.font as font

def create_board(window, sudoku):
    board_frame = tk.Frame(window)
    board_frame.grid(row = 0, column = 1)
    for i in range(9):
        for j in range(9):
            cell = tk.Entry(board_frame, width=2, justify="center", font=("Arial", 20))
            cell.grid(row=i, column=j)
            cell_value = sudoku.get_cell(i, j)
            if cell_value != 0:
                cell.insert(0, cell_value)
            else:
                cell.insert(0, "")

def adjust_column_width(window, column_index):
    widgets = window.grid_slaves(column=column_index)
    max_width = max(widget.winfo_width() for widget in widgets)
    window.columnconfigure(column_index, minsize=max_width)

def generate_threaded(window):
    threading.Thread(target=generate, args=(window,)).start()

def generate(window):
    generator = Generator()
    sudoku : Sudoku = None
    try:
        sudoku = generator.generate()
    except Exception as e:
        print(e)
        exit(1)
    sudoku.print_board()
    create_board(window, sudoku)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sudoku")
    window.geometry("750x500")

    style = ttk.Style(window)
    window.tk.call('source', 'breeze-dark/breeze-dark.tcl')
    style.theme_use('breeze-dark')

    menu_frame = tk.Frame(window)
    menu_frame.grid(row = 0, column = 0, sticky="n")

    button_font = font.Font(family='Arial', size=20)

    generate_button = ttk.Button(window, text="Generate",command=lambda: generate_threaded(window))
    generate_button.pack(in_=menu_frame, fill="x")
    adjust_column_width(window, 0)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)

    window.mainloop()