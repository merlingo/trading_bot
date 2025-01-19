from Decider.rsi_rule import Rsi_Rule
from Position import PositionList
from gui import TradingBotGUI
from utils.env_vars import read_env_file
from utils.loader import Market
from loguru import logger
import tkinter as tk
from tkinter import ttk
import threading
import time

def main():
    #read config file
    env_file_path = '.env_variable_file'
    env_vars = read_env_file(env_file_path)

    print(env_vars)
    #initialize Market Decider PositionList Logger  and Gui
    exchange_id = 'binance'
    symbol = env_vars['SPOT_ASSET']+"/USDT"
    market = Market(exchange_id, env_vars['APIKEY'], env_vars['SECRET_KEY'], symbol)
    plist = PositionList(market.exchange,env_vars['LIMIT'], env_vars['POZISYON_ACMA_ARALIGI'], env_vars['POZISYON_KAPAMA_ARALIGI'])
    logger.add(env_vars['PWD']+"/logs/logs", rotation="12:00")  # New file is created each day at noon
    logger.info("Trading bot başlıyor")

    decider = Rsi_Rule(min,max)

    root = tk.Tk()
    app = TradingBotGUI(root, market, plist, decider, [env_vars['SPOT_ASSET'],"USDT"],env_vars['AMOUNT'])
    root.mainloop()

if __name__ == "__main__":
    main()