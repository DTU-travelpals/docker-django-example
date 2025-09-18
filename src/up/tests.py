from unittest.mock import patch

from django.test import TestCase


class ViewTests(TestCase):
    def test_up(self):
        """Up should respond with a success 200."""
        response = self.client.get("/up/", follow=True)
        self.assertEqual(response.status_code, 200)

    @patch("redis.from_url")
    def test_up_databases(self, mock_from_url):
        """Up databases should respond with a success 200."""
        response = self.client.get("/up/databases", follow=True)
        self.assertEqual(response.status_code, 200)
