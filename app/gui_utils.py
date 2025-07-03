import tkinter as tk
from tkinter import ttk


def code_input_dialog() -> None:
    code_result = {"code": None}

    def submit():
        code_result["code"] = code_var.get()
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("Введите код из Telegram")
    popup.geometry("300x130")
    popup.grab_set()

    ttk.Label(popup, text="Введите код, отправленный Telegram:").pack(pady=(15, 5))
    code_var = tk.StringVar()
    ttk.Entry(popup, textvariable=code_var, justify="center").pack(pady=5)
    ttk.Button(popup, text="Отправить", command=submit).pack(pady=10)

    popup.wait_window()
    return code_result["code"]


def password_input_dialog() -> None:
    result = {"password": None}

    def submit():
        result["password"] = pass_var.get()
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("Двухфакторная авторизация")
    popup.geometry("300x130")
    popup.grab_set()

    ttk.Label(popup, text="Введите пароль Telegram:").pack(pady=(15, 5))
    pass_var = tk.StringVar()
    ttk.Entry(popup, textvariable=pass_var, show="*", justify="center").pack(pady=5)
    ttk.Button(popup, text="Отправить", command=submit).pack(pady=10)

    popup.wait_window()
    return result["password"]
