import os
from importlib import reload
from unittest.mock import patch

from django.test import TestCase


class SettingsTests(TestCase):
    @patch.dict(os.environ, {"DEBUG": "true"})
    def test_debug_true(self):
        from config import settings

        reload(settings)
        self.assertTrue(settings.DEBUG)

    @patch.dict(os.environ, {"DEBUG": "false"})
    def test_debug_false(self):
        from config import settings

        reload(settings)
        self.assertFalse(settings.DEBUG)

    @patch.dict(os.environ, {"ALLOWED_HOSTS": "test.com,example.com"})
    def test_allowed_hosts(self):
        from config import settings

        reload(settings)
        self.assertEqual(settings.ALLOWED_HOSTS, ["test.com", "example.com"])

    def test_installed_apps(self):
        from config import settings

        self.assertIn("pages.apps.PagesConfig", settings.INSTALLED_APPS)

    @patch.dict(os.environ, {"SECRET_KEY": "test-secret"})
    def test_secret_key(self):
        from config import settings

        reload(settings)
        self.assertEqual(settings.SECRET_KEY, "test-secret")


class UrlsTests(TestCase):
    def test_debug_toolbar_not_in_testing(self):
        from config import urls

        self.assertNotIn(
            "__debug__/", [p.pattern.regex.pattern for p in urls.urlpatterns]
        )


class WsgiAsgiTests(TestCase):
    def test_wsgi(self):
        from config import wsgi  # noqa

    def test_asgi(self):
        from config import asgi  # noqa


class CeleryTests(TestCase):
    def test_celery(self):
        from config import celery  # noqa


class GunicornTests(TestCase):
    @patch.dict(os.environ, {"PORT": "8080"})
    def test_gunicorn_bind(self):
        from config import gunicorn

        reload(gunicorn)
        self.assertEqual(gunicorn.bind, "0.0.0.0:8080")

    @patch("multiprocessing.cpu_count", return_value=2)
    def test_gunicorn_workers(self, mock_cpu_count):
        from config import gunicorn

        reload(gunicorn)
        self.assertEqual(gunicorn.workers, 4)
