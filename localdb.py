import sqlite3
from typing import List, Tuple, Any

class LocalDB:
    def __init__(self, db_name: str = "trading_bot.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                symbol TEXT NOT NULL,
                                quantity REAL NOT NULL,
                                price REAL NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                              )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS positions (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                marketid TEXT NOT NULL,
                                state TEXT NOT NULL,
                                price REAL NOT NULL,
                                miktar REAL NOT NULL,
                                kar REAL NOT NULL
                              )''')
        self.connection.commit()

    def insert_trade(self, symbol: str, quantity: float, price: float):
        self.cursor.execute('''INSERT INTO trades (symbol, quantity, price)
                               VALUES (?, ?, ?)''', (symbol, quantity, price))
        self.connection.commit()

    def get_trades(self) -> List[Tuple[int, str, float, float, str]]:
        self.cursor.execute('''SELECT * FROM trades''')
        return self.cursor.fetchall()

    def insert_position(self,marketid:str, state: str, price: float, miktar: float, kar: float):
        self.cursor.execute('''INSERT INTO positions (marketid,state, price, miktar, kar)
                               VALUES (?, ?, ?, ?, ?)''', (marketid,state, price, miktar, kar))
        self.connection.commit()

    def get_positions(self) -> List[Tuple[int, str, str, float, float, float]]:
        self.cursor.execute('''SELECT * FROM positions''')
        return self.cursor.fetchall()

    def remove_position_by_id(self, position_id: str):
        self.cursor.execute('''DELETE FROM positions WHERE marketid = ?''', (position_id,))
        self.connection.commit()

    def remove_all_positions(self):
        self.cursor.execute('''DELETE FROM positions''')
        self.connection.commit()

    def close(self):
        self.connection.close()