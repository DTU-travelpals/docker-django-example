document.addEventListener('DOMContentLoaded', function () {
  const table = document.getElementById('task-table');
  if (!table) return;

  const headers = table.querySelectorAll('.sortable-header');
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  // Set initial sort state for the 'Date Done' column
  const dateDoneHeader = document.getElementById('date-done-header');
  if (dateDoneHeader) {
    dateDoneHeader.dataset.sortState = 'asc';
    const arrow = document.createElement('span');
    arrow.classList.add('sort-arrow', 'asc');
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

            const aNum = parseFloat(aValue);
            const bNum = parseFloat(bValue);

            let comparison = 0;
            if (!isNaN(aNum) && !isNaN(bNum)) {
              comparison = aNum - bNum;
            } else {
              comparison = aValue.localeCompare(bValue);
            }

            return sortState === 'asc' ? comparison : -comparison;
          });

      // Re-append sorted rows
      tbody.innerHTML = '';
      rowsToSort.forEach(row => tbody.appendChild(row));
    });
  });
});
