import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import filedialog as fd

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
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime, timedelta


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)
START_DATE = datetime.now() - timedelta(100)
END_DATE = datetime.now()


lightcolor = '#00A3E0'
darkcolor = '#183A54'
alpha_key = 'EAY8N3YJIB72Q35C'

timeseries = ts(key=alpha_key, output_format='pandas')

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        try:
            tk.Tk.iconbitmap(self, default='got.ico')
        except Exception:
            pass

        tk.Tk.wm_title(self, 'Sea of FRT')

        # master frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # menubar to add more options
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command=lambda: msg.showinfo('Title', 'Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        #top frame for user input
        top_frame = tk.Frame(container)
        top_frame.pack(pady=5)

        #company name to search for
        ttk.Label(top_frame, text='Enter company name: ').grid(column=0, row=0)
        self.search = ttk.Entry(top_frame) 
        self.search.grid(column=1, row=0, padx=5)
        self.search.bind("<Return>", (lambda event: self.search_symbol(self.search.get())))

        #enter stock symbol to query pricing data
        ttk.Label(top_frame, text='Enter stock symbol: ').grid(column=2, row=0)

        self.symbol_entry = ttk.Entry(top_frame)
        self.symbol_entry.grid(column=3, row=0)

        # start date
        tk.Label(top_frame, text='Start Date: ').grid(column=4, row=0)
        self.start_date = ttk.Entry(top_frame)
        self.start_date.grid(column=5, row=0)

        # end date
        tk.Label(top_frame, text='End Date: ').grid(column=6, row=0)
        self.end_date = ttk.Entry(top_frame)
        self.end_date.grid(column=7, row=0)

        ttk.Button(top_frame, text='Export Prices', command=self.export_prices).grid(column=8, row=0, padx=5)

        # middle frame to render graph
        mid_frame = tk.Frame(container)
        mid_frame.pack(expand=True, fill='both')

        self.symbol_entry.bind("<Return>", (lambda event: self.get_stock(self.symbol_entry.get(), self.start_date.get(), self.end_date.get())))
        self.end_date.bind("<Return>", (lambda event: self.get_stock(self.symbol_entry.get(), self.start_date.get(), self.end_date.get())))
        self.start_date.bind("<Return>", (lambda event: self.get_stock(self.symbol_entry.get(), self.start_date.get(), self.end_date.get())))

        self.figure = Figure(figsize=(5,4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, mid_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # bottom frame for navigation tool bar
        bot_frame = tk.Frame(container)
        bot_frame.pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, bot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.get_crypto('btc')

    def get_crypto(self, coin):
        """get crypto currency prices"""
        self.ax.clear()

        df = cc(key=alpha_key, output_format='pandas')
        crypto = df.get_digital_currency_daily(coin, 'USD')[0].reset_index()
        crypto.sort_values(by='date', ascending=False, inplace=True)
        crypto = crypto.iloc[:100, :]
        crypto['date'] = pd.to_datetime(crypto['date'])
        crypto["MPLDates"] = crypto.loc[:, "date"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

        candle(self.ax, crypto[['MPLDates', '1a. open (USD)', '2a. high (USD)', '3a. low (USD)', '4a. close (USD)']].values, colorup=lightcolor, colordown=darkcolor)
        
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.figure.autofmt_xdate()
        self.ax.set_ylabel('Price')
        self.ax.set_xlabel('Date')
        self.ax.set_title(f'{coin.upper()} Daily Prices')
        self.canvas.draw()

    def get_stock(self, stock, start_date, end_date):
        """get common stock prices"""
        self.ax.clear()

        try:
            stock_data = timeseries.get_daily(symbol=stock, outputsize='full')[0].reset_index()
        except Exception as e:
            msg.showerror('Error retrieving prices', str(e))
        else:            
            stock_data.sort_values(by='date', ascending=False, inplace=True)
            stock_data['date'] = pd.to_datetime(stock_data['date'])

            if start_date != '' and end_date != '':
                try:
                    stock_data = stock_data[(stock_data['date'] > start_date) & (stock_data['date'] < end_date)]
                except TypeError:
                    msg.showerror('Date input error', 'Date format should be YYYYMMDD or YYYY-MM-DD')
            else: # default to last 100 days prices if user doesn't put start_date and end_date
                stock_data = stock_data[(stock_data['date'] > START_DATE) & (stock_data['date'] < END_DATE)]

            try:
                stock_data["MPLDates"] = stock_data.loc[:, "date"].apply(lambda date: mdates.date2num(date.to_pydatetime()))
            except KeyError:
                msg.showerror('Date input error', 'Date format should be YYYYMMDD or YYYY-MM-DD')
                
            candle(self.ax, stock_data[['MPLDates', '1. open', '2. high', '3. low', '4. close']].values, colorup=lightcolor, colordown=darkcolor)
            
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            self.ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
            self.figure.autofmt_xdate()
            self.ax.set_ylabel('Price')
            self.ax.set_xlabel('Date')
            self.ax.set_title(label=f'{stock.upper()} Daily Prices', pad=5)
            self.canvas.draw()
    
    def search_symbol(self, name):
        """search symbol based on a given name"""
        
        try:
            df = timeseries.get_symbol_search(name)[0]
        except IndexError:
            msg.showerror('Error searching name', 'Could not find any results')
        except Exception as e:
            msg.showerror('Error searching name', str(e))
        else:
            master = tk.Tk()
            master.wm_title('Search Results')

            df = df[['1. symbol', '2. name', '3. type', '4. region', '8. currency']].rename(columns={'1. symbol':'Symbol', '2. name':'Name', '3. type':'Type', '4. region':'Region', '8. currency':'Currency'})
            df.index.rename('', inplace=True)
            search_results = tk.Text(master)
            search_results.insert(tk.END, df)
            search_results.pack(expand=True, fill='both')

            master.mainloop()

    def export_prices(self):
        """export prices to a given file name"""

        filename = fd.asksaveasfilename(initialdir = "/", title = "Select file", defaultextension='.csv',
                                        filetypes = (('Comma Separated Values', '*.csv'), ("All files","*.*")))
        try:
            data = timeseries.get_daily_adjusted(symbol=self.symbol_entry.get(), outputsize='full')[0].reset_index()
            data.to_csv(filename, index=False)
        except Exception as e:
            msg.showerror('Error saving file', str(e))

if __name__ == "__main__":
    app = SeaofBTCapp()
    app.geometry('1280x720')
    app.mainloop()