import tkinter as tk
import xml.etree.ElementTree as ET

import LoginFrame as lf

import database as db

FONT = ("DejaVu Sans Mono Bold", 12)

class PpdbFrame(tk.Frame):
    def __init__(self, master, file, ddb, crypt):
        tk.Frame.__init__(self, master)

        self.master = master
        self.crypt = crypt
        self.ddb = ddb
        self.curr = 0

        # START OF LISTBOX
        frame1 = tk.Frame(self)

        scroll1 = tk.Scrollbar(frame1)
        scroll1.pack(side="right", fill="y")

        self.lbNotes = tk.Listbox(frame1, font=FONT,
                                  yscrollcommand=scroll1.set)
        self.refreshNotes()
        self.lbNotes.bind('<<ListboxSelect>>', self.changeNote)
        self.lbNotes.pack(side="left", fill="y")

        scroll1["command"] = self.lbNotes.yview

        frame1.grid(row=0, column=0, columnspan=3,
                   sticky=tk.E+tk.W+tk.S+tk.N)
        # END OF LISTBOX

        # START OF TEXT
        frame2 = tk.Frame(self)

        scroll2 = tk.Scrollbar(frame2)
        scroll2.pack(side="right", fill="y")

        self.txtText = tk.Text(frame2, font=FONT,
                               yscrollcommand=scroll2.set)
        self.txtText.pack(side="left", fill="y")

        scroll2["command"] = self.txtText.yview
        frame2.grid(row=0, column=3, rowspan=2,
                    sticky=tk.E+tk.W+tk.S+tk.N)
        #END OF TEXT

        btnClose = tk.Button(self, text="Close", font=FONT,
                            command=self.btnCloseClicked,
                            anchor=tk.W)
        btnClose.grid(row=1, column=0)

        btnSave = tk.Button(self, text="Save", font=FONT,
                            command=self.btnSaveClicked,
                            anchor=tk.E)
        btnSave.grid(row=1, column=1)

        btnAdd = tk.Button(self, text="+", font=FONT,
                           command=self.btnAddClicked,
                           anchor=tk.E)
        btnAdd.grid(row=1, column=2)
        
        self.lbNotes.select_set(0)
        if self.ddb.Notes:
            self.txtText.insert(tk.END, self.ddb.Notes[0].Texts[0].content)

        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.rUSure)
        self.master.title(file.split('/')[-1] + " - pyptopad")

    def btnSaveClicked(self):
        self.saveNote(self.curr)
        self.crypt.write(self.ddb.to_xml_string())

    def btnAddClicked(self):
        self.window = tk.Toplevel(self.master)
        self.text = tk.StringVar()
        entry = tk.Entry(self.window, textvariable=self.text,
                         font=FONT)
        entry.bind("<Return>", self.checkAdd)
        entry.grid(row=0)
        entry.focus_set()
        butt = tk.Button(self.window, text="Add", font=FONT,
                         command=self.checkAdd, anchor=tk.E)
        butt.grid(row=1)

    def btnCloseClicked(self):
        msgbox = tk.messagebox.askquestion("Return to login", 
                                           "Are you sure you want to return")
        if msgbox == "yes":
            self.crypt.close()
            self.master.setFrame(lf.LoginFrame(self.master))

    def rUSure(self, *args):
        msgbox = tk.messagebox.askquestion("Exit application", 
                                           "Are you sure you want to exit the application?")
        if msgbox == "yes":
            self.crypt.close()
            self.master.destroy()

    def refreshNotes(self):
        self.lbNotes.delete(0, tk.END)
        if self.ddb.Notes:
            for x in self.ddb.Notes:
                self.lbNotes.insert(tk.END, x.attributes["name"])

    def checkAdd(self, *args):
        if self.text.get():
            self.ddb.Notes.append(db.Note(ET.fromstring("<note name='" + self.text.get() + "'></note>")))
            self.ddb.Notes[-1].Texts.append(db.Text())
            self.ddb.Notes[-1].Texts[0].content = ""
            self.refreshNotes()
            self.window.destroy()

    def changeNote(self, *args):
        if not self.lbNotes.curselection():
            return
        self.saveNote(self.curr)
        self.curr = self.lbNotes.curselection()[0]
        self.txtText.delete("1.0", tk.END)
        for x in self.ddb.Notes[self.curr].Texts:
            self.txtText.insert(tk.INSERT, x.content)
        
    def saveNote(self, i):
        self.ddb.Notes[i].Texts[0].content = self.txtText.get("1.0", tk.END)[:-1]