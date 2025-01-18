import tkinter as tk
from tkinter import ttk



def submit():
    rsi_min = rsi_min_entry.get()
    rsi_max = rsi_max_entry.get()
    islem_miktari = islem_miktari_entry.get()
    islem_turu = islem_turu_var.get()
    
    # For demonstration purposes, just print the values
    print("RSI Min:", rsi_min)
    print("RSI Max:", rsi_max)
    print("İşlem Miktarı:", islem_miktari)
    print("İşlem Türü:", islem_turu)
    
    # Update labels (dummy values for now)
    toplam_kar_label.config(text="Toplam Kar: 0")
    taken_decision_label.config(text="Taken Decision: None")
    usdt_miktari_label.config(text="USDT Miktarı: 1000")
    btc_miktari_label.config(text="BTC Miktarı: 0.05")


# Create the main window
root = tk.Tk()
root.title("Trading Bot")

# Create and place the RSI Min input
tk.Label(root, text="RSI Min:").grid(row=0, column=0, padx=10, pady=10)
rsi_min_entry = tk.Entry(root)
rsi_min_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the RSI Max input
tk.Label(root, text="RSI Max:").grid(row=1, column=0, padx=10, pady=10)
rsi_max_entry = tk.Entry(root)
rsi_max_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the İşlem Miktarı input
tk.Label(root, text="İşlem Miktarı:").grid(row=2, column=0, padx=10, pady=10)
islem_miktari_entry = tk.Entry(root)
islem_miktari_entry.grid(row=2, column=1, padx=10, pady=10)

# Create and place the İşlem Türü dropdown
tk.Label(root, text="İşlem Türü:").grid(row=3, column=0, padx=10, pady=10)
islem_turu_var = tk.StringVar()
islem_turu_dropdown = ttk.Combobox(root, textvariable=islem_turu_var)
islem_turu_dropdown['values'] = ("kaldıraç", "normal")
islem_turu_dropdown.grid(row=3, column=1, padx=10, pady=10)

# Create and place the Toplam Kar label
toplam_kar_label = tk.Label(root, text="Toplam Kar:")
toplam_kar_label.grid(row=4, column=0, padx=10, pady=10)

# Create and place the Taken Decision label
taken_decision_label = tk.Label(root, text="Taken Decision:")
taken_decision_label.grid(row=4, column=1, padx=10, pady=10)

# Create and place the USDT Miktarı label
usdt_miktari_label = tk.Label(root, text="USDT Miktarı:")
usdt_miktari_label.grid(row=5, column=0, padx=10, pady=10)

# Create and place the BTC Miktarı label
btc_miktari_label = tk.Label(root, text="BTC Miktarı:")
btc_miktari_label.grid(row=5, column=1, padx=10, pady=10)

# Create and place the Alinan Pozisyonlar table
tk.Label(root, text="Alınan Pozisyonlar:").grid(row=6, column=0, padx=10, pady=10, columnspan=2)
positions_table = ttk.Treeview(root, columns=("Position", "Amount", "Price"), show='headings')
positions_table.heading("Position", text="Position")
positions_table.heading("Amount", text="Amount")
positions_table.heading("Price", text="Price")
positions_table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Create and place the Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()
