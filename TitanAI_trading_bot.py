
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("TitanAI_BotLogger")

class TitanAI_Bot:
    def __init__(self, balance, fee=0.001, risk_management=0.1):
        self.balance = balance
        self.holdings = {}
        self.fee = fee
        self.risk_management = risk_management

    def calculate_fee(self, amount):
        return amount * self.fee

    def log_trade(self, action, asset, amount, price, fee, profit=None):
        message = f"{action} {amount} {asset} at {price}. Fee: {fee:.2f}"
        if profit is not None:
            message += f". Profit: {profit:.2f}"
        logger.info(message)
        return message

    def buy_asset(self, asset, price, amount_to_invest):
        amount_to_buy = amount_to_invest / price
        fee = self.calculate_fee(amount_to_invest)
        self.balance -= (amount_to_invest + fee)
        self.holdings[asset] = self.holdings.get(asset, 0) + amount_to_buy
        return self.log_trade("Buy", asset, amount_to_buy, price, fee)

    def sell_asset(self, asset, price):
        amount_to_sell = self.holdings.get(asset, 0)
        if amount_to_sell == 0:
            return None
        sell_value = amount_to_sell * price
        fee = self.calculate_fee(sell_value)
        self.balance += (sell_value - fee)
        self.holdings[asset] = 0
        return self.log_trade("Sell", asset, amount_to_sell, price, fee)

    def scalping_strategy(self, asset, price, volatility):
        if asset not in self.holdings:
            self.holdings[asset] = 0

        price_change = price * volatility * random.uniform(-1, 1)
        target_price = price + price_change

        if target_price > price and self.holdings[asset] > 0:
            return self.sell_asset(asset, price)
        elif target_price < price:
            amount_to_invest = self.balance * self.risk_management
            if amount_to_invest > 0:
                return self.buy_asset(asset, price, amount_to_invest)
        return "No action taken"

    def arbitrage_strategy(self, asset, price_binance, price_other_exchange):
        if abs(price_other_exchange - price_binance) / price_binance > 0.01:
            if price_binance < price_other_exchange:
                buy_message = self.buy_asset(asset, price_binance, self.balance * self.risk_management)
                profit = (self.holdings[asset] * price_other_exchange) - (self.holdings[asset] * price_binance)
                fee_sell = self.calculate_fee(profit)
                self.balance += profit - fee_sell
                return buy_message + "\n" + self.log_trade("Arbitrage Sell", asset, self.holdings[asset], price_other_exchange, fee_sell, profit)

    def show_trade_log(self):
        return logger.handlers[0].baseFilename

# Interfaz gráfica con Tkinter y ttk

def execute_scalping():
    try:
        price = float(price_input.get())
        volatility = float(volatility_input.get())
        message = bot.scalping_strategy("BTC", price, volatility)
        update_history(message)
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores válidos para el precio y la volatilidad")

def execute_arbitrage():
    try:
        price_binance = float(price_binance_input.get())
        price_other = float(price_other_exchange_input.get())
        message = bot.arbitrage_strategy("BTC", price_binance, price_other)
        update_history(message)
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores válidos para los precios de arbitraje")

def update_history(message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + "\n")
    chat_history.config(state=tk.DISABLED)

def show_balance():
    balance_label.config(text=f"Balance: {bot.balance:.2f} USD")

# Configuración de la interfaz
root = tk.Tk()
root.title("✨ TITAN AI TRADING BOT 🤖💰 ✨")
root.geometry("500x600")

# Crear instancia del bot
bot = TitanAI_Bot(balance=1000)

# Configuración de estilo
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12))

# Encabezado y branding
header = ttk.Label(root, text="✨ TITAN AI TRADING BOT 🤖💰 ✨", font=("Helvetica", 18, "bold"))
header.pack(pady=10)

subheader = ttk.Label(root, text="El poder de la inteligencia artificial aplicado al trading.\n〽️ Análisis. 📈 Predicción. 💡 Decisiones Automatizadas.", font=("Helvetica", 10))
subheader.pack(pady=5)

branding = ttk.Label(root, text="Powered by Melano Inc®", font=("Helvetica", 10, "italic"))
branding.pack(pady=5)

# Frame para Scalping
scalping_frame = ttk.Frame(root, padding=(20, 10))
scalping_frame.pack(fill="x")

ttk.Label(scalping_frame, text="Precio de BTC para Scalping:").pack(anchor="w")
price_input = ttk.Entry(scalping_frame)
price_input.pack(fill="x")

ttk.Label(scalping_frame, text="Volatilidad para Scalping:").pack(anchor="w")
volatility_input = ttk.Entry(scalping_frame)
volatility_input.pack(fill="x")

scalping_button = ttk.Button(scalping_frame, text="Ejecutar Scalping", command=execute_scalping)
scalping_button.pack(pady=10)

# Frame para Arbitraje
arbitrage_frame = ttk.Frame(root, padding=(20, 10))
arbitrage_frame.pack(fill="x")

ttk.Label(arbitrage_frame, text="Precio BTC en Binance:").pack(anchor="w")
price_binance_input = ttk.Entry(arbitrage_frame)
price_binance_input.pack(fill="x")

ttk.Label(arbitrage_frame, text="Precio BTC en Otro Exchange:").pack(anchor="w")
price_other_exchange_input = ttk.Entry(arbitrage_frame)
price_other_exchange_input.pack(fill="x")

arbitrage_button = ttk.Button(arbitrage_frame, text="Ejecutar Arbitraje", command=execute_arbitrage)
arbitrage_button.pack(pady=10)

# Frame para Balance y Historial
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
