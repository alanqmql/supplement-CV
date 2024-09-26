import tkinter as tk
from debt_app import DebtApp

if __name__ == "__main__":
    root = tk.Tk()
    app = DebtApp(root)
    root.mainloop()