
import random
import tkinter as tk
from tkinter import scrolledtext

class TitanBot:
    def __init__(self, balance, fee=0.001, risk_management=0.1):
        self.balance = balance
        self.holdings = {}  # Diccionario para gestionar múltiples activos
        self.fee = fee  # Comisión por operación (0.1% por defecto)
        self.risk_management = risk_management  # Máximo porcentaje del balance a usar por operación
        self.trade_log = []  # Registro de todas las operaciones

    def calculate_fee(self, amount):
        return amount * self.fee

    def scalping_strategy(self, asset, price, volatility):
        price_change = price * volatility * random.uniform(-1, 1)
        target_price = price + price_change

        if asset not in self.holdings:
            self.holdings[asset] = 0

        if target_price > price:
            if self.holdings[asset] > 0:
                amount_to_sell = self.holdings[asset]
                sell_value = amount_to_sell * price
                fee = self.calculate_fee(sell_value)
                self.balance += sell_value - fee
                self.holdings[asset] = 0
                self.trade_log.append(f"Sell {amount_to_sell} {asset} at {price}. Balance: {self.balance}. Fee: {fee}")
        elif target_price < price:
            amount_to_invest = self.balance * self.risk_management
            if amount_to_invest > 0:
                amount_to_buy = amount_to_invest / price
                buy_value = amount_to_invest
                fee = self.calculate_fee(buy_value)
                self.holdings[asset] += amount_to_buy
                self.balance -= (buy_value + fee)
                self.trade_log.append(f"Buy {amount_to_buy} {asset} at {price}. Balance: {self.balance}. Fee: {fee}")

    def arbitrage_strategy(self, asset, price_binance, price_other_exchange):
        price_diff = price_other_exchange - price_binance

        if asset not in self.holdings:
            self.holdings[asset] = 0

        if abs(price_diff) / price_binance > 0.01:
            if price_binance < price_other_exchange:
                amount_to_buy = self.balance * self.risk_management / price_binance
                buy_value = amount_to_buy * price_binance
                fee = self.calculate_fee(buy_value)
                self.holdings[asset] += amount_to_buy
                self.balance -= (buy_value + fee)

                profit = amount_to_buy * price_other_exchange - buy_value
                fee_sell = self.calculate_fee(profit)
                self.balance += profit - fee_sell
                self.trade_log.append(f"Arbitrage Buy {amount_to_buy} {asset} at {price_binance}, Sell at {price_other_exchange}. Profit: {profit}. Fee: {fee_sell}")

    def show_trade_log(self):
        return self.trade_log

# Interfaz gráfica con Tkinter

def run_scalping():
    price = float(price_input.get())
    volatility = float(volatility_input.get())
    bot.scalping_strategy("BTC", price, volatility)
    update_history()

def run_arbitrage():
    price_binance = float(price_binance_input.get())
    price_other = float(price_other_exchange_input.get())
    bot.arbitrage_strategy("BTC", price_binance, price_other)
    update_history()

def update_history():
    trade_log = bot.show_trade_log()
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    for log in trade_log:
        chat_history.insert(tk.END, log + "\n")
    chat_history.config(state=tk.DISABLED)

root = tk.Tk()
root.title("TitanBot Trading App")

bot = TitanBot(balance=1000)

tk.Label(root, text="Precio de BTC para Scalping:").pack(pady=5)
price_input = tk.Entry(root)
price_input.pack(pady=5)

tk.Label(root, text="Volatilidad para Scalping:").pack(pady=5)
volatility_input = tk.Entry(root)
volatility_input.pack(pady=5)

scalping_button = tk.Button(root, text="Ejecutar Scalping", command=run_scalping)
scalping_button.pack(pady=10)

tk.Label(root, text="Precio BTC en Binance (Arbitraje):").pack(pady=5)
price_binance_input = tk.Entry(root)
price_binance_input.pack(pady=5)

tk.Label(root, text="Precio BTC en Otro Exchange (Arbitraje):").pack(pady=5)
price_other_exchange_input = tk.Entry(root)
price_other_exchange_input.pack(pady=5)

arbitrage_button = tk.Button(root, text="Ejecutar Arbitraje", command=run_arbitrage)
arbitrage_button.pack(pady=10)

chat_history = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
chat_history.pack(pady=10)

root.mainloop()
