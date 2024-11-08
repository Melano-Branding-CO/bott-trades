
import random
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog

class BaseStrategy:
    """Base class for trading strategies with a method to calculate fees."""
    def __init__(self, fee):
        self.fee = fee  # Default operation fee percentage (0.1%)
    
    def calculate_fee(self, amount):
        """Calculate the fee based on the amount."""
        return amount * self.fee


class ScalpingStrategy(BaseStrategy):
    """Scalping trading strategy."""
    def execute(self, bot, asset, price, volatility):
        price_change = price * volatility * random.uniform(-1, 1)
        target_price = price + price_change

        if asset not in bot.holdings:
            bot.holdings[asset] = 0

        if target_price > price and bot.holdings[asset] > 0:
            amount_to_sell = bot.holdings[asset]
            sell_value = amount_to_sell * price
            fee = self.calculate_fee(sell_value)
            bot.balance += sell_value - fee
            bot.holdings[asset] = 0
            bot.trade_log.append(f"Sell {amount_to_sell} {asset} at {price}. Balance: {bot.balance}. Fee: {fee}")

        elif target_price < price:
            amount_to_invest = bot.balance * bot.risk_management
            if amount_to_invest > 0:
                amount_to_buy = amount_to_invest / price
                buy_value = amount_to_invest
                fee = self.calculate_fee(buy_value)
                bot.holdings[asset] += amount_to_buy
                bot.balance -= (buy_value + fee)
                bot.trade_log.append(f"Buy {amount_to_buy} {asset} at {price}. Balance: {bot.balance}. Fee: {fee}")


class ArbitrageStrategy(BaseStrategy):
    """Arbitrage trading strategy."""
    def execute(self, bot, asset, price_binance, price_other_exchange):
        price_diff = price_other_exchange - price_binance

        if asset not in bot.holdings:
            bot.holdings[asset] = 0

        if abs(price_diff) / price_binance > 0.01 and price_binance < price_other_exchange:
            amount_to_buy = bot.balance * bot.risk_management / price_binance
            buy_value = amount_to_buy * price_binance
            fee = self.calculate_fee(buy_value)
            bot.holdings[asset] += amount_to_buy
            bot.balance -= (buy_value + fee)

            profit = amount_to_buy * price_other_exchange - buy_value
            fee_sell = self.calculate_fee(profit)
            bot.balance += profit - fee_sell
            bot.trade_log.append(f"Arbitrage Buy {amount_to_buy} {asset} at {price_binance}, Sell at {price_other_exchange}. Profit: {profit}. Fee: {fee_sell}")


class TitanBot:
    """Main bot class managing balance, risk, and trade logs."""
    def __init__(self, balance, fee=0.001, risk_management=0.1):
        self.balance = balance
        self.holdings = {}
        self.risk_management = risk_management
        self.trade_log = []
        self.strategies = {
            'scalping': ScalpingStrategy(fee),
            'arbitrage': ArbitrageStrategy(fee)
        }
    
    def execute_strategy(self, strategy_name, **kwargs):
        """Execute the specified strategy."""
        strategy = self.strategies.get(strategy_name)
        if strategy:
            strategy.execute(self, **kwargs)
        else:
            raise ValueError("Strategy not found")

    def show_trade_log(self):
        """Return the trade log."""
        return self.trade_log

    def export_log(self, filename):
        """Export the trade log to a file."""
        with open(filename, "w") as f:
            for log in self.trade_log:
                f.write(log + "\n")


# GUI Interface with enhanced error handling and log export
def run_scalping():
    try:
        price = float(price_input.get())
        volatility = float(volatility_input.get())
        bot.execute_strategy('scalping', asset="BTC", price=price, volatility=volatility)
        update_history()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for price and volatility.")

def run_arbitrage():
    try:
        price_binance = float(price_binance_input.get())
        price_other = float(price_other_exchange_input.get())
        bot.execute_strategy('arbitrage', asset="BTC", price_binance=price_binance, price_other_exchange=price_other)
        update_history()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for the prices.")

def update_history():
    trade_log = bot.show_trade_log()
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    for log in trade_log:
        chat_history.insert(tk.END, log + "\n")
    chat_history.config(state=tk.DISABLED)

def export_trade_log():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        bot.export_log(filename)
        messagebox.showinfo("Export Successful", f"Trade log exported to {filename}.")

root = tk.Tk()
root.title("TitanBot Trading App")
root.geometry("500x600")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12))

bot = TitanBot(balance=1000)

header = ttk.Label(root, text="TitanBot", font=("Helvetica", 24, "bold"))
header.pack(pady=20)

scalping_frame = ttk.Frame(root, padding=(20, 10))
scalping_frame.pack(fill="x")

ttk.Label(scalping_frame, text="Precio de BTC para Scalping:").pack(anchor="w")
price_input = ttk.Entry(scalping_frame)
price_input.pack(fill="x")

ttk.Label(scalping_frame, text="Volatilidad para Scalping:").pack(anchor="w")
volatility_input = ttk.Entry(scalping_frame)
volatility_input.pack(fill="x")

scalping_button = ttk.Button(scalping_frame, text="Ejecutar Scalping", command=run_scalping)
scalping_button.pack(pady=10)

arbitrage_frame = ttk.Frame(root, padding=(20, 10))
arbitrage_frame.pack(fill="x")

ttk.Label(arbitrage_frame, text="Precio BTC en Binance:").pack(anchor="w")
price_binance_input = ttk.Entry(arbitrage_frame)
price_binance_input.pack(fill="x")

ttk.Label(arbitrage_frame, text="Precio BTC en Otro Exchange:").pack(anchor="w")
price_other_exchange_input = ttk.Entry(arbitrage_frame)
price_other_exchange_input.pack(fill="x")

arbitrage_button = ttk.Button(arbitrage_frame, text="Ejecutar Arbitraje", command=run_arbitrage)
arbitrage_button.pack(pady=10)

balance_frame = ttk.Frame(root, padding=(20, 10))
balance_frame.pack(fill="x")

balance_label = ttk.Label(balance_frame, text=f"Balance: {bot.balance:.2f} USD")
balance_label.pack(anchor="w")

export_button = ttk.Button(balance_frame, text="Exportar Historial", command=export_trade_log)
export_button.pack(pady=10)

chat_history = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
chat_history.pack(pady=10)

root.mainloop()
