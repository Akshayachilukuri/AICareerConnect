import unittest
from app import create_app, db
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_route(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_stats_api(self):
        response = self.client.get('/api/dashboard/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('kpi', data)
        self.assertIn('charts', data)

    def test_ai_chat_api(self):
        response = self.client.post('/api/ai/chat', json={
            'message': 'How do I prepare for a Flask senior developer interview?'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('reply', data)

if __name__ == '__main__':
    unittest.main()
