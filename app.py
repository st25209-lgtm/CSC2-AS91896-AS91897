from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def load_pizza_data():
    with open('data/pizzas1.json') as file:
        pizzas1 = json.load(file)
        return pizzas1

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)