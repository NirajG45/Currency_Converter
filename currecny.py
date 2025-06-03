import requests
import tkinter as tk
from tkinter import ttk, messagebox

# Function to get the list of supported currencies
def get_currencies():
    url = "https://api.exchangerate.host/symbols"
    try:
        response = requests.get(url)
        data = response.json()
        return sorted(data["symbols"].keys())
    except Exception as e:
        messagebox.showerror("Error", "Failed to fetch currency list.")
        return []

# Function to convert currency
def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_curr = from_currency.get()
        to_curr = to_currency.get()
        url = f"https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}"
        response = requests.get(url)
        data = response.json()
        result = data["result"]
        result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")
    except Exception as e:
        messagebox.showerror("Error", "Conversion failed. Check your internet connection or API.")

# GUI Setup
root = tk.Tk()
root.title("💱 Currency Converter")
root.geometry("400x300")
root.config(padx=20, pady=20)

# Fetch currency list
currencies = get_currencies()

# Title
tk.Label(root, text="🌐 Currency Converter", font=("Arial", 16, "bold")).pack(pady=10)

# Amount
tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# From Currency
tk.Label(root, text="From Currency:").pack()
from_currency = ttk.Combobox(root, values=currencies, state="readonly")
from_currency.pack()
from_currency.set("USD")  # Default selection

# To Currency
tk.Label(root, text="To Currency:").pack()
to_currency = ttk.Combobox(root, values=currencies, state="readonly")
to_currency.pack()
to_currency.set("INR")  # Default selection

# Convert Button
tk.Button(root, text="Convert", command=convert_currency).pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

root.mainloop()
