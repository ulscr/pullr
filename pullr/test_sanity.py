import django.test
import unittest

class TestSanity(unittest.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_welcome_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.content), 0)
