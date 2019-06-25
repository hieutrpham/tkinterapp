import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc as candle
from alpha_vantage.timeseries import TimeSeries as ts
from alpha_vantage.cryptocurrencies import CryptoCurrencies as cc
# from utilities import Info
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

lightcolor = '#00A3E0'
darkcolor = '#183A54'
alpha_key = 'EAY8N3YJIB72Q35C'

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        # tk.Tk.iconbitmap(self, default=r'C:\Users\hpham\Documents\GitHub\tkinterapp\got.ico')
        
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

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for F in (StartPage, PageOne):

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

        self.symbol_entry = tk.Entry(self)
        self.symbol_entry.bind("<Return>", (lambda event: self.get_stock(self.symbol_entry.get())))
        self.symbol_entry.pack(pady=5)

        self.figure = Figure(figsize=(5,4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.get_crypto('btc')

    def get_crypto(self, coin):

        self.ax.clear()

        df = cc(key=alpha_key, output_format='pandas')
        crypto = df.get_digital_currency_daily(coin, 'USD')[0].reset_index()
        crypto.sort_values(by='date', ascending=False, inplace=True)
        crypto = crypto.iloc[:100, :]
        crypto['date'] = pd.to_datetime(crypto['date'])
        crypto["MPLDates"] = crypto["date"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

        candle(self.ax, crypto[['MPLDates', '1a. open (USD)', '2a. high (USD)', '3a. low (USD)', '4a. close (USD)']].values, colorup=lightcolor, colordown=darkcolor)
        
        # for label in self.ax.xaxis.get_ticklabels():
        #     label.set_rotation(45)
        
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.figure.autofmt_xdate()
        # self.figure.tight_layout()
        self.ax.set_ylabel('Price')
        self.ax.set_xlabel('Date')
        self.ax.set_title(f'{coin.upper()} Daily Prices')
        self.canvas.draw()

    def get_stock(self, stock):

        self.ax.clear()

        df = ts(key=alpha_key, output_format='pandas')
        stock_data = df.get_daily_adjusted(stock, 'USD')[0].reset_index()
        stock_data.sort_values(by='date', ascending=False, inplace=True)
        stock_data = stock_data.iloc[:100, :]
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data["MPLDates"] = stock_data["date"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

        candle(self.ax, stock_data[['MPLDates', '1. open', '2. high', '3. low', '4. close']].values, colorup=lightcolor, colordown=darkcolor)
        
        # for label in self.ax.xaxis.get_ticklabels():
        #     label.set_rotation(45)
        
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.figure.autofmt_xdate()
        # self.figure.tight_layout()
        self.ax.set_ylabel('Price (USD)')
        self.ax.set_xlabel('Date')
        self.ax.set_title(label=f'{stock.upper()} Daily Prices', pad=5)
        self.canvas.draw()
    

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        ttk.Button(self, text='New Page', command=self.newpage).pack()

    def newpage(self):
        page = tk.Tk()
        ttk.Button(page, text='new button').pack()
        page.mainloop()

        
app = SeaofBTCapp()
app.geometry('1280x720')
app.mainloop()