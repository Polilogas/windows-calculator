import tkinter as tk
import math

# My approach is that every input is first saved in the bigValue,
# then when an operation is pressed, it does the operation with the smallValue.
# Example, smallValue *= bigValue
# and then resets the bigValue back to 0 before it receive the next input
#
# ╔════════════════════════════════════╗
# ║ Calculator               -   □   x ║
# ╟────────────────────────────────────╢
# ║                        smallLabel  ║ ◀─────────────────── smallValue ◀────────────────────────────────────────────┐
# ║                        bigLabel    ║ ◀─────────────────── (bigValue * 10) + ◀┐      ┌‐‐‐‐‐‐‐‐‐┐                   │
# ║                                    ║                                         └──────┤  Input  │                   │
# ║                                    ║                                                └‐‐‐‐‐‐‐‐‐┘                   │
# ╟────────┬────────┬────────┬─────────╢                                                                              │
# ║   %    │   CE   │   C    │    ⌫   ║ ╍╍╍╍╍╍╍ Row 5                                                                │
# ║────────┼────────┼────────┼─────────╢                      ┌‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐┐   │
# ║  ¹/x   │   x²   │  ²√x   │    ÷    ║ ╍╍╍╍╍╍╍ Row 4        │smallValue = smallValue previousOperation= bigValue├───┘
# ║────────┼────────┼────────┼─────────╢                      └‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐┘
# ║    7   │    8   │    9   │    ×    ║ ╍╍╍╍╍╍╍ Row 3                                         ▲
# ║────────┼────────┼────────┼─────────╢                                                       │
# ║    4   │    5   │    6   │    -    ║ ╍╍╍╍╍╍╍ Row 2                                         │
# ║────────┼────────┼────────┼─────────╢                                                       │
# ║    1   │    2   │    3   │    +    ║ ╍╍╍╍╍╍╍ Row 1                                         │
# ║────────┼────────┼────────┼─────────╢                                                       │
# ║   +/-  │    0   │    ,   │    =    ║ ╍╍╍╍╍╍╍ Row 0                                         │
# ╚════════╧════════╧════════╧════╤════╝                                                       │
#                                 │                                                            │
#                                 │                         ┌‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐┐    │
#                                 └────────────────────────▶│previousOperation = operation├────┘
#                                                           └‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐┘


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Variables
        self.bigValue = 0                   # It is used to store the input and the final sum
        self.smallValue = 0                 # It is used to store the temporary sum
        self.previousOperation = ""         # It stores the previous operation
        self.writeIsEnabled = True          # If False, then the the calculator will not accept more numbers

        # configure the root window
        self.title('Calculator')            # Window Title
        self.geometry('295x400')            # Window starting dimensions
        self.config(bg='#1f1f1f')           # Window background Color
        self.attributes('-alpha', 0.95)     # Window transparency
        self.resizable(False, False)        # If False, the user will not be allowed to resize the window
        #self.iconbitmap('logo.ico')    # Set the icon on the title bar

        # Set the button sizes
        self.buttonHeight = 2
        self.buttonWidth = 9

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Labels ╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # This is the small results text
        self.smallResult = tk.StringVar()
        self.smallResult.set("")
        self.smallLabel = tk.Label(self, textvariable=self.smallResult, font=('Times New Roman', 11),
                                   bg='#1f1f1f', fg='#b1b0b0')
        self.smallLabel.pack(pady=0, side=tk.TOP, anchor='e')

        # This is the big results text
        self.bigResult = tk.StringVar()
        self.bigResult.set(0)
        self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 40),
                                 bg='#1f1f1f', fg='#ffffff')
        self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Buttons ╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        self.bind_all('<Key>', self.keyboard_pressed)   # For getting keyboard inputs
        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 0 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' = '
        self.buttonEquals = tk.Button(self, text="=", command=lambda: calculator.equals(),
                                      bg="#253b4d", activebackground="#275e8a",
                                      fg="#ffffff", height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonEquals.pack()
        self.buttonEquals.place(x=225, y=360)
        self.buttonEquals.bind("<Enter>", lambda event: self.hover_on(key="<=>"))   # Change color on Hover
        self.buttonEquals.bind("<Leave>", lambda event: self.hover_off(key="<=>"))  # Reset the color on Hover off

        # Button ' 0 '
        self.button_0 = tk.Button(self, text="0", command=lambda: calculator.write(0),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_0.pack()
        self.button_0.place(x=75, y=360)
        self.button_0.bind("<Enter>", lambda event: self.hover_on(key="<0>"))  # Change color on Hover
        self.button_0.bind("<Leave>", lambda event: self.hover_off(key="<0>"))  # Reset the color on Hover off

        # Button ' , '
        self.buttonComma = tk.Button(self, text=",", command=lambda: calculator.comma(),
                                     bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                     height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonComma.pack()
        self.buttonComma.place(x=150, y=360)
        self.buttonComma.bind("<Enter>", lambda event: self.hover_on(key="<,>"))  # Change color on Hover
        self.buttonComma.bind("<Leave>", lambda event: self.hover_off(key="<,>"))  # Reset the color on Hover off

        # Button ' +/- '
        self.buttonNegate = tk.Button(self, text="+/-", command=lambda: calculator.negate(),
                                      bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                      height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonNegate.pack()
        self.buttonNegate.place(x=0, y=360)
        self.buttonNegate.bind("<Enter>", lambda event: self.hover_on(key="<+/->"))  # Change color on Hover
        self.buttonNegate.bind("<Leave>", lambda event: self.hover_off(key="<+/->"))  # Reset the color on Hover off

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 1 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' 1 '
        self.button_1 = tk.Button(self, text="1", command=lambda: calculator.write(1),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_1.pack()
        self.button_1.place(x=0, y=320)
        self.button_1.bind("<Enter>", lambda event: self.hover_on(key="<1>"))  # Change color on Hover
        self.button_1.bind("<Leave>", lambda event: self.hover_off(key="<1>"))  # Reset the color on Hover off

        # Button ' 2 '
        self.button_2 = tk.Button(self, text="2", command=lambda: calculator.write(2),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_2.pack()
        self.button_2.place(x=75, y=320)
        self.button_2.bind("<Enter>", lambda event: self.hover_on(key="<2>"))  # Change color on Hover
        self.button_2.bind("<Leave>", lambda event: self.hover_off(key="<2>"))  # Reset the color on Hover off

        # Button ' 3 '
        self.button_3 = tk.Button(self, text="3", command=lambda: calculator.write(3),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_3.pack()
        self.button_3.place(x=150, y=320)
        self.button_3.bind("<Enter>", lambda event: self.hover_on(key="<3>"))  # Change color on Hover
        self.button_3.bind("<Leave>", lambda event: self.hover_off(key="<3>"))  # Reset the color on Hover off

        # Button ' + '
        self.buttonPlus = tk.Button(self, text="+", command=lambda: calculator.plus(),
                                    bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                    height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonPlus.pack()
        self.buttonPlus.place(x=225, y=320)
        self.buttonPlus.bind("<Enter>", lambda event: self.hover_on(key="<+>"))  # Change color on Hover
        self.buttonPlus.bind("<Leave>", lambda event: self.hover_off(key="<+>"))  # Reset the color on Hover off

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 2 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' 4 '
        self.button_4 = tk.Button(self, text="4", command=lambda: calculator.write(4),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_4.pack()
        self.button_4.place(x=0, y=278)
        self.button_4.bind("<Enter>", lambda event: self.hover_on(key="<4>"))  # Change color on Hover
        self.button_4.bind("<Leave>", lambda event: self.hover_off(key="<4>"))  # Reset the color on Hover off

        # Button ' 5 '
        self.button_5 = tk.Button(self, text="5", command=lambda: calculator.write(5),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_5.pack()
        self.button_5.place(x=75, y=278)
        self.button_5.bind("<Enter>", lambda event: self.hover_on(key="<5>"))  # Change color on Hover
        self.button_5.bind("<Leave>", lambda event: self.hover_off(key="<5>"))  # Reset the color on Hover off

        # Button ' 6 '
        self.button_6 = tk.Button(self, text="6", command=lambda: calculator.write(6),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_6.pack()
        self.button_6.place(x=150, y=278)
        self.button_6.bind("<Enter>", lambda event: self.hover_on(key="<6>"))  # Change color on Hover
        self.button_6.bind("<Leave>", lambda event: self.hover_off(key="<6>"))  # Reset the color on Hover off

        # Button ' - '
        self.buttonMinus = tk.Button(self, text="-", command=lambda: calculator.minus(),
                                     bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                     height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonMinus.pack()
        self.buttonMinus.place(x=225, y=278)
        self.buttonMinus.bind("<Enter>", lambda event: self.hover_on(key="<->"))  # Change color on Hover
        self.buttonMinus.bind("<Leave>", lambda event: self.hover_off(key="<->"))  # Reset the color on Hover off

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 3 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' 7 '
        self.button_7 = tk.Button(self, text="7", command=lambda: calculator.write(7),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_7.pack()
        self.button_7.place(x=0, y=236)
        self.button_7.bind("<Enter>", lambda event: self.hover_on(key="<7>"))  # Change color on Hover
        self.button_7.bind("<Leave>", lambda event: self.hover_off(key="<7>"))  # Reset the color on Hover off

        # Button ' 8 '
        self.button_8 = tk.Button(self, text="8", command=lambda: calculator.write(8),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_8.pack()
        self.button_8.place(x=75, y=236)
        self.button_8.bind("<Enter>", lambda event: self.hover_on(key="<8>"))  # Change color on Hover
        self.button_8.bind("<Leave>", lambda event: self.hover_off(key="<8>"))  # Reset the color on Hover off

        # Button ' 9 '
        self.button_9 = tk.Button(self, text="9", command=lambda: calculator.write(9),
                                  bg='#101010', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.button_9.pack()
        self.button_9.place(x=150, y=236)
        self.button_9.bind("<Enter>", lambda event: self.hover_on(key="<9>"))  # Change color on Hover
        self.button_9.bind("<Leave>", lambda event: self.hover_off(key="<9>"))  # Reset the color on Hover off

        # Button ' x '
        self.buttonMulti = tk.Button(self, text="×", command=lambda: calculator.multiply(),
                                     bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                     height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonMulti.pack()
        self.buttonMulti.place(x=225, y=236)
        self.buttonMulti.bind("<Enter>", lambda event: self.hover_on(key="<x>"))  # Change color on Hover
        self.buttonMulti.bind("<Leave>", lambda event: self.hover_off(key="<x>"))  # Reset the color on Hover off

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 4 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' 1/x '
        self.buttonOneDiv_x = tk.Button(self, text="¹/x", command=lambda: calculator.one_div_x(),
                                        bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                        height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonOneDiv_x.pack()
        self.buttonOneDiv_x.place(x=0, y=194)
        self.buttonOneDiv_x.bind("<Enter>", lambda event: self.hover_on(key="<1/x>"))  # Change color on Hover
        self.buttonOneDiv_x.bind("<Leave>", lambda event: self.hover_off(key="<1/x>"))  # Reset the color on Hover off

        # Button ' x^2'
        self.buttonSquare = tk.Button(self, text="x²", command=lambda: calculator.square(),
                                      bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                      height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonSquare.pack()
        self.buttonSquare.place(x=75, y=194)
        self.buttonSquare.bind("<Enter>", lambda event: self.hover_on(key="<square>"))  # Change color on Hover
        self.buttonSquare.bind("<Leave>", lambda event: self.hover_off(key="<square>"))  # Reset the color on Hover off

        # Button ' root '
        self.buttonRoot = tk.Button(self, text="²√x", command=lambda: calculator.root(),
                                    bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                    height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonRoot.pack()
        self.buttonRoot.place(x=150, y=194)
        self.buttonRoot.bind("<Enter>", lambda event: self.hover_on(key="<root>"))  # Change color on Hover
        self.buttonRoot.bind("<Leave>", lambda event: self.hover_off(key="<root>"))  # Reset the color on Hover off

        # Button ' / '
        self.buttonDivide = tk.Button(self, text="÷", command=lambda: calculator.divide(),
                                      bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                      height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonDivide.pack()
        self.buttonDivide.place(x=225, y=194)
        self.buttonDivide.bind("<Enter>", lambda event: self.hover_on(key="</>"))  # Change color on Hover
        self.buttonDivide.bind("<Leave>", lambda event: self.hover_off(key="</>"))  # Reset the color on Hover off

        # ╍╍╍╍╍╍╍╍╍╍╍╍╍╍ Row 5 ╍╍╍╍╍╍╍╍╍╍╍╍╍╍
        # Button ' % '
        self.buttonPercent = tk.Button(self, text="%", command=lambda: calculator.percent(),
                                       bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                       height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonPercent.pack()
        self.buttonPercent.place(x=0, y=153)
        self.buttonPercent.bind("<Enter>", lambda event: self.hover_on(key="<%>"))  # Change color on Hover
        self.buttonPercent.bind("<Leave>", lambda event: self.hover_off(key="<%>"))  # Reset the color on Hover off

        # Button ' CE '
        self.buttonCE = tk.Button(self, text="CE", command=lambda: calculator.clear_entry(),
                                  bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                  height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonCE.pack()
        self.buttonCE.place(x=75, y=153)
        self.buttonCE.bind("<Enter>", lambda event: self.hover_on(key="<CE>"))  # Change color on Hover
        self.buttonCE.bind("<Leave>", lambda event: self.hover_off(key="<CE>"))  # Reset the color on Hover off

        # Button ' C '
        self.buttonC = tk.Button(self, text="C", command=lambda: calculator.clear(),
                                 bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                 height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonC.pack()
        self.buttonC.place(x=150, y=153)
        self.buttonC.bind("<Enter>", lambda event: self.hover_on(key="<C>"))  # Change color on Hover
        self.buttonC.bind("<Leave>", lambda event: self.hover_off(key="<C>"))  # Reset the color on Hover off

        # Button ' erase '
        self.buttonErase = tk.Button(self, text="⌫", command=lambda: calculator.erase(),
                                     bg='#242424', activebackground='#b3b3b3', fg="#ffffff",
                                     height=self.buttonHeight, width=self.buttonWidth, borderwidth=0)
        self.buttonErase.pack()
        self.buttonErase.place(x=225, y=153)
        self.buttonErase.bind("<Enter>", lambda event: self.hover_on(key="<erase>"))  # Change color on Hover
        self.buttonErase.bind("<Leave>", lambda event: self.hover_off(key="<erase>"))  # Reset the color on Hover off

    # It activates everytime you press a number on the Calculator and sends this number to the bigValue
    def write(self, num):
        if self.writeIsEnabled:
            self.bigValue = (self.bigValue * 10) + num
            self.bigResult.set(("{:,}".format(self.bigValue)).replace(",", "."))
            self.update_text_size()
        else:
            pass

    # It activates everytime you press the erase button and deletes one digit from right to left
    def erase(self):
        self.writeIsEnabled = True
        self.bigValue = int(self.bigValue / 10)
        self.bigResult.set(("{:,}".format(self.bigValue)).replace(",", "."))
        self.update_text_size()

    # It activates everytime you press the C button and clears all labels
    def clear(self):
        self.previousOperation = ""
        self.bigValue = 0
        self.smallValue = 0
        self.bigResult.set(self.bigValue)
        self.smallResult.set("")
        self.writeIsEnabled = True
        self.update_text_size()

    # It activates everytime you press the CE button and clears the bigValue
    def clear_entry(self):
        self.bigValue = 0
        self.bigResult.set(self.bigValue)
        self.writeIsEnabled = True
        self.update_text_size()

    # It activates everytime you press the = button and gives you the sum of the equation. I can simplify it
    def equals(self):
        if self.previousOperation == "":
            self.smallValue += self.bigValue
            self.previousOperation = "="
            self.bigResult.set(self.bigValue)
            self.smallResult.set(str(self.bigValue) + " =")
            self.writeIsEnabled = True
            self.update_text_size()
        elif self.previousOperation == "+":
            self.previousOperation = "="
            self.smallResult.set(str(self.smallValue) + " + " + str(self.bigValue) + " =")
            self.smallValue += self.bigValue
            self.bigValue = 0
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
            self.writeIsEnabled = True
            self.update_text_size()
        elif self.previousOperation == "-":
            self.previousOperation = "="
            self.smallResult.set(str(self.smallValue) + " - " + str(self.bigValue) + " =")
            self.smallValue -= self.bigValue
            self.bigValue = 0
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
            self.writeIsEnabled = True
            self.update_text_size()
        elif self.previousOperation == "/":
            self.previousOperation = "="
            self.smallResult.set(str(self.smallValue) + " ÷ " + str(self.bigValue) + " =")
            self.smallValue /= self.bigValue
            self.bigValue = 0
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
            self.writeIsEnabled = True
            self.update_text_size()
        elif self.previousOperation == "x":
            self.previousOperation = "="
            self.smallResult.set(str(self.smallValue) + " x " + str(self.bigValue) + " =")
            self.smallValue *= self.bigValue
            self.bigValue = 0
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
            self.writeIsEnabled = True
            self.update_text_size()

    # It activates everytime you press the + button and adds the smallValue with the bigValue. I can simplify it
    def plus(self):
        if self.previousOperation == "":
            self.previousOperation = "+"
            self.smallValue = self.bigValue
            self.update_text_size()
            self.writeIsEnabled = True
            self.bigValue = 0
            self.smallResult.set(str(self.smallValue) + " +")
        elif self.previousOperation == "+":
            self.previousOperation = "+"
            self.smallValue += self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
            self.smallResult.set(str(self.smallValue) + " +")
        elif self.previousOperation == "-":
            self.previousOperation = "+"
            self.smallValue -= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " +")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "/":
            self.previousOperation = "+"
            self.smallValue /= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " +")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "x":
            self.previousOperation = "+"
            self.smallValue *= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "=":
            self.previousOperation = "+"
            self.smallResult.set(str(self.smallValue) + " +")
            self.writeIsEnabled = True
            self.update_text_size()

    # It activates everytime you press the - button and subtract the smallValue with the bigValue. I can simplify it
    def minus(self):
        if self.previousOperation == "":
            self.previousOperation = "-"
            self.smallValue = self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " -")
        elif self.previousOperation == "-":
            self.smallValue -= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " -")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "+":
            self.previousOperation = "-"
            self.smallValue += self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " -")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "/":
            self.previousOperation = "-"
            self.smallValue /= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " -")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "x":
            self.previousOperation = "/"
            self.smallValue *= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "=":
            self.previousOperation = "-"
            self.smallResult.set(str(self.smallValue) + " -")
            self.writeIsEnabled = True
            self.update_text_size()

    # It activates everytime you press the / button and divides the smallValue with the bigValue. I can simplify it
    def divide(self):
        if self.previousOperation == "":
            self.previousOperation = "/"
            self.smallValue = self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ÷")
        elif self.previousOperation == "/":
            self.smallValue /= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ÷")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "+":
            self.previousOperation = "/"
            self.smallValue += self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ÷")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "-":
            self.previousOperation = "/"
            self.smallValue -= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ÷")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "x":
            self.previousOperation = "/"
            self.smallValue *= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ÷")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "=":
            self.previousOperation = "/"
            self.smallResult.set(str(self.smallValue) + " ×")
            self.writeIsEnabled = True
            self.update_text_size()

    # It activates everytime you press the x button and multiplies the smallValue with the bigValue. I can simplify it
    def multiply(self):
        if self.previousOperation == "":
            self.previousOperation = "x"
            self.smallValue = self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
        elif self.previousOperation == "x":
            self.smallValue *= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "/":
            self.previousOperation = "x"
            self.smallValue /= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "+":
            self.previousOperation = "x"
            self.smallValue += self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "-":
            self.previousOperation = "x"
            self.smallValue -= self.bigValue
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.smallResult.set(str(self.smallValue) + " ×")
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "=":
            self.previousOperation = "x"
            self.smallResult.set(str(self.smallValue) + " ×")
            self.writeIsEnabled = True
            self.update_text_size()

    # It activates everytime you press the root button and calculates the root of the given number. I can simplify it
    def root(self):
        if self.previousOperation == "" or self.previousOperation == "root":
            self.previousOperation = "root"
            self.smallResult.set("√(" + str(self.bigValue) + ")")
            self.smallValue = math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "+":
            self.previousOperation = "root"
            self.smallResult.set(str(self.smallValue) + " + √(" + str(self.bigValue) + ")")
            self.smallValue = self.smallValue + math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "-":
            self.previousOperation = "root"
            self.smallResult.set(str(self.smallValue) + " - √(" + str(self.bigValue) + ")")
            self.smallValue = self.smallValue - math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "x":
            self.previousOperation = "root"
            self.smallResult.set(str(self.smallValue) + " × √(" + str(self.bigValue) + ")")
            self.smallValue = self.smallValue * math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "/":
            self.previousOperation = "root"
            self.smallResult.set(str(self.smallValue) + " / √(" + str(self.bigValue) + ")")
            self.smallValue = self.smallValue / math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))
        elif self.previousOperation == "=":
            self.previousOperation = "root"
            self.smallResult.set("√(" + str(self.smallValue) + ")")
            self.smallValue = self.smallValue + math.sqrt(self.bigValue)
            self.update_text_size()
            self.bigValue = 0
            self.writeIsEnabled = True
            self.bigResult.set(("{:,}".format(self.smallValue)).replace(",", "."))

    # The following one is under development.
    def negate(self):
        print("negate")

    # The following one is under development.
    def percent(self):
        print("percent")

    # The following one is under development.
    def comma(self):
        print("comma")

    # The following one is under development.
    def square(self):
        print("square")

    # The following one is under development.
    def one_div_x(self):
        print("1/x")

    # It is used to fix the text size to fit the calculator dimensions based on the text length
    def update_text_size(self):
        if len(str(self.bigValue)) >= 21:
            self.writeIsEnabled = False

        elif len(str(self.bigValue)) >= 19:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 19),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 17:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 22),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 16:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 24),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 15:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 25),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 14:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 28),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 13:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 30),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 12:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 33),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        elif len(str(self.bigValue)) >= 11:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 35),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

        else:
            self.bigLabel.destroy()
            self.bigLabel = tk.Label(self, textvariable=self.bigResult, font=('Times New Roman', 40),
                                     bg='#1f1f1f', fg='#ffffff')
            self.bigLabel.pack(pady=0, side=tk.TOP, anchor='e')

    # Changes the color of the button on hover on
    def hover_on(self, key):
        if key == "<C>":
            self.buttonC['background'] = '#616161'

        if key == "<CE>":
            self.buttonCE['background'] = '#616161'

        if key == "<erase>":
            self.buttonErase['background'] = '#616161'

        if key == "<=>":
            self.buttonEquals['background'] = '#616161'

        if key == "<0>":
            self.button_0['background'] = '#616161'

        if key == "<1>":
            self.button_1['background'] = '#616161'

        if key == "<2>":
            self.button_2['background'] = '#616161'

        if key == "<3>":
            self.button_3['background'] = '#616161'

        if key == "<4>":
            self.button_4['background'] = '#616161'

        if key == "<5>":
            self.button_5['background'] = '#616161'

        if key == "<6>":
            self.button_6['background'] = '#616161'

        if key == "<7>":
            self.button_7['background'] = '#616161'

        if key == "<8>":
            self.button_8['background'] = '#616161'

        if key == "<9>":
            self.button_9['background'] = '#616161'

        if key == "<,>":
            self.buttonComma['background'] = '#616161'

        if key == "<+>":
            self.buttonPlus['background'] = '#616161'

        if key == "<->":
            self.buttonMinus['background'] = '#616161'

        if key == "<x>":
            self.buttonMulti['background'] = '#616161'

        if key == "</>":
            self.buttonDivide['background'] = '#616161'

        if key == "<%>":
            self.buttonPercent['background'] = '#616161'

        if key == "<square>":
            self.buttonSquare['background'] = '#616161'

        if key == "<root>":
            self.buttonRoot['background'] = '#616161'

        if key == "<1/x>":
            self.buttonOneDiv_x['background'] = '#616161'

        if key == "<+/->":
            self.buttonNegate['background'] = '#616161'

    # Resets the color of the button on hover off
    def hover_off(self, key):
        if key == "<C>":
            self.buttonC['background'] = '#242424'

        if key == "<CE>":
            self.buttonCE['background'] = '#242424'

        if key == "<erase>":
            self.buttonErase['background'] = '#242424'

        if key == "<=>":
            self.buttonEquals['background'] = '#253b4d'

        if key == "<0>":
            self.button_0['background'] = '#101010'

        if key == "<1>":
            self.button_1['background'] = '#101010'

        if key == "<2>":
            self.button_2['background'] = '#101010'

        if key == "<3>":
            self.button_3['background'] = '#101010'

        if key == "<4>":
            self.button_4['background'] = '#101010'

        if key == "<5>":
            self.button_5['background'] = '#101010'

        if key == "<6>":
            self.button_6['background'] = '#101010'

        if key == "<7>":
            self.button_7['background'] = '#101010'

        if key == "<8>":
            self.button_8['background'] = '#101010'

        if key == "<9>":
            self.button_9['background'] = '#101010'

        if key == "<,>":
            self.buttonComma['background'] = '#101010'

        if key == "<+>":
            self.buttonPlus['background'] = '#242424'

        if key == "<->":
            self.buttonMinus['background'] = '#242424'

        if key == "<x>":
            self.buttonMulti['background'] = '#242424'

        if key == "</>":
            self.buttonDivide['background'] = '#242424'

        if key == "<%>":
            self.buttonPercent['background'] = '#242424'

        if key == "<square>":
            self.buttonSquare['background'] = '#242424'

        if key == "<root>":
            self.buttonRoot['background'] = '#242424'

        if key == "<1/x>":
            self.buttonOneDiv_x['background'] = '#242424'

        if key == "<+/->":
            self.buttonNegate['background'] = '#101010'

    # When a key is pressed, it calls the corresponded function
    def keyboard_pressed(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == "1" or event.keysym == "2" or event.keysym == "3" or event.keysym == "4" \
                    or event.keysym == "5" or event.keysym == "6" or event.keysym == "7" or event.keysym == "8" \
                    or event.keysym == "9" or event.keysym == "0":
                self.write(int(event.keysym))

            elif event.keysym == "plus":
                self.plus()

            elif event.keysym == "minus":
                self.minus()

            elif event.keysym == "asterisk":
                self.multiply()

            elif event.keysym == "slash":
                self.divide()

            elif event.keysym == "Return":
                self.equals()

            elif event.keysym == "Escape":
                self.clear()

            elif event.keysym == "BackSpace":
                self.erase()

            else:
                pass


if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
