from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import os

account_sid = ""
auth_token = ""
host = os.environ.get()
client = MongoClient()
twilio_client = Client(account_sid, auth_token)
db = client.movies()
movies = db.movies
movies.drop()
carts = db.carts
carts.drop()

app = Flask(__name__)
response = MessagingResponse()
response.message("Thank you for your purchase!")

db.movies.insert_many([
    {'title': 'Star Wars: A New Hope', 'description': 'A fight for the galaxy wages on!'},
    {'title': 'Dark Knight', 'description': 'Batman fights against the madness of the Joker'},
    {'title': 'Inception', 'description': 'Mind games are all the same...until your reality is changed'},
    {'title': 'Sandlot', 'description': 'A couple kids playing in the backyard until the beast changes everything'},
])

print(response)

@app.route('/')
def cinema_index():
    """Show all movies"""
    movies = movies.find()
    return render_template('cinema_index.html', movies=movies)

@app.route('/cinema/cart')
def cinema_cart():
    """Added to the cart"""
    cart = carts.find({'_id': ObjectId(movie)})
    total_price = list(carts.find())
    for money in range(len(total_price)):
        total += total_price[money]
    return render_template('cinema_cart.html', carts=cart)

@app.route('/movies/<movies_id>/add', methods=['POST'])
def buy_movie(movies_id):
    """Adds Movie"""
    carts.find('_id': ObjectId(movies_id))
    return render_template('movie_new.html')
if __name__ == '__main__':
    app.run(debug=True)