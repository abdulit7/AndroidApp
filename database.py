import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("restaurant.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def create_tables(self):
        try:
            # Create menu table without stock
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL
                )
            ''')
            # Create orders table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    order_type TEXT NOT NULL,
                    order_date TEXT NOT NULL,
                    table_number TEXT,
                    customer_name TEXT,
                    customer_number TEXT,
                    address TEXT
                )
            ''')
            # Create order_items table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id)
                )
            ''')
            # Create expenses table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def initialize_menu(self, menu_items):
        try:
            self.cursor.executemany('''
                INSERT OR REPLACE INTO menu (name, price)
                VALUES (?, ?)
            ''', [(item["name"], item["price"]) for item in menu_items])
            self.conn.commit()
            print(f"Initialized menu with {len(menu_items)} items")
        except sqlite3.Error as e:
            print(f"Error initializing menu: {e}")
            raise

    def get_menu(self):
        try:
            self.cursor.execute("SELECT name, price FROM menu")
            return [{"name": row[0], "price": row[1]} for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving menu: {e}")
            return []

    def edit_product(self, old_name, new_name, price):
        try:
            self.cursor.execute('''
                UPDATE menu
                SET name = ?, price = ?
                WHERE name = ?
            ''', (new_name, price, old_name))
            self.conn.commit()
            print(f"Edited product: {old_name} -> {new_name}, Price={price}")
        except sqlite3.Error as e:
            print(f"Error editing product {old_name}: {e}")
            raise

    def delete_product(self, name):
        try:
            self.cursor.execute("DELETE FROM menu WHERE name = ?", (name,))
            self.conn.commit()
            print(f"Deleted product: {name}")
        except sqlite3.Error as e:
            print(f"Error deleting product {name}: {e}")
            raise

    def add_order(self, order_id, order_type, items, order_date, table_number=None, customer_name=None, customer_number=None, address=None):
        try:
            # Insert order metadata
            self.cursor.execute('''
                INSERT INTO orders (order_id, order_type, order_date, table_number, customer_name, customer_number, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (order_id, order_type, order_date, table_number, customer_name, customer_number, address))
            # Insert items
            for item in items:
                self.cursor.execute('''
                    INSERT INTO order_items (order_id, item_name, quantity, price, total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, item["name"], item["quantity"], item["price"], item["total"]))
            self.conn.commit()
            print(f"Saved order to database: Order ID={order_id}, Type={order_type}, Items={items}, DateTime={order_date}, Table={table_number}, Name={customer_name}, Number={customer_number}, Address={address}")
        except sqlite3.Error as e:
            print(f"Error saving order {order_id}: {e}")
            self.conn.rollback()
            raise

    def get_sales_by_date(self, date):
        try:
            self.cursor.execute('''
                SELECT o.order_date, SUM(oi.total) as total
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.order_date LIKE ?
                GROUP BY o.order_date
            ''', (f"{date}%",))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving sales by date {date}: {e}")
            return []

    def get_orders_by_date(self, date):
        try:
            self.cursor.execute('''
                SELECT o.order_id, o.order_type, o.order_date, o.table_number, o.customer_name, o.customer_number, o.address, SUM(oi.total) as total
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.order_date LIKE ?
                GROUP BY o.order_id, o.order_type, o.order_date, o.table_number, o.customer_name, o.customer_number, o.address
            ''', (f"{date}%",))
            return [{"order_id": row[0], "order_type": row[1], "order_date": row[2], "table_number": row[3], "customer_name": row[4], "customer_number": row[5], "address": row[6], "total": row[7]} for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving orders for {date}: {e}")
            return []

    def get_order_items(self, order_id):
        try:
            self.cursor.execute('''
                SELECT item_name, quantity, price, total
                FROM order_items
                WHERE order_id = ?
            ''', (order_id,))
            return [{"item_name": row[0], "quantity": row[1], "price": row[2], "total": row[3]} for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving items for order {order_id}: {e}")
            return []

    def add_expense(self, category, amount, date):
        try:
            self.cursor.execute('''
                INSERT INTO expenses (category, amount, date)
                VALUES (?, ?, ?)
            ''', (category, amount, date))
            self.conn.commit()
            print(f"Added expense: {category}, {amount}, {date}")
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")

    def get_expenses_today(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (today,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving today's expenses: {e}")
            return []

    def get_expenses_by_date(self, date):
        try:
            self.cursor.execute("SELECT category, amount FROM expenses WHERE date = ?", (date,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving expenses for {date}: {e}")
            return []

    def __del__(self):
        try:
            self.conn.close()
            print("Database connection closed")
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")

if __name__ == "__main__":
    db = Database()
    db.initialize_menu([
        {"name": "Burger", "price": 5.99},
        {"name": "Pizza", "price": 8.99},
    ])
    db.__del__()