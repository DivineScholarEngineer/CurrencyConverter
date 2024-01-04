import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConverter:
    def __init__(self, api_key):
        self.api_url = "http://api.exchangeratesapi.io/v1/latest?access_key="
        self.api_key = api_key

    def get_exchange_rate(self):
        try:
            url = f"{self.api_url}{self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'rates' in data:
                return data['rates']
            else:
                print("Error: 'rates' not found in response.")
                return {}

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {}

    def convert(self, from_currency, to_currency, amount):
        rates = self.get_exchange_rate()
        if from_currency == 'EUR':
            return round(amount * rates[to_currency], 2)
        elif to_currency == 'EUR':
            return round(amount / rates[from_currency], 2)
        else:
            return round(amount / rates[from_currency] * rates[to_currency], 2)

class CurrencyConverterUI(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.currency_converter = converter
        self.init_ui()

    def init_ui(self):
        self.configure(bg="#eaeaea")  # Modern light grey background
        self.geometry("500x250")  # Slightly larger window

        # Styling
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground="white", background="white")
        style.configure('TButton', background="#4CAF50", foreground="white", font=('Helvetica', 10, 'bold'))
        style.map('TButton', background=[('active', '!disabled', '#4CAF50'), ('pressed', '#388E3C')])

        # Variables
        self.from_currency_variable = tk.StringVar(self)
        self.to_currency_variable = tk.StringVar(self)

        # Dropdown menus
        font = ("Helvetica", 12)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.currency_converter.get_exchange_rate().keys()),
                                                   font=font, state='readonly', width=15)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.currency_converter.get_exchange_rate().keys()),
                                                 font=font, state='readonly', width=15)
        self.from_currency_dropdown.set('EUR')  # default value
        self.to_currency_dropdown.set('USD')  # default value

        # Layout
        self.from_currency_dropdown.grid(column=0, row=0, padx=10, pady=10)
        self.to_currency_dropdown.grid(column=1, row=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(self, bd=3, relief=tk.RIDGE, justify=tk.CENTER)
        self.amount_entry.grid(column=0, row=1, padx=10, pady=10)

        self.converted_amount_label = tk.Label(self, text='', fg='black', bg='white', relief=tk.RIDGE,
                                               justify=tk.CENTER, borderwidth=3)
        self.converted_amount_label.grid(column=1, row=1, padx=10, pady=10)

        self.convert_button = ttk.Button(self, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(columnspan=2, row=2, padx=10, pady=10)

    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            self.converted_amount_label.config(text="Invalid input")
            return

        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        self.converted_amount_label.config(text=str(converted_amount))

if __name__ == '__main__':
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key from https://exchangeratesapi.io/
    converter = CurrencyConverter(api_key)
    CurrencyConverterUI(converter).mainloop()

