import tkinter as tk
import xml.etree.ElementTree as ET

import LoginFrame as lf

import database as db

FONT = ("DejaVu Sans Mono Bold", 12)

class PpdbFrame(tk.Frame):
    def __init__(self, master, file=None, xmldb=None, crypt=None):
        tk.Frame.__init__(self, master)
        self.master = master

        self.file = file
        self.crypt = crypt

        self.d = db.Database(xmldb)

        self.lbNotes = tk.Listbox(self, font=FONT)
        self.refreshNotes()
        self.lbNotes.bind('<<ListboxSelect>>', self.changeNote)
        self.lbNotes.grid(row=0, column=0, columnspan=3,
                          sticky=tk.E+tk.W+tk.S+tk.N,
                          )

        self.txtText = tk.Text(self, font=FONT)
        #self.txtText.insert(tk.INSERT, self.d.Notes[0])
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
        
        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.rUSure)
        self.master.title(file.split('/')[-1] + " - pyptopad")

    def btnSaveClicked(self):
        self.crypt.write(self.d.to_xml_string())
        pass

    def btnAddClicked(self):
        window = tk.Toplevel(self.master)
        self.text = tk.StringVar()
        entry = tk.Entry(window, textvariable=self.text,
                                font=FONT)
        entry.pack()
        butt = tk.Button(window, text="Next", font=FONT,
                            command=self.checkAdd)
        butt.pack()
        '''
        self.d.Notes.append(db.Note().to_xml())
        self.lbNotes.insert(tk.END, self.d.Notes[-1].attributes["name"])
        pass
        '''

    def rUSure(self, *args):
        self.crypt.close()
        msgbox = tk.messagebox.askquestion("Exit application", 
                                           "Are you sure you want to exit the application?")
        if msgbox == "yes":
            self.master.setFrame(lf.LoginFrame(self.master))

    def refreshNotes(self):
        if not self.d.Notes:
            for x in self.d.Notes:
                self.lbNotes.insert(tk.END, x.attributes["name"])

    def checkAdd(self):
        if self.text.get():
            self.d.Notes.append(db.Note(ET.fromstring("<note name='" + self.text.get() + "'></note>")))
            self.lbNotes.insert(tk.END, self.d.Notes[-1].attributes["name"])

    def changeNote(self, *args):
        self.txtText.delete('1.0', tk.END)
        self.txtText.insert(tk.INSERT, self.lbNotes.curselection())
        