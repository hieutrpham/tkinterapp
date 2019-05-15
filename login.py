import tkinter as tk
from tkinter import ttk

class Login:

    def __init__(self, master):

        master.title('Login')
        master.resizable(False, False)

        self.frame = ttk.Frame(master)
        self.frame.pack()

        self.label_user = ttk.Label(self.frame, text='Username:')
        self.label_user.grid(row=0, column=0)

        self.label_pass = ttk.Label(self.frame, text='Password:')
        self.label_pass.grid(row=1, column=0)

        self.entry_user = ttk.Entry(self.frame)
        self.entry_user.grid(row=0, column=1)

        self.entry_pass = ttk.Entry(self.frame)
        self.entry_pass.grid(row=1, column=1)

        self.button_submit = ttk.Button(self.frame, text='Submit', command=self.submit)
        self.button_submit.grid(row=2, column=0, sticky='e')

        self.button_cancel = ttk.Button(self.frame, text='Cancel', command=self.cancel)
        self.button_cancel.grid(row=2, column=1, sticky='w')

    def submit(self):
        print('submited')

    def cancel(self):
        pass

def main():
    root = tk.Tk()
    Login(root)
    root.mainloop()

if __name__ == '__main__':
    main()