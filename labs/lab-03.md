# Лабораторная работа №3

## Создание каталога товаров

### Цель
Реализовать главную страницу с выводом списка товаров из базы данных.

### Задачи
1. Файл `templates/base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Магазин Flask{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
<body>
    <header>
        <h1><a href="{{ url_for('index') }}">Магазин Flask</a></h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

2. Файл `templates/index.html`

```html
{% extends "base.html" %}

{% block content %}
<h2>Наши товары</h2>
<div class="products">
    {% for product in products %}
    <div class="product">
        <h3>{{ product.name }}</h3>
        <p class="price">{{ "%.2f"|format(product.price) }} руб.</p>
        <p>{{ product.description }}</p>
        <form action="{{ url_for('add_to_cart') }}" method="POST">
            <input type="hidden" name="product_id" value="{{ product.id }}">
            <label>Количество: <input type="number" name="quantity" value="1" min="1" style="width: 60px;"></label>
            <button type="submit">Добавить к заказу</button>
        </form>
    </div>
    {% endfor %}
</div>
<div style="margin-top: 20px; text-align: center;">
    <a href="{{ url_for('order') }}"><button>Перейти к оформлению заказа</button></a>
</div>
{% endblock %}
```

3. Обновленный `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, session
from models import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    if 'cart' not in session:
        session['cart'] = {}
    
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

4. Файл `static/style.css`

```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.products {
    display: grid;
    grid-gap: 20px;
}

.product {
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 5px;
}

.price {
    font-weight: bold;
    color: green;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
```

### Вопрос для самоконтроля
- Как Flask сохраняет данные сессии между запросами? Где физически хранятся эти данные?

### Полезные ссылки
- Основы Flask (маршруты, представления): https://pythonru.com/uroki/3-osnovy-flask


