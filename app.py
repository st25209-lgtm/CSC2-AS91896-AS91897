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
    return render_template("menu.html", pizzas1=pizzas1, links=links)

if __name__ == '__main__':
    app.run(debug=True)