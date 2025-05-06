import math
import re
import numpy as np
from scipy.special import factorial
from tkinter import RIDGE, Button, Entry, Label, StringVar, Tk, Frame

class Calculator:
    def __init__(self, gui_win):
        # Window configuration
        self.gui_win = gui_win
        self.gui_win.title("Scientific Calculator")
        self.gui_win.geometry("650x780")
        self.gui_win.configure(bg="cadet blue")
        self.gui_win.iconbitmap('calci32.ico')

        # Main container frame
        self.MainFrame = Frame(self.gui_win, bd=18, relief=RIDGE, bg='powder blue')
        self.MainFrame.pack(expand=True, fill='both')

        # Inner widget frame for buttons and input
        self.WidgetFrame = Frame(self.MainFrame, bd=18, relief=RIDGE, bg='cadet blue')
        self.WidgetFrame.pack(expand=True, fill='both')

        # Configure grid layout
        for i in range(8): self.WidgetFrame.columnconfigure(i, weight=1)
        for i in range(11): self.WidgetFrame.rowconfigure(i, weight=1)

        # Expression label above input field
        self.expression_label_var = StringVar()
        self.ExpressionLabel = Label(self.WidgetFrame, textvariable=self.expression_label_var,
                                     font=("arial", 16, "bold"), anchor='e', bg='cadet blue', fg='white')
        self.ExpressionLabel.grid(row=0, column=0, columnspan=8, sticky="nsew", padx=10, pady=(10, 0))

        # Input field for expressions
        self.input_Val = StringVar()
        self.EvalText = Entry(self.WidgetFrame, textvariable=self.input_Val, bd=10, bg='white',
                              font=("arial", 20, "bold"), justify='right')
        self.EvalText.grid(row=1, column=0, columnspan=8, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Buttons initialization (key functional and layout buttons)
        self.create_button("±", 3, 1)
        self.create_button(".", 3, 2)
        self.create_button("CE", 3, 3, bg='red')
        self.create_button("⌫", 3, 4, bg='#FF7F50')
        self.create_button("=", 3, 5, columnspan=2, bg='#00FA9A')

        # Trigonometric and number buttons with color coding
        self.create_button("sin", 4, 1, fg="red")
        self.create_button("π", 4, 2)
        self.create_button("7", 4, 3, bg='light yellow')
        self.create_button("8", 4, 4, bg='light yellow')
        self.create_button("9", 4, 5, bg='light yellow')
        self.create_button("+", 4, 6, bg='light yellow')

        self.create_button("cos", 5, 1, fg="red")
        self.create_button("e", 5, 2)
        self.create_button("4", 5, 3, bg='light yellow')
        self.create_button("5", 5, 4, bg='light yellow')
        self.create_button("6", 5, 5, bg='light yellow')
        self.create_button("-", 5, 6, bg='light yellow')

        self.create_button("tan", 6, 1, fg="red")
        self.create_button("|x|", 6, 2)
        self.create_button("1", 6, 3, bg='light yellow')
        self.create_button("2", 6, 4, bg='light yellow')
        self.create_button("3", 6, 5, bg='light yellow')
        self.create_button("x", 6, 6, bg='light yellow')

        # Inverse trigonometric functions
        self.create_button("sin⁻¹", 7, 1, fg="red")
        self.create_button("(", 7, 2)
        self.create_button(")", 7, 3)
        self.create_button("0", 7, 4, bg='light yellow')
        self.create_button("%", 7, 5)
        self.create_button("÷", 7, 6, bg='light yellow')

        self.create_button("cos⁻¹", 8, 1, fg="red")
        self.create_button("1/x", 8, 2)
        self.create_button("ln", 8, 3)
        self.create_button("exp", 8, 4)
        self.create_button("n!", 8, 5)
        self.create_button("log₁₀", 8, 6)

        self.create_button("tan⁻¹", 9, 1, fg="red")
        self.create_button("√", 9, 2)
        self.create_button("∛", 9, 3)
        self.create_button("x²", 9, 4)
        self.create_button("x^y", 9, 5)
        self.create_button("10^y", 9, 6)

    def create_button(self, text, row, col, columnspan=1, command=None, bg='powder blue', fg=None):
        # Creates calculator buttons with optional customization
        btn = Button(
            self.WidgetFrame, text=text, width=4, height=2, bd=2, bg=bg, fg=fg,
            font=('arial', 16, 'bold') if text.isdigit() else ('arial', 14, 'bold'),
            command=command if command else lambda t=text: self.on_button_click(t)
        )
        btn.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="nsew")

    def get_after_last_operator(self, s):
        # Extracts the last operand after an operator or parenthesis
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
        operators = ("+", "-", "x", "÷", "*", "/", "+", "-", "%")

        try:
            if char == "CE":
                self.input_Val.set("")
                self.expression_label_var.set("")

            elif char == "⌫":
                self.input_Val.set(current[:-1])

            elif char == "=":
                if not current:
                    return
                # Replace user-friendly symbols and functions with Python/evaluable syntax
                expression = current.replace("exp", str(np.e) + "**")
                expression = expression.replace("log₁₀", "np.log10")
                expression = expression.replace("+", "+").replace("-", "-").replace("x", "*").replace("÷", "/").replace("%", "%")
                expression = re.sub(r'(\d+(\.\d+)?)(π|e)', r'\1*\3', expression)
                expression = re.sub(r'\bln\(([^()]*)\)', r'np.log(\1)', expression)
                expression = expression.replace("π", str(np.pi)).replace("e", str(np.e))
                expression = expression.replace("sqrt", "np.sqrt").replace("∛", "np.cbrt")
                expression = expression.replace("fact", "factorial").replace("10^", "10**")

                # Handle trigonometric and inverse trigonometric functions
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

            # Operator logic to avoid repeated symbols
            elif char in operators:
                if not current or current[-1] in operators:
                    return
                self.input_Val.set(current + char)

            # Handle special operations and wrappers
            elif char == "x²":
                if current:
                    self.input_Val.set(str(current) + '**2')

            elif char == "√":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = 'sqrt(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'sqrt' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "∛":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = '∛(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else '∛' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "1/x":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = '1/(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else '1/' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "exp":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = 'exp(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'exp' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "log₁₀":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = 'log₁₀(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'log₁₀' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "ln":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = 'ln(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'ln' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "n!":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = 'fact(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else 'fact' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "x^y":
                if current:
                    self.input_Val.set(current + "**")

            elif char == "10^y":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    after = '10^(' + after + ')' if not (after.startswith('(') and after.endswith(')')) else '10^' + after
                    self.input_Val.set(before + (operator if operator else "") + after)

            elif char == "|x|":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    if before == "" and operator == '-':
                        self.input_Val.set(before  + 'abs(' +operator+ after + ')')
                    else:
                        self.input_Val.set(before + operator + 'abs(' + after + ')')

            elif char == "±":
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    operator = '+' if operator == '-' else '-' if operator else '-'
                    self.input_Val.set(before + operator + after)

            elif char in ("sin", "cos", "tan"):
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    func_expr = f"{char}({after})" if (after.startswith("(") and after.endswith(")")) else f"{char}(" + after + ")"
                    self.input_Val.set(before + (operator if operator else "") + func_expr)

            elif char in ("sin⁻¹", "cos⁻¹", "tan⁻¹"):
                func_map = {"sin⁻¹": "asin", "cos⁻¹": "acos", "tan⁻¹": "atan"}
                func = func_map[char]
                if current:
                    before, operator, after = self.get_after_last_operator(current)
                    func_expr = f"{func}({after})" if (after.startswith("(") and after.endswith(")")) else f"{func}(" + after + ")"
                    self.input_Val.set(before + (operator if operator else "") + func_expr)

            elif char in valid_inputs or char in "()":
                self.input_Val.set(current + char)

        except Exception:
            self.input_Val.set("Error")
            self.expression_label_var.set("")

# Initialize the GUI window and run the app
gui_win = Tk()
App = Calculator(gui_win)
gui_win.mainloop()
