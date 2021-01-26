import unittest

from flask.globals import request
from flask.wrappers import Response

from bot import app
class TestApli(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        pass
    
    def test_00_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_01_login(self):
        response = self.app.post('/login', data=dict(username="dirgaizan@yahoo.com", password="a"))
        self.assertEqual(response.status_code, 302)

    def test_02_login(self):
        response = self.app.post('/login', data=dict(username="dirgaizan@yahoo.com", password="ab"))
        if "Email atau User Salah!" in str(response.data):
            a = "Email atau User Salah!"
        else:
            a = "Ada"
        self.assertEqual(a, "Email atau User Salah!")

    def test_03_logout(self):
        with self.app.session_transaction() as session:
            session["user"] = "dirgaizan@yahoo.com"
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_04_indexHome(self):
        with self.app.session_transaction() as session:
            session["user"] = "dirgaizan@yahoo.com"
        response = self.app.post("/")
        self.assertEqual(response.status_code, 200)

