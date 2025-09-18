document.addEventListener('DOMContentLoaded', function () {
  const table = document.getElementById('task-table');
  if (!table) return;

  const checkboxes = table.querySelectorAll('.task-completed-checkbox');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const taskId = this.dataset.taskId;
      const isChecked = this.checked;

      // We need a CSRF token for Django POST requests
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch('/tasks/update-status/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
          task_id: taskId,
          completed: isChecked,
        }),
      })
      .then(response => {
        if (!response.ok) {
          // Revert checkbox state if the update fails
          this.checked = !isChecked;
          // Optionally, show an error message to the user
          console.error('Failed to update task status.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        this.checked = !isChecked;
      });
    });
  });
});
