document.addEventListener('DOMContentLoaded', function () {
  const table = document.getElementById('task-table');
  if (!table) return;

  const headers = table.querySelectorAll('.sortable-header');
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  // Set initial sort state for the 'Date Done' column
  const dateDoneHeader = document.getElementById('date-done-header');
  if (dateDoneHeader) {
    dateDoneHeader.dataset.sortState = 'desc';
    const arrow = document.createElement('span');
    arrow.classList.add('sort-arrow', 'desc');
    dateDoneHeader.appendChild(arrow);
  }

  headers.forEach((header, index) => {
    header.addEventListener('click', () => {
      // Get current sort state, default to 'none'
      let sortState = header.dataset.sortState || 'none';

      // Reset all other headers
      headers.forEach(h => {
        if (h !== header) {
          h.dataset.sortState = 'none';
          h.querySelector('.sort-arrow')?.remove();
        }
      });

      // Cycle through states: none -> asc -> desc -> none
      if (sortState === 'none') {
        sortState = 'asc';
      } else if (sortState === 'asc') {
        sortState = 'desc';
      } else {
        sortState = 'none';
      }

      header.dataset.sortState = sortState;

      // Update sort arrow
      let arrow = header.querySelector('.sort-arrow');
      if (!arrow) {
        arrow = document.createElement('span');
        arrow.classList.add('sort-arrow');
        header.appendChild(arrow);
      }

      arrow.classList.remove('asc', 'desc');
      if (sortState === 'asc') {
        arrow.classList.add('asc');
      } else if (sortState === 'desc') {
        arrow.classList.add('desc');
      }

      // Determine the rows to sort
      const rowsToSort = sortState === 'none'
        ? rows.slice().sort((a, b) => a.dataset.originalIndex - b.dataset.originalIndex)
        : rows.slice().sort((a, b) => {
            const aValue = a.cells[index].textContent.trim();
            const bValue = b.cells[index].textContent.trim();
            const isDateColumn = header.id === 'date-done-header';

            let comparison = 0;

            if (isDateColumn) {
              const aDate = aValue && aValue !== 'None' ? new Date(aValue.replace('a.m.', 'am').replace('p.m.', 'pm')) : null;
              const bDate = bValue && bValue !== 'None' ? new Date(bValue.replace('a.m.', 'am').replace('p.m.', 'pm')) : null;

              if (aDate && bDate) {
                comparison = aDate - bDate;
              } else if (aDate) {
                comparison = -1; // a has date, b doesn't, so a comes first
              } else if (bDate) {
                comparison = 1; // b has date, a doesn't, so b comes first
              }
            } else {
              const aNum = parseFloat(aValue);
              const bNum = parseFloat(bValue);

              if (!isNaN(aNum) && !isNaN(bNum)) {
                comparison = aNum - bNum;
              } else {
                comparison = aValue.localeCompare(bValue);
              }
            }

            return sortState === 'asc' ? comparison : -comparison;
          });

      // Re-append sorted rows
      tbody.innerHTML = '';
      rowsToSort.forEach(row => tbody.appendChild(row));
    });
  });

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
