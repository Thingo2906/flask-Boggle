from unittest import TestCase
from app import app
from flask import session
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
class FlaskTests(TestCase):
    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('timeplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["L", "A", "T", "K", "T"], 
                                 ["C", "B", "Y", "M", "T"], 
                                 ["D", "A", "H", "C", "T"], 
                                 ["O", "L", "T", "K", "S"], 
                                 ["C", "F", "P", "L", "K"]]
        response = client.get('/check-word?word=do')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        with app.test_client() as client:

            client.get('/')
            response = client.get('/check-word?word=beautiful')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_english_word(self):
        """Test if word is on the board"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=hsgywgdjjdvgsbvd')
            self.assertEqual(response.json['result'], 'not-word')