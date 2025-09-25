# Лабораторная работа №4

## Создание страницы оформления заказа

### Цель
Реализовать страницу оформления заказа с отображением товаров, возможностью изменения количества и заполнения контактных данных.

### Задачи
1. Файл `templates/order.html`

```html
{% extends "base.html" %}

{% block content %}
<h2>Оформление заказа</h2>

{% if cart_items %}
<form action="{{ url_for('process_order') }}" method="POST">
    <h3>Ваш заказ:</h3>
    <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
        <thead>
            <tr>
                <th>Товар</th>
                <th>Цена</th>
                <th>Количество</th>
                <th>Сумма</th>
            </tr>
        </thead>
        <tbody>
            {% for item in cart_items %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ "%.2f"|format(item.price) }} руб.</td>
                <td>
                    <input type="number" name="quantity_{{ item.id }}" value="{{ item.quantity }}" min="1" style="width: 60px;">
                </td>
                <td>{{ "%.2f"|format(item.total) }} руб.</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <td colspan="3" style="text-align: right;"><strong>Итого:</strong></td>
                <td><strong>{{ "%.2f"|format(total_price) }} руб.</strong></td>
            </tr>
        </tfoot>
    </table>

    <h3>Контактные данные:</h3>
    <div>
        <label>ФИО:* <input type="text" name="customer_name" required></label><br><br>
        <label>Email:* <input type="email" name="customer_email" required></label><br><br>
        <label>Телефон:* <input type="tel" name="customer_phone" required></label><br><br>
        <label>Адрес доставки:* <textarea name="customer_address" required></textarea></label><br><br>
    </div>

    <button type="submit">Подтвердить заказ</button>
</form>
{% else %}
<p>Ваша корзина пуста. <a href="{{ url_for('index') }}">Вернуться к покупкам</a>.</p>
{% endif %}
{% endblock %}
```

2. Добавление маршрутов в `app.py`

```python
@app.route('/order')
def order():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    if cart:
        conn = get_db_connection()
        for product_id, quantity in cart.items():
            product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
            if product:
                item_total = product['price'] * quantity
                cart_items.append({
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'total': item_total
                })
                total_price += item_total
        conn.close()

    return render_template('order.html', cart_items=cart_items, total_price=total_price)

@app.route('/process_order', methods=['POST'])
def process_order():
    cart = session.get('cart', {})
    
    # Обновление количеств товаров
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = key.split('_')[1]
            if product_id in cart:
                new_quantity = int(value)
                if new_quantity > 0:
                    cart[product_id] = new_quantity
                else:
                    del cart[product_id]
    
    session['cart'] = cart

    # Создание заказа если корзина не пуста
    if cart:
        conn = get_db_connection()

        # Расчет общей суммы
        total_price = 0
        for product_id, quantity in cart.items():
            product = conn.execute('SELECT price FROM products WHERE id = ?', (product_id,)).fetchone()
            total_price += product['price'] * quantity

        # Создание заказа
        cursor = conn.execute(
            'INSERT INTO orders (customer_name, customer_email, customer_phone, customer_address, total_price) VALUES (?, ?, ?, ?, ?)',
            (request.form['customer_name'], request.form['customer_email'], request.form['customer_phone'], request.form['customer_address'], total_price)
        )
        order_id = cursor.lastrowid

        # Добавление товаров заказа
        for product_id, quantity in cart.items():
            conn.execute(
                'INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                (order_id, product_id, quantity)
            )

        conn.commit()
        conn.close()

        # Очистка корзины
        session.pop('cart', None)

        return f"<h1>Спасибо за заказ, {request.form['customer_name']}!</h1><p>Ваш заказ №{order_id} успешно оформлен.</p>"
    else:
        return redirect(url_for('index'))
```

### Вопрос для самоконтроля
- Почему мы используем `quantity_{{ item.id }}` в именах полей ввода? Как потом правильно обработать эти данные?

### Полезные ссылки
- Основы Flask (маршрутизация и обработка запросов): https://pythonru.com/uroki/3-osnovy-flask


