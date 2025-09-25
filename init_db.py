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
    print('База данных инициализирована!')


