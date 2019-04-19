import tkinter as tk

import LoginFrame as lf

from cryptor import Cryptor
import database as db

FONT = ("DejaVu Sans Mono Bold", 12)

class CreatePpdbFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text="New database:", font=FONT,
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

        self.secMode = tk.IntVar()
        sclSec = tk.Scale(self, font=FONT, orient=tk.HORIZONTAL,
                          variable=self.secMode, to=2)
        sclSec.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E+tk.S+tk.N)

        lblPass = tk.Label(self, text="Password:", font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.userPass1 = tk.StringVar()
        self.entPass1 = tk.Entry(self, font=FONT, show='*',
                                textvariable=self.userPass1)
        self.entPass1.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E+tk.S+tk.N)

        lblPass = tk.Label(self, text="Repeat password:", font=FONT,
                                anchor=tk.W)
        lblPass.grid(row=5, column=0, sticky=tk.W+tk.E)

        self.userPass2 = tk.StringVar()
        self.entPass2 = tk.Entry(self, font=FONT, show='*',
                                textvariable=self.userPass2)
        self.entPass2.bind("<Return>", self.btnCreateClicked)
        self.entPass2.grid(row=6, column=0, columnspan=2, sticky=tk.W+tk.E+tk.S+tk.N)

        btnCreate = tk.Button(self, text="Create DB", font=FONT,
                             command=self.btnCreateClicked,
                             anchor=tk.E)
        btnCreate.grid(row=7, column=1, sticky=tk.E)


        
        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.master.title("New database - pyptopad")

    def btnPpdbClicked(self):
        file = tk.filedialog.asksaveasfilename(filetypes=(("pyptopad dbs",
                                "*.ppdb"), ("all files", "*.*")))
        if file:
            self.ppdbPath.set(file)

    def btnCreateClicked(self, *args):
        if self.userPass1.get() != self.userPass2.get():
            print("Passwords don't match")
            return
        self.entPass1['state'] = "disabled"
        c = Cryptor()
        print(self.ppdbPath.get(), self.userPass1.get(), self.secMode.get())
        try:
            c.create(self.ppdbPath.get(), self.userPass1.get(), self.secMode.get())
        except FileNotFoundError:
            print("Wrong file")
            self.entPass1["state"] = "normal"
            return
        d = db.Database()
        c.write(d.to_xml_string())
        c.close()
        self.closeWindow()

    def closeWindow(self):
        self.master.setFrame(lf.LoginFrame(self.master))