#!/usr/bin/env python
# coding: utf-8

# In[8]:


import tkinter as tk
from tkinter import ttk
import numexpr as ne
import math
import re

root = tk.Tk()
root.title("簡易電卓")
root.geometry("280x400")
root.minsize(width=280, height=400)

# --- スタイル設定 ---
style = ttk.Style()
style.configure("TButton", font=('Arial', 12), foreground='black')
style.configure("Bold.TButton", font=('Arial', 12, 'bold'), foreground='black')

# --- 表示部 (tk.Entryで直接フォント指定) ---
display_var = tk.StringVar()
display = tk.Entry(root, width=30, justify="right", state="normal", textvariable=display_var,
                   font=('Arial', 16), bg='lightgray', fg='black', readonlybackground='lightgray')
display.grid(row=0, column=0, columnspan=5, padx=15, pady=20, sticky="nsew")
display.bind("<Key>", lambda e: "break")  # 手入力をブロック

# --- ボタンの定義 ---
buttons_info = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3), ('√', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3), ('%', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('π', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('(', 4, 2), (')', 4, 3), ('+', 4, 4),
    ('C', 5, 0), ('sin', 5, 1), ('cos', 5, 2), ('tan', 5, 3), ('=', 5, 4)
]
button_widgets = {}

def button_click(char):
    current_text = display_var.get()
    display_operators = ['+', '-', '×', '÷', '^', '%']

    if current_text == "Error" and char not in ['C', '=']:
        current_text = ""
        display_var.set("")

    if char == 'C':
        display_var.set("")
        return
    elif char == '=':
        expression_for_eval = current_text
        pattern_sqrt = r'√(\d+(?:\.\d+)?|\([^)]+\)|(?:sin|cos|tan)\([^)]+\))'
        expression_for_eval = re.sub(pattern_sqrt, r'sqrt(\1)', expression_for_eval)
        expression_for_eval = expression_for_eval.replace('π', str(math.pi))
        expression_for_eval = expression_for_eval.replace('×', '*')
        expression_for_eval = expression_for_eval.replace('÷', '/')
        expression_for_eval = expression_for_eval.replace('%', '/100')
        try:
            result = ne.evaluate(expression_for_eval)
            if result == int(result):
                display_var.set(str(int(result)))
            else:
                display_var.set(f"{result:.8g}")
        except Exception as e:
            display_var.set("Error")
            print(f"Calculation Error: {e}")
        return

    last_char = current_text[-1:] if current_text else ''
    if char in display_operators and last_char in display_operators:
        display_var.set(current_text[:-1] + char)
    elif char == '.' and '.' in re.split(r'[+\-*/×÷]', current_text)[-1]:
        pass
    elif char in ['sin', 'cos', 'tan', '√']:
        if last_char.isdigit() or last_char == ')' or last_char == 'π':
            display_var.set(current_text + '*' + char)
        else:
            display_var.set(current_text + char)
    elif char == '(':
        if last_char.isdigit() or last_char == ')' or last_char == 'π':
            display_var.set(current_text + '*' + char)
        else:
            display_var.set(current_text + char)
    elif char == ')':
        display_var.set(current_text + char)
    else:
        display_var.set(current_text + char)

# --- フォントサイズ調整関数 ---
def on_window_resize(event=None):
    root.update_idletasks()

    display_height = display.winfo_height()
    entry_font_size = max(16, int(display_height * 0.5))  # サイズに応じて調整
    display.config(font=('Arial', entry_font_size))

    if '7' in button_widgets:
        sample_button = button_widgets['7']
        button_height = sample_button.winfo_height()
        button_font_size = max(12, int(button_height * 0.3))
        style.configure("TButton", font=('Arial', button_font_size))
        style.configure("Bold.TButton", font=('Arial', button_font_size, 'bold'))

# --- ボタンの配置 ---
for (btn_text, row, col) in buttons_info:
    btn_style = "Bold.TButton" if btn_text in ('C', '=') else "TButton"
    btn = ttk.Button(root, text=btn_text, command=lambda t=btn_text: button_click(t), style=btn_style)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    button_widgets[btn_text] = btn

# --- グリッド構成 ---
root.grid_rowconfigure(0, weight=1)
for i in range(1, 6):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# --- ウィンドウリサイズイベント処理 ---
def delayed_resize_handler(event):
    if hasattr(root, '_resize_job_id'):
        root.after_cancel(root._resize_job_id)
    root._resize_job_id = root.after(50, lambda: on_window_resize(event))

root.bind('<Configure>', delayed_resize_handler)

# 初期フォントサイズ設定
root.update_idletasks()
on_window_resize()

root.mainloop()

