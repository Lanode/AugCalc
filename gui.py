from calculator import calculate
from simplifier import simplify
from derivative import differentiate, detect_vars_and_diff
from math_parser import parse 
from math_composer import compose
from integral import detect_vars_and_simp

from tkinter import StringVar, Text, ttk
from tkinter import messagebox
import tkinter as tk
import traceback

def solve_diff():
    vvod = str(formula_diff.get()) 
    try:
        ast = parse(vvod)
        ast = simplify(ast)
        print('simplified:\n'+compose(ast))
        deriv_ast = detect_vars_and_diff(ast)
        print('derivative:\n'+compose(deriv_ast))
        deriv_ast = simplify(deriv_ast)
        print('simplified derivative:\n'+compose(deriv_ast))
        vivod_diff.delete(0,"end")
        vivod_diff.insert(0, compose(deriv_ast))
    except Exception as e:
        traceback.print_exc()

def solve_integ():
    vvod_formula = str(formula_integ.get())
    vvod_a = float(chislo_a.get())
    vvod_b = float(chislo_b.get()) 
    try:
        ast = parse(vvod_formula)
        ast = simplify(ast)
        print('simplified:\n'+compose(ast))
        integ = detect_vars_and_simp(ast,vvod_a,vvod_b)
        print('area under a curve:\n'+str(integ))
        vivod_integ.delete(0,"end")
        vivod_integ.insert(0, str(integ))
    except Exception as e:
        traceback.print_exc()


root = tk.Tk()
root.geometry('550x230')
root.minsize(550, 230)
root.maxsize(550, 230)
root.title('Calculator')

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

frame1 = ttk.Frame(notebook, width=300, height=100)
frame2 = ttk.Frame(notebook, width=500, height=300)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)


notebook.add(frame1, text='Differentiation')
notebook.add(frame2, text='Integration')

tk.Label(frame1,text ="Input function:" ).grid(column = 1,
row = 2,)
name = StringVar()
formula_diff = tk.Entry(frame1, width=70)
formula_diff.grid(column= 2, row= 2)
button_diff = tk.Button(frame1,text="Solve", width = 60, height=2, command=solve_diff)
button_diff.grid(row=4, column=2,)
tk.Label(frame1,text ="Output:").grid(column = 1,row = 5,)
name = StringVar()
vivod_diff = tk.Entry(frame1, width=70, relief="ridge")
vivod_diff.grid(column= 2, row= 5)

# tk.Label(frame2,text ='Use only "x" variable' ).grid(column = 1,row = 1,)
formula_integ = tk.Entry(frame2, width=87)
formula_integ.grid(column= 1, row= 1)
tk.Label(frame2,text ="a:" ).grid(column = 1,row = 2,)
chislo_a = tk.Entry(frame2, width=87)
chislo_a.grid(column= 1, row= 3)
tk.Label(frame2,text ="b:" ).grid(column = 1,row = 4,)
chislo_b = tk.Entry(frame2, width=87)
chislo_b.grid(column= 1, row= 5)
button_integ = tk.Button(frame2,text="Solve", width = 60, height=2, command=solve_integ).grid(column=1,row=6) 
vivod_integ = tk.Entry(frame2, width=70, relief="ridge")
vivod_integ.grid(column= 1, row= 7)


root.mainloop()