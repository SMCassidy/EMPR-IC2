# Use Tkinter for python 2, tkinter for python 3
import Tkinter as tk

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = Canvas(self, width=625, height=325, relief="raised", bg='#222222')
        self.canvas.config(highlightbackground="#111111")
        self.console = Console(self, height=6, width=75, bd=2, bg='#444444', fg='#BBBBBB')
        self.pack(fill="both", side="right", expand=True)

class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", expand=True, side="left")
        title = tk.Label(self, text="  EMPR IC2  \n\n DMX-512 ", bd=3, font="bold", bg="black", fg="white")
        title.pack(fill="both")
        title.config(highlightbackground="red")
        w = tk.Label(self, text="Red", bg="red", fg="white")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Green", bg="green", fg="black")
        w.pack(fill="x", side="bottom")
        w = tk.Label(self, text="Blue", bg="blue", fg="white")
        w.pack(fill="x", side="bottom")

class Console(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", side="bottom")

class Canvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.pack(fill="both", side="top", expand=True)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main = Main(self, width=625, height=350)
        self.main.config(highlightbackground="#111111")
        self.control = ControlPanel(self, bg="#444444")

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("DMX-512 Project")
    MainApplication(root, width=600, height=350).pack(side="top", fill="both", expand=True)
    root.mainloop()
