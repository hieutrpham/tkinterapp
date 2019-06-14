import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import cx_Oracle as cx
from pricecheck import run


ip = 'ORAPROD.FRTSERVICES.COM'
port = 1522
SID = 'PROD01.FRTSERVICES.COM'
dsn_tns = cx.makedsn(ip, port, service_name=SID)
tables = ['TRANSACTION', 'TRANSACTION_ARCHIVE', 'TRANSACTION_INELIGIBLE']


class FRT(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        tk.Tk.iconbitmap(self, default=r'C:\Users\hpham\Documents\GitHub\tkinterapp\got.ico')
        tk.Tk.wm_title(self, 'Sea of FRT')
        
        self.file_path = None
        self.username = None
        self.password = None
        self.currency = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)  

        label_user = ttk.Label(container, text='Username:')
        label_user.pack()

        self.entry_user = ttk.Entry(container)
        self.entry_user.pack(pady=5,padx=5)

        label_pass = ttk.Label(container, text='Password:')
        label_pass.pack()

        self.entry_pass = ttk.Entry(container, show='*')
        self.entry_pass.pack(pady=5,padx=5)

        button_browse = ttk.Button(container, text='Browse', command=self.browse_file)
        button_browse.pack(pady=5,padx=5)

        self.file_entry = ttk.Entry(container, textvariable=self.file_path)
        self.file_entry.pack(pady=5,padx=5)

        label_currency = ttk.Label(container, text='Currency to check')
        label_currency.pack()

        self.currency_entry = ttk.Entry(container, textvariable=self.currency)
        self.currency_entry.pack()

        button_price_check = ttk.Button(container, text='Price Check', command=lambda: run(self.username, self.password, dsn_tns, self.file_path, self.currency, tables))
        button_price_check.pack(pady=5,padx=5)

    def browse_file(self):
        self.file_path = fd.askopenfilename(initialdir=r"C:\Users",
                                filetypes=(("All files", "*.*"),))
        self.file_entry.delete(0, tk.END)                                
        self.file_entry.insert(0, self.file_path)

app = FRT()
app.geometry('250x250')
app.mainloop()