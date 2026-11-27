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
  const updateChrome=()=>{const meta=document.querySelector('meta[name=theme-color]');if(meta)meta.content=getComputedStyle(document.documentElement).getPropertyValue('--paper').trim()||'#031E24';};
  requestAnimationFrame(updateChrome);
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>requestAnimationFrame(updateChrome));
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
      theme = select.value; applyTheme(theme); requestAnimationFrame(updateChrome);
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
      if (counter) counter.textContent = 'View ' + (current + 1) + ' of ' + thumbs.length;
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

;(() => {
  const old = document.querySelector('.theme-switcher select');
  if (old) {
    const host = old.parentElement;
    host.setAttribute('role','group'); host.setAttribute('aria-label','Appearance theme');
    old.hidden = true; const label = host.querySelector('label'); if(label) label.hidden=true;
    const entries=[['system','System','◐'],['light','Light','☀'],['dark','Dark','☾']];
    const themeIcons={"system": "<svg class=\"ui-icon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\" focusable=\"false\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"13\" rx=\"2\"/><path d=\"M8 21h8m-4-4v4\"/></svg>", "light": "<svg class=\"ui-icon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5\"/></svg>", "dark": "<svg class=\"ui-icon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M20.5 14A8.5 8.5 0 0 1 10 3.5 9 9 0 1 0 20.5 14Z\"/></svg>"};
    const buttons=entries.map(([value,name,symbol])=>{
      const button=document.createElement('button'); button.type='button'; button.innerHTML=themeIcons[value];
      button.title=name+' theme'; button.setAttribute('aria-label',name+' theme');
      button.setAttribute('aria-pressed',String(old.value===value));
      button.addEventListener('click',()=>{old.value=value;old.dispatchEvent(new Event('change'));buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));});
      host.append(button); return button;
    });
  }
  const form=document.querySelector('#brief-form'); if(!form)return;
  const out=document.querySelector('#brief-output'),status=document.querySelector('#brief-status');
  const copy=document.querySelector('#copy-brief'),download=document.querySelector('#download-brief');
  const type=form.elements.type;
  const initial=new URLSearchParams(location.search).get('type');
  if(initial && [...type.options].some(o=>o.value===initial))type.value=initial;
  const reference=new URLSearchParams(location.search).get('reference');if(reference && form.elements.reference)form.elements.reference.value=reference.replace(/-/g,' ').slice(0,120);
  form.addEventListener('submit',event=>{
    event.preventDefault();
    const data=new FormData(form);
    const val=k=>String(data.get(k)||'').trim()||'To be discussed';
    out.value=['KODRYN / Publication design brief','','Publication type: '+type.selectedOptions[0].textContent,'Portfolio reference: '+val('reference'),'Estimated pages: '+val('pages'),'Deadline: '+val('deadline'),'Budget: '+val('budget'),'Deliverables: '+val('format'),'Content readiness: '+val('assets'),'Project goals and notes: '+val('notes')].join('\n');
    copy.disabled=download.disabled=false;status.textContent='Brief prepared. Copy or download it before contacting Kodryn.';
  });
  copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(out.value);status.textContent='Brief copied.';}catch{out.focus();out.select();status.textContent='Select and copy the brief manually.';}});
  download.addEventListener('click',()=>{const url=URL.createObjectURL(new Blob([out.value],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='kodryn-project-brief.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='Brief download requested.';});
})();
