from unittest.mock import patch

from django.apps import apps
from django.db import OperationalError
from django.test import TestCase
from redis.exceptions import ConnectionError

from up.apps import UpConfig


class ViewTests(TestCase):
    def test_up(self):
        """Up should respond with a success 200."""
        response = self.client.get("/up/", follow=True)
        self.assertEqual(response.status_code, 200)

    @patch("up.views.redis")
    def test_up_databases(self, mock_redis):
        """Up databases should respond with a success 200."""
        mock_redis.ping.return_value = True
        response = self.client.get("/up/databases", follow=True)
        self.assertEqual(response.status_code, 200)

    @patch("up.views.redis.ping", side_effect=ConnectionError)
    def test_up_databases_redis_error(self, mock_redis_ping):
        """Up databases should respond with a 500 if redis is down."""
        with self.assertRaises(ConnectionError):
            self.client.get("/up/databases", follow=True)

    @patch(
        "django.db.connection.ensure_connection", side_effect=OperationalError
    )
    def test_up_databases_db_error(self, mock_db_connection):
        """Up databases should respond with a 500 if the db is down."""
        with self.assertRaises(OperationalError):
            self.client.get("/up/databases", follow=True)


class UpConfigTests(TestCase):
    def test_apps(self):
        self.assertEqual(UpConfig.name, "up")
        self.assertEqual(apps.get_app_config("up").name, "up")
