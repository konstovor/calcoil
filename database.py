import sqlite3
import os
DB_FILE = "history_of_drives.db"
class DatabaseManager:
    def __init__(self):
        self.conn = None
    def init_db(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                distance REAL NOT NULL,
                liters REAL NOT NULL,
                price REAL,
                consumption REAL,
                cost REAL,
                image_path TEXT
            )
        """)
        self.conn.commit()
    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, distance, liters, price, consumption, cost, image_path FROM items ORDER BY id")
        return cursor.fetchall()
    def insert_record(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO items (distance, liters, price, consumption, cost, image_path) VALUES (?, ?, ?, ?, ?, ?)",(data["distance"], data["liters"], data["price"], data["consumption"], data["cost"], data.get("image_path", ""))
        )
        self.conn.commit()
    def update_record(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE items SET distance=?, liters=?, price=?, consumption=?, cost=?, image_path=? WHERE id=?", (data["distance"], data["liters"], data["price"], data["consumption"], data["cost"], data.get("image_path", ""), data["id"])
        )
        self.conn.commit()
    def delete_record(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
        self.conn.commit()