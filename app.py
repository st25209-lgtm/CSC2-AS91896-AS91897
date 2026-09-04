from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def load_pizza_data():
    with open('data/pizzas1.json') as file:
        pizzas1 = json.load(file)
        return pizzas1

def load_links():
    with open('data/links.json') as file:
        links = json.load(file)
        return links

@app.route('/')
def index():
    pizzas1 = load_pizza_data()
    links = load_links()
    return render_template("base.html", pizzas1=pizzas1, links=links)

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
    pizzas1 = load_pizza_data()
    links = load_links()
    return render_template("menu.html", pizzas1=pizzas1, links=links)

if __name__ == '__main__':
    app.run(debug=True)