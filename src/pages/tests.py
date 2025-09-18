from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory, TestCase

from .tasks import read_tasks_from_db


class ViewTests(TestCase):
    def test_home_page(self):
        """Home page should respond with a success 200."""
        with patch.dict("os.environ", {"PYTHON_VERSION": "3.11"}):
            response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)


class TaskSortingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mock_tasks = [
            {
                "task_id": "1",
                "status": "SUCCESS",
                "result": "A",
                "date_done": "2023-01-01T12:00:00",
                "completed": True,
            },
            {
                "task_id": "2",
                "status": "PENDING",
                "result": "B",
                "date_done": "2023-01-03T12:00:00",
                "completed": False,
            },
            {
                "task_id": "3",
                "status": "FAILURE",
                "result": "C",
                "date_done": "2023-01-02T12:00:00",
                "completed": True,
            },
        ]

    @patch("pages.views.read_tasks_from_db")
    def test_task_list_default_sorting(self, mock_read_tasks):
        mock_read_tasks.return_value = sorted(
            self.mock_tasks, key=lambda x: x["date_done"], reverse=True
        )

        with patch.dict("os.environ", {"PYTHON_VERSION": "3.11"}):
            response = self.client.get("/tasks/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "task_id")

        # Check if the tasks are sorted by date_done descending
        task_ids = [t["task_id"] for t in response.context["tasks"]]
        self.assertEqual(task_ids, ["2", "3", "1"])

    def test_read_tasks_from_db_sorting(self):
        # Test sorting by result ascending
        sorted_tasks = read_tasks_from_db(
            settings, sort_by="result", sort_order="asc", tasks=self.mock_tasks
        )
        self.assertEqual([t["result"] for t in sorted_tasks], ["A", "B", "C"])

        # Test sorting by status descending
        sorted_tasks = read_tasks_from_db(
            settings,
            sort_by="status",
            sort_order="desc",
            tasks=self.mock_tasks,
        )
        self.assertEqual(
            [t["status"] for t in sorted_tasks],
            ["SUCCESS", "PENDING", "FAILURE"],
        )

        # Test sorting by completed ascending
        sorted_tasks = read_tasks_from_db(
            settings,
            sort_by="completed",
            sort_order="asc",
            tasks=self.mock_tasks,
        )
        self.assertEqual(
            [t["completed"] for t in sorted_tasks], [False, True, True]
        )
