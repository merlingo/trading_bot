import tkinter as tk
from tkinter import ttk
import threading
import time
from tkinter import messagebox

class TradingBotGUI:
    def __init__(self, root, market, plist, decider, assets):
        self.root = root
        self.root.title("Trading Bot")
        self.running = False

        # Market and PositionList objects initialized in main function
        self.market = market
        self.plist = plist
        self.decider = decider
        self.assets = assets
        self.amount = 0
        self.toplam_kar = 0
        
        # Create and place the RSI Min input
        tk.Label(root, text="RSI Min:").grid(row=0, column=0, padx=10, pady=10)
        self.rsi_min_entry = tk.Entry(root)
        self.rsi_min_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create and place the RSI Max input
        tk.Label(root, text="RSI Max:").grid(row=1, column=0, padx=10, pady=10)
        self.rsi_max_entry = tk.Entry(root)
        self.rsi_max_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create and place the İşlem Miktarı input
        tk.Label(root, text="İşlem Miktarı:").grid(row=2, column=0, padx=10, pady=10)
        self.islem_miktari_entry = tk.Entry(root)
        self.islem_miktari_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create and place the İşlem Türü dropdown
        tk.Label(root, text="İşlem Türü:").grid(row=3, column=0, padx=10, pady=10)
        self.islem_turu_var = tk.StringVar()
        self.islem_turu_dropdown = ttk.Combobox(root, textvariable=self.islem_turu_var)
        self.islem_turu_dropdown['values'] = ("kaldıraç", "normal")
        self.islem_turu_dropdown.grid(row=3, column=1, padx=10, pady=10)

        self.usdt_miktari_label = tk.Label(root, text="USDT Miktarı: "+self.market.get_USDT())
        self.usdt_miktari_label.grid(row=4, column=0, padx=10, pady=10)

        # Create and place the BTC Miktarı label
        self.btc_miktari_label = tk.Label(root, text="BTC Miktarı:"+ self.market.get_BTC())
        self.btc_miktari_label.grid(row=4, column=1, padx=10, pady=10)
        # Create and place the Taken Decision label
        self.last10_rsi_label = tk.Label(root, text="Last 10 RSI:")
        self.last10_rsi_label.grid(row=5, column=0, padx=10, pady=5)
        self.rsi_listbox = tk.Listbox(root, height=10, width=10)
        self.rsi_listbox.grid(row=6, column=0, padx=10, pady=20)
        
        # Create and place the Taken Decision label
        self.last_price_label = tk.Label(root, text="Last 10 Prices:")
        self.last_price_label.grid(row=5, column=1, padx=10, pady=5)
        self.price_listbox = tk.Listbox(root, height=10, width=65)
        self.price_listbox.grid(row=6, column=1, padx=10, pady=20)
        # Create and place the USDT Miktarı label


        # Create and place the Alinan Pozisyonlar table
        tk.Label(root, text="Alınan Pozisyonlar:").grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        self.positions_table = ttk.Treeview(root, columns=("Position", "Amount(BTC)", "USDT", "Price"), show='headings')
        self.positions_table.heading("Position", text="Position")
        self.positions_table.heading("Amount(BTC)", text="Amount")
        self.positions_table.heading("USDT", text="USDT")
        self.positions_table.heading("Price", text="Price")
        self.positions_table.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # init position list
        for position in self.plist.list:
            
            self.pozisyonAc(position.state, position.miktar, position.price)

        # Create and place the Start button
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.grid(row=9, column=0, padx=10, pady=10)

        # Create and place the Stop button
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.grid(row=9, column=1, padx=10, pady=10)

        # Create and place the notification label with a red dot
        self.notification_label = tk.Label(root, text="Stopped")
        self.notification_label.grid(row=10, column=0, padx=10, pady=10)
        self.notification_dot = tk.Canvas(root, width=20, height=20)
        self.red_dot = self.notification_dot.create_oval(5, 5, 15, 15, fill="red")
        self.notification_dot.grid(row=10, column=1, padx=10, pady=10)
        
        # Last price values
        self.refresh_rsi_values()
        self.refresh_price_values()

    def refresh_rsi_values(self):
        self.rsi_listbox.delete(0, tk.END)
        rsi_values = self.market.get_rsi_values()
        #print(rsi_values)
        i=1
        for rsi in rsi_values:
            self.rsi_listbox.insert(tk.END, str(i)+") "+str(round(float(rsi), 3)))
            i=i+1

    def refresh_price_values(self):
        self.price_listbox.delete(0, tk.END)
        price_values = self.market.get_last10_prices()
        #print(price_values)
        #i=1
        for value in price_values:
            self.price_listbox.insert(tk.END, f"Time: {value[0]}, Open: {value[1]}, High: {value[2]}, Low: {value[3]}, Close: {value[4]}")
            #i=i+1

    def start(self):
        rsi_min = self.rsi_min_entry.get()
        rsi_max = self.rsi_max_entry.get()
        self.amount = self.islem_miktari_entry.get()
        islem_turu = self.islem_turu_var.get()
        if(rsi_min == "" or rsi_max == "" or self.amount == "" or islem_turu == ""):
            print("Please fill all the fields.")
            messagebox.showinfo("Alert", "Please fill all the fields !!!")
            return
        # For demonstration purposes, just print the values
        print("Trading started with the following parameters:")
        print("RSI Min:", rsi_min)
        print("RSI Max:", rsi_max)
        print("İşlem Miktarı:", self.amount)
        print("İşlem Türü:", islem_turu)
        
        # Market settings
        self.decider.set_min(rsi_min)
        self.decider.set_max(rsi_max)

        # Update labels and notification
        #self.toplam_kar_label.config(text="Toplam Kar: 0")
        #self.last_price.config(text="Last Price: "+str(self.market.get_price()))
        #self.usdt_miktari_label.config(text="USDT Miktarı: 1000")
        #self.btc_miktari_label.config(text="BTC Miktarı: 0.05")
        self.notification_label.config(text="Running")
        self.notification_dot.itemconfig(self.red_dot, fill="green")

        # Start the infinite loop for collecting data
        self.running = True
        self.collect_data_thread = threading.Thread(target=self.collect_data)
        self.collect_data_thread.start()

    def stop(self):
        # Stop the infinite loop
        self.running = False
        self.collect_data_thread.join(timeout=1)

        # For demonstration purposes, just print a message
        print("Trading stopped.")
        
        # Update labels and notification
        #self.toplam_kar_label.config(text="Toplam Kar: --")
        #self.taken_decision_label.config(text="Taken Decision: --")
        self.usdt_miktari_label.config(text="USDT Miktarı: --")
        self.btc_miktari_label.config(text="BTC Miktarı: --")
        self.notification_label.config(text="Stopped")
        self.notification_dot.itemconfig(self.red_dot, fill="red")

    def collect_data(self):
        while self.running:
            # Simulate data collection from exchange market
            print("Collecting data from exchange market...")
            self.market.load_data()
            stock = self.market.get_stock_data()
            #print(type(stock))
            #print(stock.columns.tolist())

            self.plist.ex = self.market.exchange
            
            # Get the latest RSI_14 value
            #last_rsi_14 = stock['rsi_14'].iloc[-1]
            #print("Last RSI_14 value:", last_rsi_14)
            #self.last_price_label.config(text="Last RSI(50): "+str(self.market.get_rsi(50)))
            decision = self.decider.decide(self.market.get_rsi(50))

            # Get the latest RSI value
            #last_rsi = stock['stochrsi'].iloc[-1]
            #print("Last RSI value:", last_rsi)
            #self.last10_rsi_label.config(text="Last RSI(100): "+str(self.market.get_rsi(100)))
            try:
                price = self.market.get_price()
                kar = self.plist.evaluate(self.amount,price, decision)
                self.toplam_kar += kar

                #self.toplam_kar_label.config(text="Toplam Kar: " + str(self.toplam_kar))
                #self.last_price.config(text="Last Price: "+str(price))
                print("Total profit:", self.toplam_kar)
                for(position) in self.plist.list:
                    print("Position:", position.state, position.miktar, position.price)
                #print("Position list:", self.plist.list)
                self.usdt_miktari_label.config(text="USDT Miktarı: "+self.market.get_USDT())
                self.btc_miktari_label.config(text="BTC Miktarı: "+self.market.get_BTC())
                #time.sleep(1)  # Simulate delay
                self.refresh_rsi_values()
                self.refresh_price_values()
                self.delete_all_rows()
                for position in self.plist.list:
                    self.pozisyonAc(position.state, position.miktar, position.price)
            except Exception as e:
                print(e)
                print("Error in collect_data")
                pass

    def pozisyonAc(self, position, amount, price):
        self.positions_table.insert("", "end", values=(position, amount, amount*price, price))

    def pozisyonKapa(self):
        selected_item = self.positions_table.selection()
        if selected_item:
            self.positions_table.delete(selected_item)

    def delete_all_rows(self):
        for row in self.positions_table.get_children():
            self.positions_table.delete(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
    