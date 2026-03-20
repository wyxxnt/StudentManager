import tkinter as tk
from tkinter import ttk


WINDOW_TITLE = "Менеджер навчання студента"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

SUBJECTS = [
    "Програмування",
    "Математика",
    "Фізика",
    "Іноземна мова",
    "Біологія",
    "Інше",
]


def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(600, 400)

    title_label = tk.Label(root, text="📚 Менеджер навчання", font=("Arial", 18, "bold"))
    title_label.pack(pady=15)

    info_label = tk.Label(root, text="Група ІМ-о51 | КПІ ім. Ігоря Сікорського", font=("Arial", 10))
    info_label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
