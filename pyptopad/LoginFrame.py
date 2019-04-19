import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import PpdbFrame as pf
import CreatePpdbFrame as cpf

from nacl import exceptions

from cryptor import Cryptor

FONT = ("DejaVu Sans Mono Bold", 12)

class LoginFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text="Database:", font=FONT,
                                anchor=tk.W)
        lblPpdb.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.ppdbPath = tk.StringVar()
        self.entPpdb = tk.Entry(self, textvariable=self.ppdbPath,
                                font=FONT, width=30)
        self.entPpdb.grid(row=1, column=0, sticky=tk.W+tk.E+tk.S+tk.N)

        btnPpdb = tk.Button(self, text="...", font=FONT,
                                 command=self.btnPpdbClicked,
                                 anchor=tk.E)
        btnPpdb.grid(row=1, column=1, sticky=tk.E, ipadx=1)

        lblPass = tk.Label(self, text="Password:", font=FONT,
                                anchor=tk.W)
        lblPass.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.userPass = tk.StringVar()
        self.entPass = tk.Entry(self, font=FONT, show='*',
                                textvariable=self.userPass)
        self.entPass.bind("<Return>", self.btnOpenClicked)
        self.entPass.grid(row=3, column=0, sticky=tk.W+tk.E+tk.S+tk.N)

        btnOpen = tk.Button(self, text="Open", font=FONT,
                                 command=self.btnOpenClicked,
                                 anchor=tk.E)
        btnOpen.grid(row=3, column=1, sticky=tk.E)

        btnNew = tk.Button(self, text="New database", font=FONT,
                           command=self.btnNewClicked)
        btnNew.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.S, pady=20)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.pack(padx=30, pady=20, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.title("pyptopad")

    def btnPpdbClicked(self):
        file = tk.filedialog.askopenfilename(filetypes=(("pyptopad dbs",
                                "*.ppdb"), ("all files", "*.*")))
        if file:
            self.ppdbPath.set(file)

    def btnOpenClicked(self, *args):
        c = Cryptor()
        c.open(self.ppdbPath.get())
        try:
            self.master.setFrame(pf.PpdbFrame(self.master,
                                           file=self.ppdbPath.get(),
                                           xmldb=c.read(self.userPass.get()),
                                            crypt=c))
        except exceptions.CryptoError:
            print("Wrong password")
        '''except Exception as exc:
            print(exc)
            print("Wrong password.")'''
        #c.close()
        '''if self.userPass.get() == "lol":
            self.master.setFrame(PpdbFrame(self.master))
        else:
            tk.messagebox.showerror("WRONG PASSWORD", "Are you kidding me?")'''

    def btnNewClicked(self):
        self.master.setFrame(cpf.CreatePpdbFrame(self.master))