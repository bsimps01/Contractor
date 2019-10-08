from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Contractor
movies = db.movies

app = Flask(__name__)

@app.route('/')
def cinema_index():
    """Show all movies"""
    return render_template('cinema_index.html', movies=movies.find())

@app.route('/cinema/cart')
def cinema_cart():
    """Added to the cart"""
    return render_template('cinema_cart.html')


if __name__ == '__main__':
    app.run(debug=True)