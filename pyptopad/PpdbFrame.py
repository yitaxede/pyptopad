import tkinter as tk
import xml.etree.ElementTree as ET
import gettext
import os
import sys

import LoginFrame as lf

import database as db

FONT = ('DejaVu Sans Mono Bold', 12)

gettext.install('pyptopad', os.path.dirname(sys.argv[0]))


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
        self.scroll1.pack(side='right', fill='y')

        self.lbNotes = tk.Listbox(frame1, font=FONT,
                                  yscrollcommand=self.scroll1.set)
        self.refreshNotes()
        self.lbNotes.bind('<<ListboxSelect>>', self.changeNote)
        self.lbNotes.bind('<Button-3>', self.rmbClicked)
        self.lbNotes.pack(side='left', fill='y')

        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Up", command=self.popupUp)
        self.popup.add_command(label="Down", command=self.popupDown)
        self.popup.add_separator()
        self.popup.add_command(label="Rename", command=self.popupRename)
        self.popup.add_command(label="Clone", command=self.popupClone)
        self.popup.add_command(label="Delete", command=self.popupDelete)
        self.popup.bind('<FocusOut>', lambda e: self.popup.unpost())

        self.scroll1['command'] = self.lbNotes.yview

        frame1.grid(row=0, column=0, columnspan=3,
                    sticky=tk.E+tk.W+tk.S+tk.N)
        # END of Listbox & Scrollbar

        # START of Text & Scrollbar
        frame2 = tk.Frame(self, bd=4, relief='groove')

        self.scroll2 = tk.Scrollbar(frame2)
        self.scroll2.pack(side='right', fill='y')

        self.txtText = tk.Text(frame2, font=FONT, wrap=tk.WORD,
                               yscrollcommand=self.scroll2.set)
        self.txtText.bind('<KeyRelease>', self.textModified)
        self.txtText.bind('<Control-Key-a>', self.textSelectAll)
        self.txtText.bind('<Control-Key-A>', self.textSelectAll)
        self.txtText.pack(side='left', fill='y')

        self.scroll2['command'] = self.txtText.yview
        frame2.grid(row=0, column=3, rowspan=2,
                    sticky=tk.E+tk.W+tk.S+tk.N)
        # END of Text & Scrollbar

        self.btnClose = tk.Button(self, text=_("Close"), font=FONT,
                                  command=self.btnCloseClicked,
                                  anchor=tk.W)
        self.btnClose.grid(row=1, column=0)

        self.btnSave = tk.Button(self, text=_("Save"), font=FONT,
                                 command=self.btnSaveClicked,
                                 anchor=tk.E)
        self.btnSave.grid(row=1, column=1)

        self.btnAdd = tk.Button(self, text='+', font=FONT,
                                command=self.btnAddClicked,
                                anchor=tk.E)
        self.btnAdd.grid(row=1, column=2)

        self.lbNotes.select_set(0)
        if self.ddb.Notes:
            if self.ddb.Notes[0].Texts[0].content:
                self.txtText.insert(tk.END, self.ddb.Notes[0].Texts[0].content)

        self.modified = False
        self.btnSave['state'] = 'disabled'

        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        # When the user decides to exit the app, the app offers the messagebox
        # The user needs to press 'Close' button to return to the LoginFrame
        self.master.protocol('WM_DELETE_WINDOW', self.rUSure)
        self.master.title(file.split('/')[-1] + ' - pyptopad')

    def textModified(self, event):
        if event.state != 0 or event.char == '' or not self.ddb.Notes:
            return
        self.modified = True
        self.btnSave['state'] = 'normal'
        self.master.update_idletasks()

    def textSelectAll(self, event):
        self.txtText.tag_add(tk.SEL, '1.0', tk.END)
        self.txtText.mark_set(tk.INSERT, '1.0')
        self.txtText.see(tk.INSERT)
        return 'break'

    def btnSaveClicked(self):
        if self.ddb.Notes:
            self.saveNote(self.curr)
        self.changeState('disabled')
        self.crypt.write(self.ddb.to_xml_string())
        self.modified = False
        self.btnSave['state'] = 'disabled'
        self.changeState('normal')

    def btnAddClicked(self):
        self.window = tk.Toplevel(self.master)
        self.window.geometry('350x100+' +
                             str(self.master.winfo_x() +
                                 int(self.master.winfo_width() / 2) - 175) +
                             '+' +
                             str(self.master.winfo_y() +
                                 int(self.master.winfo_height() / 2) - 50))
        subFrame = tk.Frame(self.window)
        lblEntry = tk.Label(subFrame,
                            text=_("Enter the title for a new note:"),
                            font=FONT, anchor=tk.W)
        lblEntry.grid(row=0, columnspan=2, sticky=tk.W+tk.E)
        self.text = tk.StringVar()
        entry = tk.Entry(subFrame, textvariable=self.text,
                         font=FONT)
        entry.bind('<Return>', self.checkAdd)
        entry.grid(row=1, columnspan=2, sticky=tk.W+tk.E)
        entry.focus_set()
        butt1 = tk.Button(subFrame, text=_("Add"), font=FONT,
                          command=self.checkAdd, anchor=tk.E)
        butt1.grid(row=2, column=0)
        butt2 = tk.Button(subFrame, text=_("Cancel"), font=FONT,
                          command=self.window.destroy)
        butt2.grid(row=2, column=1)
        subFrame.pack(padx=10, pady=10, expand=True)
        self.window.title(_("New note - ") + self.master.title())

    def btnCloseClicked(self):
        if self.modified:
            self.window = tk.Toplevel(self.master)
            self.window.geometry('450x150+' +
                                 str(self.master.winfo_x() +
                                     int(self.master.winfo_width() / 2) -
                                     225) +
                                 '+' +
                                 str(self.master.winfo_y() +
                                     int(self.master.winfo_height() / 2) -
                                     75))
            subFrame = tk.Frame(self.window)
            label = tk.Label(subFrame, text=_("Do you want to save changes") +
                             _("before returning to login window?\nIf you") +
                             _("don't save, changes will be") +
                             _("permanently lost."),
                             font=FONT, justify=tk.LEFT)
            label.grid(row=0, columnspan=3)
            butt1 = tk.Button(subFrame, text=_("Save & Close"), font=FONT,
                              command=self.subFunc12)
            butt1.grid(row=1, column=0)
            butt2 = tk.Button(subFrame, text=_("Close w/o saving"), font=FONT,
                              command=self.subFunc22)
            butt2.grid(row=1, column=1)
            butt3 = tk.Button(subFrame, text=_("Cancel"), font=FONT,
                              command=self.window.destroy)
            butt3.grid(row=1, column=2)
            subFrame.pack(padx=10, pady=10, expand=True)
            self.window.title(_("Save changes? - ") + self.master.title())
        else:
            self.crypt.close()
            self.master.setFrame(lf.LoginFrame(self.master))

    def rmbClicked(self, event):
        self.lbNotes.select_clear(0, tk.END)
        self.lbNotes.select_set(self.lbNotes.nearest(event.y))
        self.lbNotes.activate(self.lbNotes.nearest(event.y))
        self.changeNote()
        self.popup.post(event.x_root, event.y_root)
        self.popup.focus_set()

    def popupUp(self):
        if self.curr == 0:
            return
        temp = self.ddb.Notes[self.curr]
        self.ddb.Notes[self.curr] = self.ddb.Notes[self.curr - 1]
        self.ddb.Notes[self.curr - 1] = temp
        self.refreshNotes()
        self.curr = self.curr - 1
        self.lbNotes.select_clear(0, tk.END)
        self.lbNotes.select_set(self.curr)
        self.lbNotes.activate(self.curr)
        self.modified = True
        self.btnSave['state'] = 'normal'

    def popupDown(self):
        if self.curr == self.lbNotes.size() - 1:
            return
        temp = self.ddb.Notes[self.curr]
        self.ddb.Notes[self.curr] = self.ddb.Notes[self.curr + 1]
        self.ddb.Notes[self.curr + 1] = temp
        self.refreshNotes()
        self.curr = self.curr + 1
        self.lbNotes.select_clear(0, tk.END)
        self.lbNotes.select_set(self.curr)
        self.lbNotes.activate(self.curr)
        self.modified = True
        self.btnSave['state'] = 'normal'

    def popupRename(self):
        if not self.ddb.Notes:
            return
        self.window = tk.Toplevel(self.master)
        self.window.geometry('350x100+' +
                             str(self.master.winfo_x() +
                                 int(self.master.winfo_width() / 2) - 175) +
                             '+' +
                             str(self.master.winfo_y() +
                                 int(self.master.winfo_height() / 2) - 50))
        subFrame = tk.Frame(self.window)
        lblEntry = tk.Label(subFrame,
                            text=_("Enter the new title:"),
                            font=FONT, anchor=tk.W)
        lblEntry.grid(row=0, columnspan=2, sticky=tk.W+tk.E)
        self.text = tk.StringVar()
        entry = tk.Entry(subFrame, textvariable=self.text,
                         font=FONT)
        entry.bind('<Return>', self.checkRename)
        entry.grid(row=1, columnspan=2, sticky=tk.W+tk.E)
        entry.focus_set()
        butt1 = tk.Button(subFrame, text=_("Rename"), font=FONT,
                          command=self.checkRename, anchor=tk.E)
        butt1.grid(row=2, column=0)
        butt2 = tk.Button(subFrame, text=_("Cancel"), font=FONT,
                          command=self.window.destroy)
        butt2.grid(row=2, column=1)
        subFrame.pack(padx=10, pady=10, expand=True)
        self.window.title(_("Renaming note - ") + self.master.title())

    def popupClone(self):
        if not self.ddb.Notes:
            return
        self.window = tk.Toplevel(self.master)
        self.window.geometry('350x100+' +
                             str(self.master.winfo_x() +
                                 int(self.master.winfo_width() / 2) - 175) +
                             '+' +
                             str(self.master.winfo_y() +
                                 int(self.master.winfo_height() / 2) - 50))
        subFrame = tk.Frame(self.window)
        lblEntry = tk.Label(subFrame,
                            text=_("Enter the title for a new note:"),
                            font=FONT, anchor=tk.W)
        lblEntry.grid(row=0, columnspan=2, sticky=tk.W+tk.E)
        self.text = tk.StringVar()
        entry = tk.Entry(subFrame, textvariable=self.text,
                         font=FONT)
        entry.bind('<Return>', self.checkClone)
        entry.grid(row=1, columnspan=2, sticky=tk.W+tk.E)
        entry.focus_set()
        butt1 = tk.Button(subFrame, text=_("Clone"), font=FONT,
                          command=self.checkClone, anchor=tk.E)
        butt1.grid(row=2, column=0)
        butt2 = tk.Button(subFrame, text=_("Cancel"), font=FONT,
                          command=self.window.destroy)
        butt2.grid(row=2, column=1)
        subFrame.pack(padx=10, pady=10, expand=True)
        self.window.title(_("Cloning note - ") + self.master.title())


    def popupDelete(self):
        if not self.ddb.Notes:
            return
        self.ddb.Notes.pop(self.curr)
        self.refreshNotes()
        self.modified = True
        self.btnSave['state'] = 'normal'
        self.txtText.delete('1.0', tk.END)
        if not self.ddb.Notes:
            self.curr = 0
            return
        self.lbNotes.select_clear(0, tk.END)
        self.lbNotes.select_set(self.curr)
        self.lbNotes.activate(self.curr)
        for x in self.ddb.Notes[self.curr].Texts:
            if x.content:
                self.txtText.insert('1.0', x.content)

    def subFunc1(self):
        self.btnSaveClicked()
        self.crypt.close()
        self.window.destroy()
        self.master.destroy()

    def subFunc2(self):
        self.crypt.close()
        self.window.destroy()
        self.master.destroy()

    def subFunc12(self):
        self.btnSaveClicked()
        self.crypt.close()
        self.window.destroy()
        self.master.setFrame(lf.LoginFrame(self.master))

    def subFunc22(self):
        self.crypt.close()
        self.window.destroy()
        self.master.setFrame(lf.LoginFrame(self.master))

    def rUSure(self, *args):
        if self.modified:
            self.window = tk.Toplevel(self.master)
            self.window.geometry('450x150+' +
                                 str(self.master.winfo_x() +
                                     int(self.master.winfo_width() / 2) -
                                     225) +
                                 '+' +
                                 str(self.master.winfo_y() +
                                     int(self.master.winfo_height() / 2) -
                                     75))
            subFrame = tk.Frame(self.window)
            label = tk.Label(subFrame, text=_("Do you want to save changes") +
                             _("before closing?\nIf you don't save, changes") +
                             _("will be permanently lost."),
                             font=FONT, justify=tk.LEFT)
            label.grid(row=0, columnspan=3)
            butt1 = tk.Button(subFrame, text=_("Save & Close"), font=FONT,
                              command=self.subFunc1)
            butt1.grid(row=1, column=0)
            butt2 = tk.Button(subFrame, text=_("Close w/o saving"), font=FONT,
                              command=self.subFunc2)
            butt2.grid(row=1, column=1)
            butt3 = tk.Button(subFrame, text=_("Cancel"), font=FONT,
                              command=self.window.destroy)
            butt3.grid(row=1, column=2)
            subFrame.pack(padx=10, pady=10, expand=True)
            self.window.title(_("Save changes? - ") + self.master.title())
        else:
            self.crypt.close()
            self.master.destroy()

    def refreshNotes(self):
        self.lbNotes.delete(0, tk.END)
        if self.ddb.Notes:
            for x in self.ddb.Notes:
                self.lbNotes.insert(tk.END, x.attributes['name'])

    def checkAdd(self, *args):
        if self.text.get():
            newNote = ET.fromstring('<note />')
            # Proper addition of 'name' attrib
            newNote.set('name', self.text.get())
            self.ddb.Notes.append(db.Note(newNote))
            self.ddb.Notes[-1].Texts.append(db.Text())
            self.ddb.Notes[-1].Texts[0].content = ''
            self.refreshNotes()
            self.lbNotes.select_clear(0, tk.END)
            self.lbNotes.select_set(tk.END)
            self.lbNotes.activate(tk.END)
            self.changeNote()
            self.txtText.focus_set()
            self.modified = True
            self.btnSave['state'] = 'normal'
            self.master.update_idletasks()
            self.window.destroy()

    def checkRename(self, *args):
        if self.text.get():
            self.ddb.Notes[self.curr].attributes['name'] = self.text.get()
            self.refreshNotes()
            self.lbNotes.select_clear(0, tk.END)
            self.lbNotes.select_set(self.curr)
            self.lbNotes.activate(self.curr)
            self.txtText.focus_set()
            self.modified = True
            self.btnSave['state'] = 'normal'
            self.master.update_idletasks()
            self.window.destroy()

    def checkClone(self, *args):
        if self.text.get():
            newNote = ET.fromstring('<note />')
            # Proper addition of 'name' attrib
            newNote.set('name', self.text.get())
            self.ddb.Notes.append(db.Note(newNote))
            self.ddb.Notes[-1].Texts.append(db.Text())
            old = self.ddb.Notes[self.curr].Texts[0].content
            self.ddb.Notes[-1].Texts[0].content = old
            self.refreshNotes()
            self.lbNotes.select_clear(0, tk.END)
            self.lbNotes.select_set(tk.END)
            self.lbNotes.activate(tk.END)
            self.changeNote()
            self.txtText.focus_set()
            self.modified = True
            self.btnSave['state'] = 'normal'
            self.master.update_idletasks()
            self.window.destroy()

    def changeNote(self, *args):
        if not self.lbNotes.curselection():
            return
        self.saveNote(self.curr)
        self.curr = self.lbNotes.curselection()[0]
        self.txtText.delete('1.0', tk.END)
        for x in self.ddb.Notes[self.curr].Texts:
            if x.content:
                self.txtText.insert('1.0', x.content)

    def changeState(self, state):
        self.lbNotes['state'] = state
        self.txtText['state'] = state
        self.btnClose['state'] = state
        if self.modified:
            self.btnSave['state'] = state
        self.btnAdd['state'] = state
        self.master.update_idletasks()

    def saveNote(self, i):
        self.changeState('disabled')
        self.ddb.Notes[i].Texts[0].content = self.txtText.get('1.0',
                                                              tk.END)[:-1]
        self.changeState('normal')
