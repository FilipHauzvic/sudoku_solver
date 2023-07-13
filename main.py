from sudoku import Sudoku, Difficulty
from generator import Generator
import threading
import time

import tkinter as tk
from tkinter import ttk
import tkinter.font as font

main_sudoku = Sudoku()

def validate_entry(value):
    if len(value) == 0:
        return True
    try:
        int(value)
        if len(value) > 1:
            return False
        else:
            return True
    except ValueError:
        return False

def create_board(window, sudoku):
    board_frame = tk.Frame(window)
    board_frame.grid(row = 0, column = 1)
    for i in range(9):
        for j in range(9):
            cell = tk.Entry(board_frame, width=2, justify="center", font=("Arial", 20), validate="key", validatecommand=validate_entry_command)
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

def generate_threaded(window, button : ttk.Button, combobox : ttk.Combobox):
    gen_thread = threading.Thread(target=generate, args=(window, button, combobox, Difficulty[combobox.get()]))
    gen_thread.daemon = True
    gen_thread.start()

def generate(window, button : ttk.Button = None, combobox : ttk.Combobox = None, difficulty : Difficulty = Difficulty.MEDIUM):    
    if button is not None:
        button.configure(state="disabled", text="Generating...")
        window.update()
    if combobox is not None:
        combobox.configure(state="disabled")
        window.update()
    generator = Generator(difficulty)
    sudoku : Sudoku = None
    try:
        sudoku = generator.generate()
    except Exception as e:
        print(e)
        exit(1)
    sudoku.print_board()
    create_board(window, sudoku)
    if button is not None:
        button.configure(state="enabled", text="Generate")
        window.update()
    if combobox is not None:
        combobox.configure(state="enabled")
        window.update()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sudoku")
    window.geometry("750x500")
    validate_entry_command = (window.register(validate_entry), '%P')

    style = ttk.Style(window)
    window.tk.call('source', 'breeze-dark/breeze-dark.tcl')
    style.theme_use('breeze-dark')

    menu_frame = tk.Frame(window)
    menu_frame.grid(row = 0, column = 0, sticky="n")

    button_font = font.Font(family='Arial', size=20)

    difficulty_combobox = ttk.Combobox(window, values=[Difficulty.EASY.name, Difficulty.MEDIUM.name, Difficulty.HARD.name, Difficulty.EXPERT.name])
    difficulty_combobox.current(1)
    difficulty_combobox.pack(in_=menu_frame, fill="x")

    generate_button = ttk.Button(window, text="Generate",command=lambda: generate_threaded(window, generate_button, difficulty_combobox))
    generate_button.pack(in_=menu_frame, fill="x")

    test_button = ttk.Button(window, text="Test",command=lambda: print(Difficulty[difficulty_combobox.get()].name))
    test_button.pack(in_=menu_frame, fill="x")

    adjust_column_width(window, 0)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)

    create_board(window, main_sudoku)

    window.mainloop()