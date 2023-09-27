import math
import tkinter as tk
from tkinter import Label, Entry, Button, Text, END, W, E
from tkinter import Canvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def bisection_method(func, a, b, tol, max_iterations):
    try:
        def f(x):
            return eval(func, {'x': x, 'math': math})
        
        if f(a) * f(b) >= 0:
            raise ValueError("The function values at the endpoints must have opposite signs.")
        
        iteration = 0
        result_text = ""
        while (b - a) / 2.0 > tol and iteration < max_iterations:
            c = (a + b) / 2.0
            if f(c) == 0.0:
                return c, result_text
            elif f(c) * f(a) < 0:
                b = c
            else:
                a = c
            iteration += 1
            result_text += f"Iteration {iteration}: Approximate root = {c:.6f}\n"
        
        return (a + b) / 2.0, result_text
    except Exception as e:
        return None, str(e)

def eval_expression(x, expression):
    return eval(expression, {'x': x, 'math': math})

def calculate_root():
    func = func_entry.get()
    a = float(a_entry.get())
    b = float(b_entry.get())
    tol = float(tol_entry.get())

    max_iterations = math.ceil(math.log((b - a) / tol, 2))

    result, iteration_results = bisection_method(func, a, b, tol, max_iterations)

    if result is not None:
        result_label.config(text=f"Approximate root: {result:.6f}")
        iterations_text.config(state='normal')
        iterations_text.delete(1.0, END)
        iterations_text.insert(END, iteration_results)
        iterations_text.config(state='disabled')

        # Update the graph with the approximate root
        update_graph(func, a, b, result)
    else:
        result_label.config(text="Error: Invalid input or no root found.")

def update_graph(func, a, b, root):
    x_values = np.linspace(a, b, 400)
    y_values = [eval_expression(x, func) for x in x_values]

    ax.clear()
    ax.plot(x_values, y_values, label=f'f(x) = {func}', color='b')
    ax.axhline(0, color='r', linestyle='--', linewidth=0.7)
    ax.axvline(0, color='r', linestyle='--', linewidth=0.7)
    
    # Plot the approximate root point
    ax.plot(root, eval_expression(root, func), 'ro', label='Approximate Root')
    
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Function Plot')
    ax.legend()
    ax.grid(True)

    canvas.draw()

root = tk.Tk()
root.title("Bisection Method Calculator")
root.geometry("800x600")  # Adjust window size

func_label = Label(root, text="Enter the function f(x):")
func_label.pack()
func_entry = Entry(root, width=50)
func_entry.pack()

a_label = Label(root, text="Enter the left endpoint (a):")
a_label.pack()
a_entry = Entry(root, width=20)
a_entry.pack()

b_label = Label(root, text="Enter the right endpoint (b):")
b_label.pack()
b_entry = Entry(root, width=20)
b_entry.pack()

tol_label = Label(root, text="Enter tolerance:")
tol_label.pack()
tol_entry = Entry(root, width=20)
tol_entry.pack()

calculate_button = Button(root, text="Calculate Root", command=calculate_root)
calculate_button.pack()

result_label = Label(root, text="")
result_label.pack()

iterations_text = Text(root, height=10, width=60)
iterations_text.pack()
iterations_text.config(state='disabled')

# Create a Matplotlib figure and canvas
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

root.mainloop()
