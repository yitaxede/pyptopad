import tkinter as tk
import LoginFrame as lf


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # We need to prevent showing the hidden files
        try:
            try:
                self.tk.call("tk_getOpenFile", "-foobarbaz")
            except tk.TclError:
                pass
            self.tk.call("set", "::tk::dialog::file::showHiddenVar", '0')
            self.tk.call("set", "::tk::dialog::file::showHiddenBtn", '0')
        except tk.TclError:
            pass
        # Now hidden files won't be shown
        self.frame = lf.LoginFrame(self)

    def setFrame(self, frame):
        self.frame.destroy()
        self.frame = frame


if __name__ == "__main__":
    Window().mainloop()
