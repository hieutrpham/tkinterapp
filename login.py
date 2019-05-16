import tkinter as tk
from tkinter import ttk

class Login:

    def __init__(self, master):

        master.title('Login')
        master.resizable(False, False)
        master.geometry('220x100')

        self.frame1 = ttk.Frame(master)
        self.frame1.pack()

        self.frame2 = ttk.Frame(master)
        self.frame2.pack()    

        self.label_user = ttk.Label(self.frame1, text='Username:')
        self.label_user.grid(row=0, column=0, pady=2, sticky='e')

        self.entry_user = ttk.Entry(self.frame1)
        self.entry_user.grid(row=0, column=1, pady=2)

        self.label_pass = ttk.Label(self.frame1, text='Password:')
        self.label_pass.grid(row=1, column=0, pady=2, sticky='e')

        self.entry_pass = ttk.Entry(self.frame1, show='*')
        self.entry_pass.grid(row=1, column=1, pady=2, sticky='w')
        
        self.button_submit = ttk.Button(self.frame2, text='Submit', command=self.submit)
        self.button_submit.grid(row=0, column=0, pady=10)

        self.button_cancel = ttk.Button(self.frame2, text='Cancel', command=master.destroy)
        self.button_cancel.grid(row=0, column=1, pady=10)

    def submit(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        print(username, password)

def main():
    root = tk.Tk()
    Login(root)
    root.mainloop()

if __name__ == '__main__':
    main()