# tests.py

from unittest import TestCase, main as unittest_main
from app import app
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

sample_movie_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_movie = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'title': sample_movie['title'],
    'description': sample_movie['description'],
    'videos': '\n'.join(sample_movie['videos'])
}

class MoviesTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the playlists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Movie', result.data)

    def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/movies/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Movie', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_movie(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/playlists/{sample_movie_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_movie(self, mock_find):
        """Test editing a single playlist."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/movies/{sample_movie_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_movie(self, mock_insert):
        """Test submitting a new playlist."""
        result = self.client.post('/movies', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_movie)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_movie(self, mock_update):
        result = self.client.post(f'/playlists/{sample_movie_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_movie_id}, {'$set': sample_movie})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_movie(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/movies/{sample_movie_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_movie_id})
        
if __name__ == '__main__':
    unittest_main()