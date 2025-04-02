import unittest
from app import app

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_fetch_processes(self):
        response = self.app.get('/api/processes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('processes', response.json)

    def test_cpu_details(self):
        response = self.app.get('/api/cpu-details')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cpu_count', response.json)

    def test_ask_ai(self):
        response = self.app.post('/ask-ai', json={"query": "What is my CPU usage?"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)

if __name__ == '__main__':
    unittest.main()