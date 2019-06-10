import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


exchange = 'BTC-e'
datcounter = 9000
program_name = 'btce'

def change_exchange(towhat, pn):
    global exchange
    global datcounter
    global program_name

    exchange = towhat
    program_name = pn
    datcounter = 9000


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default=r'C:\Users\hieup\Documents\GitHub\tkinterapp\got.ico')
        tk.Tk.wm_title(self, 'Sea of BTC')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command=lambda: msg.showinfo('Tile', 'Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        exchange = tk.Menu(menubar, tearoff=1)
        exchange.add_command(label='BTC-e', command=lambda: change_exchange('BTC-e', 'btce'))
        exchange.add_command(label='Bitfinex', command=lambda: change_exchange('Bitfinex', 'bitfinex'))
        exchange.add_command(label='Bitstamp', command=lambda: change_exchange('Bitstamp', 'bitstamp'))
        exchange.add_command(label='Huobi', command=lambda: change_exchange('Huobi', 'huobi'))
        menubar.add_cascade(label='Exchange', menu=exchange)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, controller=self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page): # raise the page you wanna show

        frame = self.frames[page]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        


app = SeaofBTCapp()
app.geometry('500x500')
app.mainloop()