from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
movies = db.movies
comments = db.comments

app = Flask(__name__)

# db.movies.insert_many([
#     {'title': 'Star Wars: A New Hope', 'description': 'A fight for the galaxy wages on!'},
#     {'title': 'Dark Knight', 'description': 'Batman fights against the madness of the Joker'},
#     {'title': 'Inception', 'description': 'Mind games are all the same...until your reality is changed'},
#     {'title': 'Sandlot', 'description': 'A couple kids playing in the backyard until the beast changes everything'},
# ])

@app.route('/')
def movies_index():
    """Show all movies."""
    return render_template('movies_index.html', movies=movies.find())

@app.route('/movies/new')
def movies_new():
    """Create a new cart option"""
    return render_template('movies_new.html', movie={}, title='Cart')

@app.route('/movies/<movie_id>', methods=['POST'])
def movies_update(movie_id):
    """Submit an edited movies list."""
    updated_movie = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': updated_movie})
    return redirect(url_for('movies_show', movie_id=movie_id))

@app.route('/movies/<movie_id>/edit')
def movies_edit(movie_id):
    """Show the edit form for a playlist."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('movies_edit.html', movie=movie, title='Edit Movie')


@app.route('/movies/<movie_id>/delete', methods=['POST'])
def movies_delete(movie_id):
    """Delete one playlist."""
    movies.delete_one({'_id': ObjectId(movie_id)})
    return redirect(url_for('movies_index'))

@app.route('/movies/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'movie_id': ObjectId(request.form.get('movie_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('movies_show', movie_id=request.form.get('movie_id')))

@app.route('/movies/<movie_id>')
def movies_show(movie_id):
    """Show a single playlist."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    movie_comments = comments.find({'movie_id': ObjectId(movie_id)})
    return render_template('movies_show.html', movie=movie, comments=movie_comments)

@app.route('/movies/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('movies_show', movie_id=comment.get('movie_id')))

@app.route('/movies', methods=['POST'])
def movies_submit():
    """Submit a new movie"""
    movie = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos', '').split(),
        'created_at': datetime.now()
    }
    print(movie)
    movie_id = movies.insert_one(movie).inserted_id
    return redirect(url_for('movies_show', movie_id=movie_id))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))