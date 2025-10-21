import unittest
import json
import os
from dotenv import load_dotenv
from app import app

load_dotenv()

TOKEN = os.getenv("TEST_TOKEN")

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        }

    # ACTORS
    def test_get_actors_success(self):
        res = self.client.get('/actors', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_failure(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_post_actor_success(self):
        data = {"name": "Emma Stone", "age": 34, "gender": "Female"}
        res = self.client.post('/actors', headers=self.headers, data=json.dumps(data))
        self.assertEqual(res.status_code, 200)

    def test_post_actor_failure(self):
        data = {"name": "", "age": "", "gender": ""}
        res = self.client.post('/actors', headers=self.headers, data=json.dumps(data))
        self.assertEqual(res.status_code, 400)

    def test_patch_actor_success(self):
        data = {"age": 35}
        res = self.client.patch('/actors/1', headers=self.headers, data=json.dumps(data))
        self.assertIn(res.status_code, [200, 404])  # 404 si el actor no existe

    def test_delete_actor_success(self):
        res = self.client.delete('/actors/1', headers=self.headers)
        self.assertIn(res.status_code, [200, 404])

    # MOVIES
    def test_get_movies_success(self):
        res = self.client.get('/movies', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_failure(self):
        res = self.client.get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_post_movie_forbidden(self):
        data = {"title": "La La Land", "release_date": "2023-12-01"}
        res = self.client.post('/movies', headers=self.headers, data=json.dumps(data))
        self.assertEqual(res.status_code, 403)

    def test_patch_movie_success(self):
        data = {"title": "Updated Title"}
        res = self.client.patch('/movies/1', headers=self.headers, data=json.dumps(data))
        self.assertIn(res.status_code, [200, 404])

    def test_delete_movie_forbidden(self):
        res = self.client.delete('/movies/1', headers=self.headers)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()
