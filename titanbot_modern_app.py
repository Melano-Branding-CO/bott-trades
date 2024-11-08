
import random
import tkinter as tk
from tkinter import scrolledtext, ttk

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

    def stop_loss_take_profit(self, asset, current_price, stop_loss_price, take_profit_price):
        if asset not in self.holdings or self.holdings[asset] == 0:
            return

        if current_price <= stop_loss_price:
            amount_to_sell = self.holdings[asset]
            sell_value = amount_to_sell * current_price
            fee = self.calculate_fee(sell_value)
            self.balance += sell_value - fee
            self.holdings[asset] = 0
            self.trade_log.append(f"Stop-Loss triggered. Sold {amount_to_sell} {asset} at {current_price}. Balance: {self.balance}. Fee: {fee}")
        elif current_price >= take_profit_price:
            amount_to_sell = self.holdings[asset]
            sell_value = amount_to_sell * current_price
            fee = self.calculate_fee(sell_value)
            self.balance += sell_value - fee
            self.holdings[asset] = 0
            self.trade_log.append(f"Take-Profit triggered. Sold {amount_to_sell} {asset} at {current_price}. Balance: {self.balance}. Fee: {fee}")

    def show_trade_log(self):
        return self.trade_log

# Interfaz gráfica con Tkinter y ttk

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

def apply_stop_loss_take_profit():
    current_price = float(current_price_input.get())
    stop_loss = float(stop_loss_input.get())
    take_profit = float(take_profit_input.get())
    bot.stop_loss_take_profit("BTC", current_price, stop_loss, take_profit)
    update_history()

def update_history():
    trade_log = bot.show_trade_log()
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    for log in trade_log:
        chat_history.insert(tk.END, log + "\n")
    chat_history.config(state=tk.DISABLED)

def show_balance():
    balance_label.config(text=f"Balance: {bot.balance:.2f} USD")

root = tk.Tk()
root.title("TitanBot Trading App")
root.geometry("500x600")

# Configuración de estilo
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12))

# Crear instancia del bot
bot = TitanBot(balance=1000)

# Título del bot
header = ttk.Label(root, text="TitanBot", font=("Helvetica", 24, "bold"))
header.pack(pady=20)

# Frame para operaciones de Scalping
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

# Frame para operaciones de Arbitraje
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

# Frame para Stop-Loss y Take-Profit
risk_frame = ttk.Frame(root, padding=(20, 10))
risk_frame.pack(fill="x")

ttk.Label(risk_frame, text="Precio Actual de BTC:").pack(anchor="w")
current_price_input = ttk.Entry(risk_frame)
current_price_input.pack(fill="x")

ttk.Label(risk_frame, text="Stop-Loss:").pack(anchor="w")
stop_loss_input = ttk.Entry(risk_frame)
stop_loss_input.pack(fill="x")

ttk.Label(risk_frame, text="Take-Profit:").pack(anchor="w")
take_profit_input = ttk.Entry(risk_frame)
take_profit_input.pack(fill="x")

stop_loss_button = ttk.Button(risk_frame, text="Aplicar Stop-Loss / Take-Profit", command=apply_stop_loss_take_profit)
stop_loss_button.pack(pady=10)

# Frame para balance y historial de operaciones
balance_frame = ttk.Frame(root, padding=(20, 10))
balance_frame.pack(fill="x")

balance_label = ttk.Label(balance_frame, text=f"Balance: {bot.balance:.2f} USD")
balance_label.pack(anchor="w")

show_balance_button = ttk.Button(balance_frame, text="Mostrar Balance", command=show_balance)
show_balance_button.pack(pady=10)

# Historial de operaciones (ScrollText)
chat_history = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
chat_history.pack(pady=10)

root.mainloop()
