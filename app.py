import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def load_pizza_data():
    with open('data/pizzas.json') as file:
        pizzas = json.load(file)
        return pizzas

def load_links():
    with open('data/links.json') as file:
        links = json.load(file)
        return links

def load_preview():
    with open('data/preview.json') as file:
        previews = json.load(file)
        return previews

@app.route('/')
def index():
    cart = session.get('cart', {})
    pizzas = load_pizza_data()
    links = load_links()
    previews = load_preview()
    return render_template("base.html", pizzas=pizzas, links=links, previews=previews, cart=cart)

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/about')
def about():
    links = load_links()
    return render_template("about.html", links=links)

@app.route('/menu')
def menu():
    cart = session.get('cart', {})
    pizzas = load_pizza_data()
    links = load_links()
    return render_template("menu.html", pizzas=pizzas, links=links, cart=cart)

@app.route('/order', methods=['POST'])
def order():
    pizza = request.form['pizza'] # this is going to ask if menu item exists
    quantity = int(request.form['quantity']) #this will turn the amount into a number
    pizzas = load_pizza_data() # it loads the data
    cart = session.get('cart', {}) # it gets the session to update the cart

    if pizza not in pizzas:
        flash("This item is not on the menu")
        return redirect(url_for('menu')) # returns to home if the item does not exist

    if pizza in cart:
        cart[pizza]['quantity'] += quantity # adds the quantity if the item exists
    else:
        cart[pizza] = { 
            'price': pizzas[pizza]['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True
    flash(f"{quantity} of {pizza} added to your order")
    return redirect(url_for('menu'))

@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})

    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"{item} was removed")
    else:
        flash("Item does not exist/is not in the cart.")
    return redirect(url_for('menu'))

@app.route('/cancel', methods=['POST'])
def cancel():
    session.pop('cart', None)
    session.modified = True

    flash(f"Cart Items have been removed")
    return redirect(url_for('menu'))


def calculate_total(cart):
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total


@app.route('/checkout', methods=['POST'])
def checkout():
    links = load_links()
    customer_name = request.form['customer_name'].strip().title()

    if not customer_name:
        flash("Requires a Customer Name")
        return redirect(url_for('home'))

    cart = session.get('cart', {})

    if not cart:
        flash("Empty Cart: Please add item(s)!")
        return redirect(url_for('home'))

    invoice_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    invoice_number = f"INV_{customer_name.replace('', '_')}_{invoice_date}"

    return render_template('invoice.html', cart=cart, customer_name=customer_name, invoice_number=invoice_number, invoice_date=invoice_date, links=links)

if __name__ == '__main__':
    app.run(debug=True)