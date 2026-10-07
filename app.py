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
    pizzas = load_pizza_data()
    links = load_links()
    previews = load_preview()
    return render_template("base.html", pizzas=pizzas, links=links, previews=previews)

@app.route('/home')
def home():
    links = load_links()
    return render_template("sample.html", links=links)

@app.route('/about')
def about():
    links = load_links()
    return render_template("about.html", links=links)

@app.route('/menu')
def menu():
    pizzas = load_pizza_data()
    links = load_links()
    return render_template("menu.html", pizzas=pizzas, links=links)

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

if __name__ == '__main__':
    app.run(debug=True)