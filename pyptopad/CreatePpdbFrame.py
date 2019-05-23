import tkinter as tk
import gettext
import os
import sys

import pyptopad.LoginFrame as lf

import pyptopad.cryptor as cr
import pyptopad.database as db

FONT = ('DejaVu Sans Mono Bold', 12)
SFONT = (FONT[0], FONT[1] - 2)

# gettext.install('pyptopad', os.path.dirname(sys.argv[0]) + 'pyptopad/')
gettext.install('pyptopad', os.path.join(os.path.dirname(__file__),'locale'))

class CreatePpdbFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text=_("Location:"), font=FONT,
                           anchor=tk.W)
        lblPpdb.grid(row=0, column=0, sticky=tk.W)

        self.ppdbPath = tk.StringVar()
        self.ppdbPath.set(os.path.expanduser('~') + '/')
        self.entPpdb = tk.Entry(self, textvariable=self.ppdbPath,
                                font=FONT, width=30)
        self.entPpdb.grid(row=1, column=0, columnspan=3,
                          sticky=tk.W+tk.E+tk.S+tk.N)
        self.entPpdb.focus_set()
        self.entPpdb.icursor(tk.END)
        self.entPpdb.xview_moveto(1.0)

        self.btnPpdb = tk.Button(self, text='...', font=FONT,
                                 command=self.btnPpdbClicked,
                                 anchor=tk.E)
        self.btnPpdb.grid(row=1, column=3, sticky=tk.E)

        lblPass = tk.Label(self, text=_("Password:"), font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=2, column=0, sticky=tk.W)

        self.userPass1 = tk.StringVar()
        self.entPass1 = tk.Entry(self, font=FONT, show='*',
                                 textvariable=self.userPass1)
        self.entPass1.grid(row=3, column=0, columnspan=4,
                           sticky=tk.W+tk.E+tk.S+tk.N)

        lblPass = tk.Label(self, text=_("Repeat password:"), font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=4, column=0, sticky=tk.W+tk.E)

        self.userPass2 = tk.StringVar()
        self.entPass2 = tk.Entry(self, font=FONT, show='*',
                                 textvariable=self.userPass2, width=3)
        self.entPass2.bind('<Return>', self.btnCreateClicked)
        self.entPass2.grid(row=5, column=0, columnspan=4,
                           sticky=tk.W+tk.E+tk.S+tk.N)

        lblSec = tk.Label(self, text=_("Security mode:"), font=FONT,
                          anchor=tk.W)
        lblSec.grid(row=6, column=0, sticky=tk.W+tk.E)

        self.secMode = tk.IntVar()
        self.sclSec = tk.Scale(self, font=FONT, orient=tk.HORIZONTAL,
                               showvalue=0,
                               variable=self.secMode, to=2,
                               command=self.changeSecMode)
        self.sclSec.grid(row=7, column=0, columnspan=4,
                         sticky=tk.W+tk.E+tk.S+tk.N)

        self.secModeStr = tk.StringVar()
        self.lblSecMode = tk.Label(self, font=FONT,
                                   textvariable=self.secModeStr, anchor=tk.W)
        self.lblSecMode.grid(row=8, column=0, columnspan=4,
                             sticky=tk.W)

        self.secModeDescr = tk.StringVar()
        lblSecModeDescr = tk.Label(self, font=SFONT,
                                   textvariable=self.secModeDescr,
                                   anchor=tk.W, justify=tk.LEFT)
        lblSecModeDescr.grid(row=9, column=0, columnspan=4,
                             sticky=tk.W)

        self.benchResult = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.benchResult[0].set('...')
        self.benchResult[1].set('...')
        self.benchResult[2].set('...')

        self.benchTxt = tk.StringVar()
        self.benchTxt.set(_("Run benchmark to see how long decryption will")
                          + '\n' +
                          _("take on your device in each security mode.")
                          + '\n\n')

        lblBench = tk.Label(self, font=SFONT, textvariable=self.benchTxt,
                            anchor=tk.W, justify=tk.LEFT,
                            bd=4, relief='groove')
        lblBench.grid(row=10, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.btnCancel = tk.Button(self, text=_("Cancel"), font=FONT,
                                   command=self.closeWindow,
                                   anchor=tk.W)
        self.btnCancel.grid(row=11, column=0, sticky=tk.W)

        self.btnBench = tk.Button(self, text=_("Run benchmark"), font=FONT,
                                  command=self.benchmark,
                                  anchor=tk.E)
        self.btnBench.grid(row=11, column=2, sticky=tk.E)

        self.btnCreate = tk.Button(self, text=_("Create"), font=FONT,
                                   command=self.btnCreateClicked,
                                   anchor=tk.E)
        self.btnCreate.grid(row=11, column=3, sticky=tk.E)

        self.changeSecMode('0')

        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        # When user decides to exit the app, the app brings back LoginFrame
        self.master.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.master.title(_("Creating Database") + ' - pyptopad')

    def btnPpdbClicked(self):
        file = tk.filedialog.asksaveasfilename(
                                            initialdir=os.path.expanduser('~'),
                                            filetypes=((_("pyptopad database"),
                                                        '*.ppdb'),
                                                       (_("all files"),
                                                        '*.*')))
        if file:
            self.ppdbPath.set(file)
            self.entPpdb.icursor(tk.END)
            self.entPpdb.xview_moveto(1.0)

    def btnCreateClicked(self, *args):
        if self.userPass1.get() != self.userPass2.get():
            tk.messagebox.showerror('', _("Passwords don't match."))
            self.userPass1.set('')
            self.userPass2.set('')
            return
        c = cr.Cryptor()
        self.changeState('disabled')
        try:
            c.create(self.ppdbPath.get(),
                     self.userPass1.get(),
                     self.secMode.get())
        except Exception:
            tk.messagebox.showerror('', _("Wrong file path."))
            self.changeState('normal')
            return
        d = db.Database()
        c.write(d.to_xml_string())
        c.close()
        self.closeWindow()

    def changeSecMode(self, mode):
        if mode == '0':
            self.lblSecMode['fg'] = 'green'
            self.secModeStr.set(_("Nothing to Hide"))
            descr = _("I put perfomance above security.") + '\n' \
                + _("In this mode decryption is quickest,") + '\n' \
                + _("but you better use a strong password.")
            self.secModeDescr.set(descr)
        elif mode == '1':
            self.lblSecMode['fg'] = 'dark goldenrod'
            self.secModeStr.set(_("Standard"))
            descr = _("Decrypion takes a little bit longer in this mode,") \
                + '\n' + _("which makes brute-force attacks harder.") + '\n'
            self.secModeDescr.set(descr)
        elif mode == '2':
            self.lblSecMode['fg'] = 'red'
            self.secModeStr.set(_("Paranoia"))
            descr = _("Just because you're paranoid,") + '\n' \
                + _("doesn't mean they're not watching you.") + '\n'
            self.secModeDescr.set(descr)

    def refreshBench(self):
        self.benchTxt.set(_("On this device decryption is going to take:")
                          + '\n'
                          + self.benchResult[0].get()
                          + _("s with Nothing to Hide Security Mode") + '\n'
                          + self.benchResult[1].get()
                          + _("s with Standard Security Mode") + '\n'
                          + self.benchResult[2].get()
                          + _("s with Paranoia Security Mode"))

    def changeState(self, state):
        self.master.update()
        self.master.update_idletasks()
        self.entPpdb['state'] = state
        self.btnPpdb['state'] = state
        self.entPass1['state'] = state
        self.entPass2['state'] = state
        self.btnCancel['state'] = state
        self.btnBench['state'] = state
        self.btnCreate['state'] = state
        self.sclSec['state'] = state
        self.master.update()
        self.master.update_idletasks()

    def benchmark(self, *args):
        self.benchResult[0].set('...')
        self.benchResult[1].set('...')
        self.benchResult[2].set('...')
        self.btnBench['text'] = _("Running...")
        self.refreshBench()
        self.changeState('disabled')
        self.benchResult[0].set(str(round(cr.benchmark(0), 2)))
        self.refreshBench()
        self.master.update_idletasks()
        self.benchResult[1].set(str(round(cr.benchmark(1), 2)))
        self.refreshBench()
        self.master.update_idletasks()
        self.benchResult[2].set(str(round(cr.benchmark(2), 2)))
        self.refreshBench()
        self.btnBench['text'] = _("Run benchmark")
        self.changeState('normal')

    def closeWindow(self):
        self.master.setFrame(lf.LoginFrame(self.master))
