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


if __name__ == '__main__':
    app.run(debug=True)


