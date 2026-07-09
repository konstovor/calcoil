import sqlite3
import logging

log = logging.getLogger(__name__)
DB_FILE = "history_of_drives.db"
class DatabaseManager:
    def __init__(self):
        self.conn = None
        log.info("Инициализация Database")

    def init_db(self):
        try:
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
            log.info(f"База данных инициализирована, файл: {DB_FILE}")
        except sqlite3.Error as e:
            log.error(f"Ошибка при инициализации БД: {e}")

    def get_all(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, distance, liters, price, consumption, cost, image_path FROM items ORDER BY id")
            records = cursor.fetchall()
            log.info(f"Получено {len(records)} записей из БД")
            return records
        except sqlite3.Error as e:
            log.error(f"Ошибка при получении данных: {e}")
            return []
        
    def insert_record(self, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO items (distance, liters, price, consumption, cost, image_path) VALUES (?, ?, ?, ?, ?, ?)",(data["distance"], data["liters"], data["price"], data["consumption"], data["cost"], data.get("image_path", ""))
            )
            self.conn.commit()
            log.info(f"Добавлена запись: distance={data['distance']}, liters={data['liters']}, price={data['price']}, consumption={data['consumption']}, cost={data['cost']}, image path={data.get("image_path", "")}")
        except sqlite3.Error as e:
            log.error(f"Ошибка при добавлении записи: {e}")

    def update_record(self, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE items SET distance=?, liters=?, price=?, consumption=?, cost=?, image_path=? WHERE id=?", (data["distance"], data["liters"], data["price"], data["consumption"], data["cost"], data.get("image_path", ""), data["id"])
            )
            self.conn.commit()
            log.info(f"Обновлена запись id={data['id']}: distance={data['distance']}, liters={data['liters']}, price={data['price']}, consumption={data['consumption']}, cost={data['cost']}, image path={data['image_path']}")
        except sqlite3.Error as e:
            log.error(f"Ошибка при обновлении записи id={data.get('id', 'unknown')}: {e}")

    def delete_record(self, item_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
            self.conn.commit()
            log.info(f"Удалена запись id={item_id}")
        except sqlite3.Error as e:
            log.error(f"Ошибка при удалении записи id={item_id}: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            log.info("Соединение с БД закрыто")