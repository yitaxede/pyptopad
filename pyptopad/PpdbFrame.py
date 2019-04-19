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

        frame = tk.Frame(self)

        scroll = tk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")

        self.lbNotes = tk.Listbox(frame, font=FONT, yscrollcommand=scroll.set)
        self.refreshNotes()
        self.lbNotes.bind('<<ListboxSelect>>', self.changeNote)
        self.lbNotes.pack(side="left", fill="y")

        scroll["command"] = self.lbNotes.yview

        frame.grid(row=0, column=0, columnspan=3,
                   sticky=tk.E+tk.W+tk.S+tk.N)

        self.txtText = tk.Text(self, font=FONT)
        self.txtText.grid(row=0, column=3, rowspan=2,
                          sticky=tk.E+tk.W+tk.S+tk.N)

        btnSave = tk.Button(self, text="Save", font=FONT,
                            command=self.btnSaveClicked,
                            anchor=tk.W)
        btnSave.grid(row=1, column=0, columnspan=2)

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
        entry.pack()
        butt = tk.Button(self.window, text="Add", font=FONT,
                         command=self.checkAdd)
        butt.pack()

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

    def checkAdd(self):
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