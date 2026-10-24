import sqlite3

DB_NAME = "shoe_store.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            material TEXT NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [("admin", "123", "Администратор"), ("manager", "123", "Менеджер")]
        )
        
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        initial_products = [
            ("Air Max 270", "Nike", "Спортивная", 14990.00, "Текстиль"),
            ("Ultraboost Light", "Adidas", "Спортивная", 18500.00, "Текстиль"),
            ("Classic Oxford", "Ecco", "Классическая", 12300.00, "Кожа"),
            ("6-Inch Premium Boot", "Timberland", "Зимняя", 24900.00, "Нубук"),
            ("Chuck Taylor All Star", "Converse", "Повседневная", 8200.00, "Хлопок")
        ]
        cursor.executemany(
            "INSERT INTO products (name, brand, category, price, material) VALUES (?, ?, ?, ?, ?)",
            initial_products
        )
        
    conn.commit()
    conn.close()
