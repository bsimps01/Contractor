from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Contractor
movies = db.movies

app = Flask(__name__)

@app.route('/')
def cinema_index():
    """Show all playlists."""
    return render_template('cinema_index.html', cinemas=cinemas.find())

if __name__ == '__main__':
    app.run(debug=True)