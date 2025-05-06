import math
import re
import numpy as np
from scipy.special import factorial
from tkinter import RIDGE, Button, Entry, Label, StringVar, Tk, Frame

class Calculator:
    def __init__(self, gui_win):
        self.gui_win = gui_win
        self.gui_win.title("Scientific Calculator")
        self.gui_win.geometry("750x700")
        self.gui_win.configure(bg="cadet blue")
        self.gui_win.iconbitmap('calci32.ico')

        self.MainFrame = Frame(self.gui_win, bd=18, relief=RIDGE, bg='powder blue')
        self.MainFrame.pack(expand=True, fill='both')

        self.WidgetFrame = Frame(self.MainFrame, bd=18, relief=RIDGE, bg='cadet blue')
        self.WidgetFrame.pack(expand=True, fill='both')

        for i in range(7): self.WidgetFrame.columnconfigure(i, weight=1)
        for i in range(10): self.WidgetFrame.rowconfigure(i, weight=1)

        self.expression_label_var = StringVar()
        self.ExpressionLabel = Label(self.WidgetFrame, textvariable=self.expression_label_var,
                                     font=("arial", 16, "bold"), anchor='e', bg='powder blue', fg='black')
        self.ExpressionLabel.grid(row=0, column=0, columnspan=7, sticky="nsew", padx=10, pady=(10, 0))

        self.input_Val = StringVar()
        self.EvalText = Entry(self.WidgetFrame, textvariable=self.input_Val, bd=10, bg='white',
                              font=("arial", 20, "bold"), justify='right')
        self.EvalText.grid(row=1, column=0, columnspan=7, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Left Side - Advanced / Trigonometric Functions
        self.create_button("sin", 3, 0, fg="red")
        self.create_button("cos", 4, 0, fg="red")
        self.create_button("tan", 5, 0, fg="red")
        self.create_button("sin⁻¹", 6, 0, fg="red")
        self.create_button("cos⁻¹", 7, 0, fg="red")
        self.create_button("tan⁻¹", 8, 0, fg="red")

        self.create_button("ln", 3, 1)
        self.create_button("log₁₀", 4, 1)
        self.create_button("exp", 5, 1)
        self.create_button("1/x", 6, 1)
        self.create_button("n!", 7, 1)
        self.create_button("x^y", 8, 1)

        self.create_button("10^y", 3, 2)
        self.create_button("√", 4, 2)
        self.create_button("∛", 5, 2)
        self.create_button("x²", 6, 2)
        self.create_button("|x|", 7, 2)
        self.create_button("±", 8, 2)

        # Right Side - Standard Calculator Functions
        self.create_button("π", 3, 3)
        self.create_button("e", 3, 4)
        self.create_button("⌫", 3, 5, bg='#FF7F50')
        self.create_button("CE", 3, 6, bg='red')

        self.create_button("7", 4, 3, bg='light yellow')
        self.create_button("8", 4, 4, bg='light yellow')
        self.create_button("9", 4, 5, bg='light yellow')
        self.create_button("÷", 4, 6, bg='light yellow')

        self.create_button("4", 5, 3, bg='light yellow')
        self.create_button("5", 5, 4, bg='light yellow')
        self.create_button("6", 5, 5, bg='light yellow')
        self.create_button("x", 5, 6, bg='light yellow')

        self.create_button("1", 6, 3, bg='light yellow')
        self.create_button("2", 6, 4, bg='light yellow')
        self.create_button("3", 6, 5, bg='light yellow')
        self.create_button("-", 6, 6, bg='light yellow')

        self.create_button("0", 7, 3, bg='light yellow')
        self.create_button(".", 7, 4)
        self.create_button("%", 7, 5)
        self.create_button("+", 7, 6, bg='light yellow')

        self.create_button("(", 8, 3)
        self.create_button(")", 8, 4)
        self.create_button("=", 8, 5, columnspan=2, bg='#00FA9A')

    def create_button(self, text, row, col, columnspan=1, command=None, bg='powder blue', fg=None):
        btn = Button(
            self.WidgetFrame, text=text, width=4, height=2, bd=2, bg=bg, fg=fg,
            font=('arial', 16, 'bold') if text.isdigit() else ('arial', 14, 'bold'),
            command=command if command else lambda t=text: self.on_button_click(t)
        )
        btn.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="nsew")

    def get_after_last_operator(self, s):
        if s and s[-1] == ')':
            count = 0
            for i in range(len(s) - 1, -1, -1):
                if s[i] == ')': count += 1
                elif s[i] == '(':
                    count -= 1
                    if count == 0:
                        if i > 0:
                            return s[:i - 1], s[i - 1], s[i:]
                        else:
                            return "", "", s
            return "", "", s
        for i in range(len(s) - 1, -1, -1):
            if s[i] in '+-x/%':
                return s[:i], s[i], s[i + 1:]
        return "", "", s

    def on_button_click(self, char):
        current = self.input_Val.get()
        valid_inputs = "0123456789.+-*/()%πe"
        operators = ("+", "-", "x", "÷", "*", "/", "%")

        try:
            if char == "CE":
                self.input_Val.set("")
                self.expression_label_var.set("")

            elif char == "⌫":
                self.input_Val.set(current[:-1])

            elif char == "=":
                if not current:
                    return
                expression = current.replace("exp", str(np.e) + "**")
                expression = expression.replace("log₁₀", "np.log10")
                expression = expression.replace("x", "*").replace("÷", "/")
                expression = re.sub(r'(\d+(\.\d+)?)(π|e)', r'\1*\3', expression)
                expression = re.sub(r'\bln\(([^()]*)\)', r'np.log(\1)', expression)
                expression = expression.replace("π", str(np.pi)).replace("e", str(np.e))
                expression = expression.replace("sqrt", "np.sqrt").replace("∛", "np.cbrt")
                expression = expression.replace("fact", "factorial").replace("10^", "10**")
                expression = re.sub(r'\bsin\(([^()]*)\)', r'np.sin(np.radians(\1))', expression)
                expression = re.sub(r'\bcos\(([^()]*)\)', r'np.cos(np.radians(\1))', expression)
                expression = re.sub(r'\btan\(([^()]*)\)', r'np.tan(np.radians(\1))', expression)
                expression = re.sub(r'\basin\(([^()]*)\)', r'np.degrees(np.arcsin(\1))', expression)
                expression = re.sub(r'\bacos\(([^()]*)\)', r'np.degrees(np.arccos(\1))', expression)
                expression = re.sub(r'\batan\(([^()]*)\)', r'np.degrees(np.arctan(\1))', expression)
                result = eval(expression)
                updated_expression = current.replace("exp", "e**").replace("π", f'({np.pi})').replace("e", f'({np.e})')
                self.expression_label_var.set(updated_expression + " =")
                self.input_Val.set(str(result))

            elif char in operators:
                if not current or current[-1] in operators:
                    return
                self.input_Val.set(current + char)

            elif char == "x²":
                if current:
                    self.input_Val.set(str(current) + '**2')

            elif char == "√":
                before, op, after = self.get_after_last_operator(current)
                after = 'sqrt(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'sqrt' + after
                self.input_Val.set(before + (op if op else "") + after)

            elif char == "∛":
                before, op, after = self.get_after_last_operator(current)
                after = '∛(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else '∛' + after
                self.input_Val.set(before + (op if op else "") + after)

            elif char == "1/x":
                before, op, after = self.get_after_last_operator(current)
                after = '1/(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else '1/' + after
                self.input_Val.set(before + (op if op else "") + after)

            elif char in ["exp", "log₁₀", "ln", "n!", "10^y"]:
                label_map = {"n!": "fact", "10^y": "10^"}
                func = label_map.get(char, char)
                before, op, after = self.get_after_last_operator(current)
                after = f'{func}({after})' if not (after.startswith('(') and after.endswith(')')) else f'{func}' + after
                self.input_Val.set(before + (op if op else "") + after)

            elif char == "|x|":
                before, op, after = self.get_after_last_operator(current)
                if before == "" and op == '-':
                    self.input_Val.set(before + 'abs(' + op + after + ')')
                else:
                    self.input_Val.set(before + op + 'abs(' + after + ')')

            elif char == "±":
                before, op, after = self.get_after_last_operator(current)
                op = '+' if op == '-' else '-' if op else '-'
                self.input_Val.set(before + op + after)

            elif char in ("sin", "cos", "tan"):
                before, op, after = self.get_after_last_operator(current)
                expr = f"{char}({after})" if not (after.startswith('(') and after.endswith(')')) else f"{char}" + after
                self.input_Val.set(before + (op if op else "") + expr)

            elif char in ("sin⁻¹", "cos⁻¹", "tan⁻¹"):
                func_map = {"sin⁻¹": "asin", "cos⁻¹": "acos", "tan⁻¹": "atan"}
                func = func_map[char]
                before, op, after = self.get_after_last_operator(current)
                expr = f"{func}({after})" if not (after.startswith('(') and after.endswith(')')) else f"{func}" + after
                self.input_Val.set(before + (op if op else "") + expr)

            elif char in valid_inputs or char in "()":
                self.input_Val.set(current + char)

        except Exception:
            self.input_Val.set("Error")
            self.expression_label_var.set("")

# Start the calculator
gui_win = Tk()
App = Calculator(gui_win)
gui_win.mainloop()
