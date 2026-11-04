
/* Persistent theme selector. Absence of an override follows system preferences. */
(function(){
  const key='kodryn-theme';
  const root=document.documentElement;
  let saved='system';
  try{const value=localStorage.getItem(key);if(value==='light'||value==='dark')saved=value}catch(e){}
  function apply(theme){if(theme==='system'){root.removeAttribute('data-theme')}else{root.setAttribute('data-theme',theme)}}
  apply(saved);
  const nav=document.querySelector('header.site');
  if(!nav)return;
  const wrap=document.createElement('div');
  wrap.className='theme-picker';
  const id='theme-preference';
  const label=document.createElement('label');label.htmlFor=id;label.textContent='Theme';
  const select=document.createElement('select');select.id=id;select.setAttribute('aria-label','Appearance theme');
  [['system','System'],['light','Light'],['dark','Dark']].forEach(([v,t])=>{const option=document.createElement('option');option.value=v;option.textContent=t;select.appendChild(option)});
  select.value=saved;select.addEventListener('change',()=>{
    saved=select.value;apply(saved);
    try{if(saved==='system')localStorage.removeItem(key);else localStorage.setItem(key,saved)}catch(e){}
  });
  wrap.append(label,select);nav.appendChild(wrap);
})();


const cards=[...document.querySelectorAll('#archive [data-category]')],buttons=[...document.querySelectorAll('[data-filter]')],search=document.querySelector('#search');let chosen='all';
function refresh(){let visible=0;const q=(search?.value||'').trim().toLowerCase();buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===chosen)));cards.forEach(c=>{let match=(chosen==='all'||c.dataset.category===chosen)&&c.dataset.search.includes(q);c.hidden=!match;if(match)visible++});const count=document.querySelector('#project-count');if(count)count.textContent=visible+' of '+cards.length+' studies';document.querySelectorAll('.discipline').forEach(s=>{s.hidden=![...s.querySelectorAll('.project')].some(c=>!c.hidden)});const empty=document.querySelector('#empty');if(empty)empty.hidden=visible!==0}
buttons.forEach(b=>b.addEventListener('click',()=>{chosen=b.dataset.filter;refresh()}));search?.addEventListener('input',refresh);document.querySelector('#reset')?.addEventListener('click',()=>{chosen='all';search.value='';refresh()});refresh();
const viewer=document.querySelector('.viewer');if(viewer){const images=[...document.querySelectorAll('[data-large]')],photo=viewer.querySelector('img'),caption=viewer.querySelector('small');let at=0,last;function show(n){at=(n+images.length)%images.length;photo.src=images[at].dataset.large;photo.alt=images[at].dataset.alt;caption.textContent='Board '+(at+1)+' of '+images.length}images.forEach((b,i)=>b.addEventListener('click',()=>{last=b;show(i);viewer.showModal()}));viewer.querySelector('[data-prev]').addEventListener('click',()=>show(at-1));viewer.querySelector('[data-next]').addEventListener('click',()=>show(at+1));viewer.querySelector('[data-close]').addEventListener('click',()=>viewer.close());viewer.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();show(at-1)}if(e.key==='ArrowRight'){e.preventDefault();show(at+1)}});viewer.addEventListener('close',()=>last?.focus());viewer.addEventListener('click',e=>{if(e.target===viewer)viewer.close()})}
