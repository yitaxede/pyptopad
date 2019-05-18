import tkinter as tk
import LoginFrame as lf


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = lf.LoginFrame(self)

    def setFrame(self, frame):
        self.frame.destroy()
        self.frame = frame


if __name__ == "__main__":
    Window().mainloop()
