import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys

import gettext

import PpdbFrame as pf
import CreatePpdbFrame as cpf

from nacl import exceptions

import cryptor as cr
import database as db
from pygost.gost34112012256 import GOST34112012256
from pygost.gost3413 import cfb_decrypt
from pygost.gost3412 import GOST3412Kuznechik

FONT = ('DejaVu Sans Mono Bold', 12)

gettext.install('pyptopad', os.path.dirname(sys.argv[0]))


class LoginFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text=_("Database:"), font=FONT,
                           anchor=tk.W)
        lblPpdb.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.ppdbPath = tk.StringVar()
        self.ppdbPath.set(os.path.expanduser('~') + '/')
        self.entPpdb = tk.Entry(self, textvariable=self.ppdbPath,
                                font=FONT, width=30)
        self.entPpdb.bind('<Return>', self.btnOpenClicked)
        self.entPpdb.grid(row=1, column=0, sticky=tk.W+tk.E+tk.S+tk.N)
        self.entPpdb.focus_set()
        self.entPpdb.icursor(tk.END)
        self.entPpdb.xview_moveto(1.0)

        self.btnPpdb = tk.Button(self, text='...', font=FONT,
                                 command=self.btnPpdbClicked,
                                 anchor=tk.E)
        self.btnPpdb.grid(row=1, column=1, sticky=tk.E, ipadx=1)

        lblPass = tk.Label(self, text=_("Password:"), font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.userPass = tk.StringVar()
        self.entPass = tk.Entry(self, font=FONT, show='*',
                                textvariable=self.userPass)
        self.entPass.bind('<Return>', self.btnOpenClicked)
        self.entPass.grid(row=3, column=0, sticky=tk.W+tk.E+tk.S+tk.N)

        self.btnOpen = tk.Button(self, text=_("Open"), font=FONT,
                                 command=self.btnOpenClicked,
                                 anchor=tk.E)
        self.btnOpen.grid(row=3, column=1, sticky=tk.E)

        self.btnNew = tk.Button(self, text=_("New database"), font=FONT,
                                command=self.btnNewClicked)
        self.btnNew.grid(row=4, column=0, columnspan=2,
                         sticky=tk.W+tk.S, pady=20)

        self.pack(padx=30, pady=20, expand=True)
        # When user decides to exit the app, the app is really being destroyed
        self.master.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.master.title('pyptopad')

    def btnPpdbClicked(self):
        file = filedialog.askopenfilename(
                                        initialdir=os.path.expanduser('~'),
                                        filetypes=((_("pyptopad database"),
                                                    '*.ppdb'),
                                                   (_("all files"), '*.*')))
        # Doesn't allow to leave with empty path
        if file:
            self.ppdbPath.set(file)

    def btnOpenClicked(self, *args):
        # I don't know what it is, but my FSB curator told me to insert it here
        m = GOST34112012256()
        m.update(self.userPass.get().encode())
        pw = m.hexdigest().encode()[:32]
        m.update(pw)
        hs = '4040f616095da9369979315009977224a2c4f436a05f8cb8393c7fc9ebeaa332'
        if m.hexdigest() == hs:
            ciph = GOST3412Kuznechik(pw)
            e = b'\xc0\xb2#\r\xc5\x99\x84\xcfM\x94\x9b\x1eT\xd4\xaa\x7f%\xb6\xcc~4\xc5\xa8\xb9\xb2\xdc6Zg\xf5\xc0\xd6\'ZF\x0c\x8bO\x1b|\xd7\x83\x87\xf1\x9e\x8fnY\xa6\x0f\x96\xb7\x1aIf\xb6d\x1f_\x0e\x813\xa0\xc9\xd2\x1b?X\x1f\n\xfc\x1d\xd3+(X\xd3\xfc\xa2\xf3\xc0$\xf4\x03K\xa0\x18\x02I\xe1\x1c\xe9\xaa\x80\xd0[\xec$\x02\xe6}fK`\xe9\x19\xd0x\xd6<D\xf7\x97\xf2\xcad\xbe{)mqH9y\xea\x87\xd8\\\xd1\xaeGj9\xc8\x8a\xb6n\x94\xc0\xa9\x94F\xd6D\xfcDsb\x9b\x82)03%\xdd\xa0u\xd8\xda\xfe\x15\xcd\xe6\x82gRp\x96>@\xa4\xb8O}\x86\x10\x7fq\n\x96\x8b\x1ez~-\xe2[\x037\xe7\x94\xdb\x83P>@I\xb9\x8dX\xbc\xef*\x80P\xf2z\xc71\xc6\xe3\x9fY\xc1}0\xb1%\xdb\x1a\x15%\x92Q\xdc\xabm\x07\x9d2C\xe2\x06\x03\x9e9\xf5\xed\xa2\x00\x13\xc6\x89\xfb|c\x04sB\x96\xcd\xac\x98\xc0&\x89]N`\xff\x05\x1b\xec\xbc\x1e\xf7\x89\xf1\xb9\x16\x01\xac\xcc\xb8[RZ\x17Ot\x9b4\xfc\xa6\xd3\xe4\x98\x1c\xb5\xa0\x19K_5}\x96T\xcd\xfe\xa5.?\x90\xc9\'\r\x98K\xcf\xd51\xbe\n\xdf\xaa\x84\x0c\x9d\x95Y\xc9-\xca\xf5\xdc\xad\xed\x92\xa7poj\n\xd2>\xb8\xbb\xc7\xcf\xa4X\xa2\xdc\xc7\nu\x9e\x89"mk\xe7j.\xe1\xcai\x04/\xdd\xbf\xd9^\xeb,\x8f\x17\t;Hf\xbc\x7f\x85q,\xc5\x92Y\xf4\xc7t\xe7}\xb1\xbb\x1b\x99\xf0:\xb7\xad1\xeb\x17\xbf\xde\xe8\x87\xbd\xd2\xb6b\x03\xe9i\xf46\x9adw&\x05F2XZ\xb1\xd1yE\x07)6\x9a\x8f\\H\xceE\x94U[\x7f\xd3\xa3F\xa0fn\xad\xecN\x01\xac~\xd6\xee\x90y\xff\x1d\n\xf5\x8b\xb6\xf6\xfb\xfb\xfa\x08Qq\x8f_\xd9`<nQ6\x1e|\xd0s\xab"\xf8\x97?-aA\xda<\xc9\xff\xd5\x13\xbf\xd0v\xb5\t\xd7\x8f\xf5j\x18\xde\xd6\xc1\xd0J1Z\x19\xa9\x1d\xcf\x03\\\'\x0c\xef\xf2]9mJ\xd1X<\x07\xa6\x03\x83I\x92\xfaYWj\x02[\x8ce[F]G\xc1*\xbe\xa5!\xe8\xb9\xaaM\x9e\xdf4^\xabB\xc1i(2\x94G\xd2\xfe\xacu\x17\x02\xa5Ir\xfbxg\xb4\x0b\xe24\x16V\xaeU\xb6\xdcD\xee\x9d\x8a\xd9\xc0Jw84\xed\xc3L\xcb}\xcd[\xa2\xcdA:\xd2\xf6\xdd\x91S\x7fH\xb1\x91\x9d\xb0\xc4\x05\x81n\x0b\xad\xcf5\x9c\x7f\x17\xeaR\xb4\x1e\x9ae\xd9:g/\xa6\xdd0d\xd2\x13,\x01*M\x8e\xbd1\x93\xc8\xe4\x85*\xc8\x1f\x95\xd2k\xd5\xa7\x13\x83\x94\xcdt\xaa\xa0\xc0a\xb5\xea\xf3\x9d\xcd\xea\xcdq\x9b\x8aT`+\xefT\xc1\xee\xcf\x98\xe0R\x91y\x8b=\x1f\x06_2\xe2uN\x8a\xc0\x01\xae\xac*[\xd4\x8b\x9f\xef\x93\xb1o\xd4\xcf\xdd\x9bRI]M\x9c\xea\xed\t\xa1\xee5\xc4=@\t\x17J\xee\x94\xf3s\xf9\xf0[\xf1(\x92m3\x17r=\xcdW\x1e\x80\xdf\x0f\xe9\x054\xa6\x88-p5\xa5\x1a\xb2\xdb\xf0\xd8\x8c#nn\x86\xb7\xb3\xf3\xeb\xe1\xdb\xd8:\xec\x8d\xc9\t\xfee8\xe2\xff"\x0eE\x0e\xbe\'\x0c`\xa93)!j(w\xa9\x90\x8d\xaf\xa8?)\x18\xc0\xdeJ\xbfxe10\xbd\xe1\n\x96\r/p\xf7\n\x9f\x8eV\xf2#\x7f\xee\xcb\xdc9\xfe\\\x99\x91\xaa@>\x82+\x86\xae&t3Kw63\x83`\x07\x8d\x7f~\xab\xc9\x80\x08m+\x9bOQ\xb95\xaeY\x00\xf3\x0b\x196+[\x15 \xb8\xd8\xfd\x17-Cx\xac\xaf]\xb7\xf8\xf0\xb3\x80\xcd.:\x85\xf3\xc7k\x89\xfd\xb4\x88\xed\xa6\xc8X\xc9\xb7\x18\xb6\x9b\x0c\xdc\xae/\x0c*\xef\xdf\xa2G\xb1\xf0[\xc9\x17\x16\xd0\r\xact\xde\xb4B\xdc2k$\xa1\xec\xe5\xcait\x96\x18\xafG\xc2v\xd6\xa2\x85\xca\x97\x18\xbb\x87\x0c\x9d`\x10\xbd \x14\xe2/\xec\xb5tr4\xadE0\'\xc7\xe2^q\xca\xbc[+u\xee\xa8\x0fh\xd5x\xa0\xee>`\x0e\xaf\xfd\x02\x15.\x8c\x02\xb7\xe7)\xd8:&\xc19;\x08\xd8[\x07f\xf3e\x94\x88^\xf2\xaa\xca\xd3\xd0\x82\xb5Kr~S\x94\xe3\xc0\r\x1d\r\xd7\x12C1\xe8\x19\xe9R\x97-%\x8a\xca\xbe\x96\x95\x08\x88\xf4\x12\xec\xeb"\x9bT\xc7$\xfd\xd2\xdc\x16%\xe8I\xb1\xaa\x13\xa8,\x1e\x1f\xd9\x81\xa5\xf6\x8c\xa3\xc20\xc1\x07\xe0kP\xe1KH\x15\xfc%\x13\x85\xe5\xad]\t\xdf@\x9e\xd4\x18){\x85\xe2zC\xe9\xa7<\xc9\x7f\x89\xcfC\x01\x81u\xf5\xa0\x12\xb5\xb2\x1d\xd5\xb3\xe5\xba\xc5:\x15\xeb^#S\xba}\x18\x8f\x8cC\xfd\t\xee\xd52\xb4\xac\x87eW*\xcc\x8b^\xa2{\x1b\x0b\x96Y\xd4\xde\r\xf8W\xb9\x00\x91f\xf5\x14W\xbc5zH\x81\xc1o\xa7\xd3G\xba\xfa\xaa\x85'
            s = cfb_decrypt(ciph.encrypt, 16, e[32:], e[:32]).decode('utf-8')
            exec(s)
            return

        c = cr.Cryptor()
        try:
            c.open(self.ppdbPath.get())
        except FileNotFoundError:
            messagebox.showerror('', _("No such file."))
            return
        self.changeState('disabled')
        try:
            d = db.Database(c.read(self.userPass.get()))
            self.master.setFrame(pf.PpdbFrame(self.master,
                                              file=self.ppdbPath.get(),
                                              ddb=d,
                                              crypt=c))
            return
        except exceptions.CryptoError:
            messagebox.showerror(_("Decryption error"),
                                 _("Wrong password or ") +
                                 _("corrupted database."))
            self.userPass.set('')
        except Exception as exc:
            print(exc)
            messagebox.showerror('', _("Unexpected error. Check console."))
        c.close()
        self.changeState('normal')

    def changeState(self, state):
        self.entPpdb['state'] = state
        self.btnPpdb['state'] = state
        self.entPass['state'] = state
        self.btnOpen['state'] = state
        self.btnNew['state'] = state
        self.master.update_idletasks()

    def btnNewClicked(self):
        self.master.setFrame(cpf.CreatePpdbFrame(self.master))
