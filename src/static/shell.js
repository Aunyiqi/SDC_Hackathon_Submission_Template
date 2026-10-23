(() => {
  const search = document.getElementById('menuSearch');
  if (!search) return;

  const links = Array.from(document.querySelectorAll('.sidebar-nav .side-link'));

  function applyFilter() {
    const query = search.value.trim().toLowerCase();
    links.forEach((link) => {
      const text = link.textContent.toLowerCase();
      link.classList.toggle('menu-hidden', Boolean(query) && !text.includes(query));
    });
  }

  search.addEventListener('input', applyFilter);

  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const typing = target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target?.isContentEditable;

    if (event.key === '/' && !typing) {
      event.preventDefault();
      search.focus();
      search.select();
    }

    if (event.key === 'Escape' && document.activeElement === search) {
      search.value = '';
      applyFilter();
      search.blur();
    }
  });
})();
