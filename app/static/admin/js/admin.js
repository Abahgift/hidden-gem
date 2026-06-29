document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(link => {
    const href = link.getAttribute('href') || '';
    if (href && href.split('/').pop() === currentPath) {
      link.classList.add('active');
    }
  });

  const filterButtons = document.querySelectorAll('[data-filter]');
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const group = button.dataset.group;
      const value = button.dataset.filter;
      const items = document.querySelectorAll(`[data-group="${group}"]`);
      items.forEach(item => {
        const matches = value === 'all' || item.dataset[group] === value;
        item.style.display = matches ? '' : 'none';
      });
      button.parentElement.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });

  const searchInputs = document.querySelectorAll('[data-search]');
  searchInputs.forEach(input => {
    input.addEventListener('input', () => {
      const value = input.value.toLowerCase();
      const group = input.dataset.search;
      const items = document.querySelectorAll(`[data-group="${group}"]`);
      items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(value) ? '' : 'none';
      });
    });
  });
});
