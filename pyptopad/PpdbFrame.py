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

        # START of Listbox & Scrollbar
        frame1 = tk.Frame(self)

        self.scroll1 = tk.Scrollbar(frame1)
        self.scroll1.pack(side="right", fill="y")

        self.lbNotes = tk.Listbox(frame1, font=FONT,
                                  yscrollcommand=self.scroll1.set)
        self.refreshNotes()
        self.lbNotes.bind('<<ListboxSelect>>', self.changeNote)
        self.lbNotes.pack(side="left", fill="y")

        self.scroll1["command"] = self.lbNotes.yview

        frame1.grid(row=0, column=0, columnspan=3,
                    sticky=tk.E+tk.W+tk.S+tk.N)
        # END of Listbox & Scrollbar

        # START of Text & Scrollbar
        frame2 = tk.Frame(self, bd=4, relief="groove")

        self.scroll2 = tk.Scrollbar(frame2)
        self.scroll2.pack(side="right", fill="y")

        self.txtText = tk.Text(frame2, font=FONT,
                               yscrollcommand=self.scroll2.set)
        self.txtText.pack(side="left", fill="y")

        self.scroll2["command"] = self.txtText.yview
        frame2.grid(row=0, column=3, rowspan=2,
                    sticky=tk.E+tk.W+tk.S+tk.N)
        # END of Text & Scrollbar

        self.btnClose = tk.Button(self, text="Close", font=FONT,
                                  command=self.btnCloseClicked,
                                  anchor=tk.W)
        self.btnClose.grid(row=1, column=0)

        self.btnSave = tk.Button(self, text="Save", font=FONT,
                                 command=self.btnSaveClicked,
                                 anchor=tk.E)
        self.btnSave.grid(row=1, column=1)

        self.btnAdd = tk.Button(self, text="+", font=FONT,
                                command=self.btnAddClicked,
                                anchor=tk.E)
        self.btnAdd.grid(row=1, column=2)

        self.lbNotes.select_set(0)
        if self.ddb.Notes:
            self.txtText.insert(tk.END, self.ddb.Notes[0].Texts[0].content)

        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        # When the user decides to exit the app, the app offers the messagebox
        # The user needs to press 'Close' button to return to the LoginFrame
        self.master.protocol("WM_DELETE_WINDOW", self.rUSure)
        self.master.title(file.split('/')[-1] + " - pyptopad")

    def btnSaveClicked(self):
        self.saveNote(self.curr)
        self.changeState("disabled")
        self.crypt.write(self.ddb.to_xml_string())
        self.changeState("normal")

    def btnAddClicked(self):
        self.window = tk.Toplevel(self.master)
        self.window.geometry("350x100+" + str(self.master.winfo_x() +
                                              int(self.master.winfo_width() / 2) -
                                              175) +
                             '+' + str(self.master.winfo_y() +
                                       int(self.master.winfo_height() / 2) - 50))
        subFrame = tk.Frame(self.window)
        lblEntry = tk.Label(subFrame, text="Enter the title for a new note:",
                            font=FONT, anchor=tk.W)
        lblEntry.grid(row=0, columnspan=2, sticky=tk.W+tk.E)
        self.text = tk.StringVar()
        entry = tk.Entry(subFrame, textvariable=self.text,
                         font=FONT)
        entry.bind("<Return>", self.checkAdd)
        entry.grid(row=1, columnspan=2, sticky=tk.W+tk.E)
        entry.focus_set()
        butt1 = tk.Button(subFrame, text="Add", font=FONT,
                          command=self.checkAdd, anchor=tk.E)
        butt1.grid(row=2, column=0)
        butt2 = tk.Button(subFrame, text="Cancel", font=FONT,
                          command=self.window.destroy)
        butt2.grid(row=2, column=1)
        subFrame.pack(padx=10, pady=10, expand=True)
        self.window.title("New note - " + self.master.title())

    def btnCloseClicked(self):
        msgbox = tk.messagebox.askquestion("Return to login window",
                                           "Are you sure you want to return?")
        if msgbox == "yes":
            self.crypt.close()
            self.master.setFrame(lf.LoginFrame(self.master))

    def rUSure(self, *args):
        msgbox = tk.messagebox.askquestion("Close pyptopad",
                                           "Are you sure?")
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
            newNote = ET.fromstring("<note />")
            # Proper addition of 'name' attrib
            newNote.set("name", self.text.get())
            self.ddb.Notes.append(db.Note(newNote))
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
            self.txtText.insert("1.0", x.content)

    def changeState(self, state):
        self.lbNotes["state"] = state
        self.txtText["state"] = state
        self.btnClose["state"] = state
        self.btnSave["state"] = state
        self.btnAdd["state"] = state
        self.master.update_idletasks()

    def saveNote(self, i):
        self.changeState("disabled")
        self.ddb.Notes[i].Texts[0].content = self.txtText.get("1.0",
                                                              tk.END)[:-1]
        self.changeState("normal")
