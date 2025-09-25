# Лабораторная работа №2

## Создание и наполнение базы данных

### Цель
Спроектировать и создать таблицы в SQLite, наполнить их тестовыми данными.

### Задачи
1. Файл `models.py`

```python
import sqlite3

# метод создания таблицы
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# подключение к базе данных
def init_db():
    conn = get_db_connection()
    
    # Таблица товаров
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    
    # Таблица заказов
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            total_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица элементов заказа
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()
```

2. Файл `init_db.py`

```python
from models import init_db, get_db_connection

def add_sample_products():
    conn = get_db_connection()
    sample_products = [
        ('Футболка Python', 19.99, 'Хлопковая футболка с принтом'),
        ('Кружка Flask', 12.50, 'Керамическая кружка объемом 350мл'),
        ('Наклейка SQLite', 2.99, 'Винтажная наклейка с логотипом'),
    ]
    conn.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', sample_products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_products()
    print("База данных инициализирована!")
```

3. Инициализация БД

```bash
python init_db.py
```

### Вопрос для самоконтроля
- Почему мы разделили заказы и товары по разным таблицам? Какую проблему решает таблица `order_items`?

### Полезные ссылки
- Учебник по SQLite3 в Python: https://digitology.tech/posts/uchebnik-po-sqlite3-v-python/


