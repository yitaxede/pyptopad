import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import PpdbFrame as pf
import CreatePpdbFrame as cpf

from nacl import exceptions

import cryptor as cr
import database as db

FONT = ("DejaVu Sans Mono Bold", 12)

class LoginFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text="Database:", font=FONT,
                           anchor=tk.W)
        lblPpdb.grid(row=0, column=0, sticky=tk.W+tk.E)

        # No default path yet
        self.ppdbPath = tk.StringVar()
        self.entPpdb = tk.Entry(self, textvariable=self.ppdbPath,
                                font=FONT, width=30)
        self.entPpdb.bind("<Return>", self.btnOpenClicked)
        self.entPpdb.grid(row=1, column=0, sticky=tk.W+tk.E+tk.S+tk.N)
        # Actually usable focus on entry
        self.entPpdb.focus_set()

        self.btnPpdb = tk.Button(self, text="...", font=FONT,
                                 command=self.btnPpdbClicked,
                                 anchor=tk.E)
        self.btnPpdb.grid(row=1, column=1, sticky=tk.E, ipadx=1)

        lblPass = tk.Label(self, text="Password:", font=FONT,
                                anchor=tk.W)
        lblPass.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.userPass = tk.StringVar()
        self.entPass = tk.Entry(self, font=FONT, show='*',
                                textvariable=self.userPass)
        self.entPass.bind("<Return>", self.btnOpenClicked)
        self.entPass.grid(row=3, column=0, sticky=tk.W+tk.E+tk.S+tk.N)

        self.btnOpen = tk.Button(self, text="Open", font=FONT,
                                 command=self.btnOpenClicked,
                                 anchor=tk.E)
        self.btnOpen.grid(row=3, column=1, sticky=tk.E)

        self.btnNew = tk.Button(self, text="New database", font=FONT,
                                command=self.btnNewClicked)
        self.btnNew.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.S, pady=20)

        self.pack(padx=30, pady=20, expand=True)
        # When user decides to exit the app, the app is really being destroyed
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.title("pyptopad")

    def btnPpdbClicked(self):
        file = tk.filedialog.askopenfilename(filetypes=(("pyptopad dbs",
                                "*.ppdb"), ("all files", "*.*")))
        # Doesn't allow to leave with empty path
        if file:
            self.ppdbPath.set(file)

    def btnOpenClicked(self, *args):
        c = cr.Cryptor()
        try:
            c.open(self.ppdbPath.get())
        except FileNotFoundError:
            tk.messagebox.showerror("", "No such file.")
            return
        self.changeState("disabled")
        try:
            d = db.Database(c.read(self.userPass.get()))
            self.master.setFrame(pf.PpdbFrame(self.master,
                                              file=self.ppdbPath.get(),
                                              ddb=d,
                                              crypt=c))
            return
        except exceptions.CryptoError:
            tk.messagebox.showerror("", "Wrong password.")
        except Exception as exc:
            print(exc)
            tk.messagebox.showerror("", "Unexpected error. Check console.")
        c.close()
        self.changeState("normal")

    def changeState(self, state):
        self.entPpdb["state"] = state
        self.btnPpdb["state"] = state
        self.entPass["state"] = state
        self.btnOpen["state"] = state
        self.btnNew["state"] = state
        self.master.update_idletasks()

    def btnNewClicked(self):
        self.master.setFrame(cpf.CreatePpdbFrame(self.master))
