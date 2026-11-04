(() => {
  'use strict';

  // The default ('system') deliberately leaves data-theme unset.
  const themeKey = 'kodryn-theme';
  let theme = 'system';
  try { const stored = localStorage.getItem(themeKey); if (stored === 'light' || stored === 'dark') theme = stored; } catch (_) {}
  const applyTheme = (value) => {
    if (value === 'system') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', value);
  };
  applyTheme(theme);
  const header = document.querySelector('.site-header');
  if (header) {
    const holder = document.createElement('div');
    holder.className = 'theme-switcher';
    const label = document.createElement('label');
    label.htmlFor = 'theme-choice'; label.textContent = 'Theme';
    const select = document.createElement('select');
    select.id = 'theme-choice'; select.setAttribute('aria-label', 'Choose appearance theme');
    [['system','System'], ['light','Light'], ['dark','Dark']].forEach(([value, text]) => {
      const option = document.createElement('option'); option.value = value; option.textContent = text; select.appendChild(option);
    });
    select.value = theme;
    select.addEventListener('change', () => {
      theme = select.value; applyTheme(theme);
      try { if (theme === 'system') localStorage.removeItem(themeKey); else localStorage.setItem(themeKey, theme); } catch (_) {}
    });
    holder.append(label, select);
    header.appendChild(holder);
  }

  const qs = (q, root = document) => root.querySelector(q);
  const qsa = (q, root = document) => Array.from(root.querySelectorAll(q));

  const rows = qsa('.archive-row');
  const archiveSearch = qs('#archive-search');
  const filterButtons = qsa('[data-archive-filter]');
  const archiveCount = qs('#archive-count');
  const archiveEmpty = qs('#archive-empty');
  const stageImage = qs('#archive-stage-image');
  const stageName = qs('#archive-stage-name');
  const stageCategory = qs('#archive-stage-category');
  let activeCategory = 'all';

  const renderArchivePreview = (row) => {
    if (!row || !stageImage) return;
    const src = row.dataset.image;
    if (src && stageImage.getAttribute('src') !== src) {
      stageImage.src = src;
      stageImage.alt = row.dataset.name + ' — approved publication design';
    }
    if (stageName) stageName.textContent = row.dataset.name;
    if (stageCategory) stageCategory.textContent = row.dataset.categoryName;
  };

  const applyArchiveFilters = () => {
    const query = (archiveSearch?.value || '').trim().toLowerCase();
    let total = 0;
    let first = null;
    filterButtons.forEach((button) => button.setAttribute(
      'aria-pressed', String(button.dataset.archiveFilter === activeCategory)
    ));
    rows.forEach((row) => {
      const matching = (activeCategory === 'all' || row.dataset.category === activeCategory) &&
        (row.dataset.search || '').includes(query);
      row.hidden = !matching;
      if (matching) { total += 1; if (!first) first = row; }
    });
    if (archiveCount) archiveCount.textContent = total + ' / ' + rows.length + ' projects';
    if (archiveEmpty) archiveEmpty.hidden = total !== 0;
    renderArchivePreview(first);
  };

  if (rows.length) {
    rows.forEach((row) => {
      row.addEventListener('mouseenter', () => renderArchivePreview(row));
      row.addEventListener('focus', () => renderArchivePreview(row));
    });
    filterButtons.forEach((button) => button.addEventListener('click', () => {
      activeCategory = button.dataset.archiveFilter;
      applyArchiveFilters();
    }));
    archiveSearch?.addEventListener('input', applyArchiveFilters);
    qs('#archive-clear')?.addEventListener('click', () => {
      if (archiveSearch) archiveSearch.value = '';
      activeCategory = 'all';
      applyArchiveFilters();
      archiveSearch?.focus();
    });
    applyArchiveFilters();
  }

  const viewer = qs('dialog.viewer');
  if (viewer) {
    const thumbs = qsa('[data-board-src]');
    const image = qs('.viewer-img', viewer);
    const title = qs('[data-viewer-title]', viewer);
    const counter = qs('[data-viewer-counter]', viewer);
    let current = 0;
    let lastTrigger = null;

    const show = (n) => {
      if (!thumbs.length) return;
      current = (n + thumbs.length) % thumbs.length;
      const button = thumbs[current];
      const src = button.dataset.boardSrc;
      if (image && src) {
        image.src = src;
        image.alt = button.dataset.boardAlt || 'Portfolio board';
      }
      if (title) title.textContent = button.dataset.projectName || '';
      if (counter) counter.textContent = 'Board ' + (current + 1) + ' of ' + thumbs.length;
    };

    thumbs.forEach((button, i) => button.addEventListener('click', () => {
      lastTrigger = button;
      show(i);
      if (typeof viewer.showModal === 'function') viewer.showModal();
    }));
    qs('[data-close-viewer]', viewer)?.addEventListener('click', () => viewer.close());
    qs('[data-prev-board]', viewer)?.addEventListener('click', () => show(current - 1));
    qs('[data-next-board]', viewer)?.addEventListener('click', () => show(current + 1));
    viewer.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
    });
    viewer.addEventListener('click', (event) => { if (event.target === viewer) viewer.close(); });
    viewer.addEventListener('close', () => lastTrigger?.focus());
  }
})();
