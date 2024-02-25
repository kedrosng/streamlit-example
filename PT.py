import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

class PairTradingApp(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pair Trading Strategy")
        self.create_widgets()

    def create_widgets(self):
        # Create label and entry for stock symbols
        self.label_stock1 = tk.Label(self, text="Enter the ticker symbol for Stock1:")
        self.label_stock1.grid(row=0, column=0)
        self.entry_stock1 = tk.Entry(self)
        self.entry_stock1.grid(row=0, column=1)

        self.label_stock2 = tk.Label(self, text="Enter the ticker symbol for Stock2:")
        self.label_stock2.grid(row=1, column=0)
        self.entry_stock2 = tk.Entry(self)
        self.entry_stock2.grid(row=1, column=1)

        # Create button to initiate pair trading strategy
        self.button_run_strategy = tk.Button(self, text="Run Pair Trading Strategy", command=self.run_strategy)
        self.button_run_strategy.grid(row=2, columnspan=2)

    def run_strategy(self):
        try:
            # Get the stock symbols from the entry fields
            stock1_symbol = self.entry_stock1.get()
            stock2_symbol = self.entry_stock2.get()
            tickers = [stock1_symbol, stock2_symbol]
            
            # Get today's date and calculate the start date as 6 months before today
            today = datetime.date.today()
            six_months_ago = today - datetime.timedelta(days=6*30)
            start_date = six_months_ago.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')

            # Download historical data
            df = yf.download(tickers, start=start_date, end=end_date)['Close']

            # Calculate the z-score of the spread
            window_length = 20
            df['Spread'] = df[stock1_symbol] - df[stock2_symbol]
            df['Mean'] = df['Spread'].rolling(window=window_length).mean()
            df['Std'] = df['Spread'].rolling(window=window_length).std()
            df['Z_Score'] = (df['Spread'] - df['Mean']) / df['Std']

            # Define the pair trading strategy
            entry_threshold = 1
            exit_threshold = 0.5
            transaction_cost = 0.0005
            in_position = False
            entry_price = 0
            exits = []
            entries = []
            pnl = []
            spread_values = df['Spread'].values
            z_scores = df['Z_Score'].values

            for i in range(1, len(df)):
                # Entry logic
                if not in_position and abs(z_scores[i]) > entry_threshold:
                    in_position = True
                    entry_price = spread_values[i]
                    entries.append((df.index[i], entry_price))

                # Exit logic
                elif in_position and abs(z_scores[i]) < exit_threshold:
                    in_position = False
                    exit_price = spread_values[i]
                    exits.append((df.index[i], exit_price))
                    trade_pnl = exit_price - entry_price - transaction_cost
                    pnl.append(trade_pnl)

            # Plot results
            plt.figure(figsize=(14, 7))
            ax1 = df[stock1_symbol].plot(color='blue', label=stock1_symbol)
            ax2 = df[stock2_symbol].plot(color='red', label=stock2_symbol, secondary_y=True)
            handles, labels = [], []
            handles.extend([plt.Line2D([0], [0], color='green', marker='^', markersize=10, linestyle='None')])
            labels.extend(['Buy/Sell'])
            for entry in entries:
                plt.scatter(entry[0], entry[1], marker='^', color='green')
            for exit in exits:
                plt.scatter(exit[0], exit[1], marker='v', color='red')
            handles.extend([plt.Line2D([0], [0], color='blue'), plt.Line2D([0], [0], color='red')])
            labels.extend([stock1_symbol, stock2_symbol])
            plt.legend(handles, labels)
            plt.title('Stock Prices with Trade Entry/Exit Points')
            plt.show()

            # Calculate and print performance metrics
            cumulative_returns = np.cumsum(pnl)
            returns = np.diff(np.insert(cumulative_returns, 0, 0))
            sharpe_ratio = np.mean(returns) / np.std(returns)
            max_drawdown = np.max(np.maximum.accumulate(cumulative_returns) - cumulative_returns)
            total_return = cumulative_returns[-1]
            messagebox.showinfo("Performance Metrics", f"Sharpe Ratio: {sharpe_ratio:.2f}\nMax Drawdown: {max_drawdown:.2f}\nTotal Return: {total_return:.2f}\nBest Entry Threshold: {entry_threshold}\nBest Exit Threshold: {exit_threshold}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PairTradingApp()
    app.mainloop()