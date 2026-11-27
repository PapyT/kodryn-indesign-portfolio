from pathlib import Path
import re,json,html,collections
d=Path('dist')
mark='<path fill="currentColor" d="M163 11H46C27 11 11 29 11 50V234L104 114Q140 59 164 13Z"/><path fill="#008C76" d="M256 10H334L193 154Q211 164 217 174L334 295H213Q196 295 183 284L96 196Q81 183 62 189L223 24Q237 11 256 10Z"/><path fill="#91C785" d="M11 288Q27 247 44 219Q59 201 77 207Q87 211 96 223L136 278Q143 291 131 295H13Q8 294 11 288Z"/>'
word='<path fill="currentColor" fill-rule="evenodd" d="M9 11H45V84L117 12H163L88 91L167 177H119L59 112L45 126V177H8Z M244 9C193 9 153 43 153 94S193 180 244 180 336 145 336 94 296 9 244 9ZM244 42C275 42 297 64 297 94S275 146 244 146 191 124 191 94 213 42 244 42Z M359 11H440C490 11 519 45 519 94S489 177 443 177H358ZM394 42V145H439C466 145 480 123 480 94S464 43 439 43Z M542 11H632C661 11 681 29 681 60Q681 100 645 117L692 177H649L605 121H578V177H540V13ZM578 43V91H621Q643 91 643 65T618 42Z M681 11H723L766 79 809 11H849L785 113V177H748V114Z M866 11H900L987 117L989 11H1025V177H990L902 72V177H865Z"/><rect x="1057" y="128" width="52" height="49" rx="4" fill="#70C507"/>'
logo='<svg class="brand-logo" viewBox="0 0 1550 305" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><g>'+mark+'</g><path d="M380 27V281" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><g transform="translate(420 57)">'+word+'</g></svg>'
(d/'assets/kodryn-brand.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 345 305" color="#031E24">'+mark+'</svg>',encoding='utf-8')
icons={'up-right':'<path d="M6 18 18 6M8 6h10v10"/>','right':'<path d="M4 12h16m-6-6 6 6-6 6"/>','left':'<path d="M20 12H4m6-6-6 6 6 6"/>','down':'<path d="M12 4v16m-6-6 6 6 6-6"/>','system':'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8m-4-4v4"/>','light':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>','dark':'<path d="M20.5 14A8.5 8.5 0 0 1 10 3.5 9 9 0 1 0 20.5 14Z"/>'}
def icon(n):return '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+icons[n]+'</svg>'
def fix_symbols(s):
 for code,name in [('↗','up-right'),('→','right'),('←','left'),('↓','down'),('&#8599;','up-right'),('&#8594;','right'),('&#8592;','left'),('&#8595;','down')]:
  s=s.replace(code,icon(name))
 return s
def esc(s):return html.escape(str(s),quote=True)
for p in d.rglob('*.html'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'<a class="brandmark"[^>]*>.*?</a>','<a class="brandmark" href="/" aria-label="Kodryn Editorial and Publication Design home">'+logo+'<span>Editorial &amp; Publication Design</span></a>',s,flags=re.S)
 s=s.replace('href="/assets/kodryn-mark.png" type="image/png"','href="/assets/kodryn-brand.svg" type="image/svg+xml"').replace('href="/assets/kodryn-mark.png"','href="/assets/kodryn-brand.svg"')
 s=re.sub(r'<a class="footer-brand" href="/">.*?</a>','<a class="footer-brand" href="/" aria-label="Kodryn home">'+logo+'<span>Editorial &amp; Publication Design</span></a>',s)
 s=s.replace('content="#151c1c"','content="#031E24"')
 s=fix_symbols(s)
 # Use explicit icon classes to repair malformed arrow glyphs independently of font rendering.
 for cls,n in [('chapter-arrow','up-right'),('archive-out','up-right')]:
  s=re.sub(r'(<span class="'+cls+r'"[^>]*>).*?(</span>)',lambda m:m[1]+icon(n)+m[2],s)
 for attr,n in [('data-prev-board','left'),('data-next-board','right')]:
  s=re.sub(r'(<button '+attr+r'[^>]*>).*?(</button>)',lambda m:m[1]+icon(n)+m[2],s)
 s=re.sub(r'(<span aria-hidden="true">)[\x19\x1a\x1b?](</span>)',lambda m:m[1]+icon('right')+m[2],s)
 s=re.sub(r'(<a href="/work/[^"]+"><span>Previous in this collection</span><b>)(.*?)(</b>)',lambda m:m[1]+re.sub(r'[\x19\x1a\x1b?]\s*$','',m[2])+m[3],s)
 s=s.replace('loading="eager"','loading="lazy"')
 p.write_text(s,encoding='utf-8')
# System theme buttons use inline SVG rather than font glyphs. Keep select behaviour.
p=d/'app.js';s=p.read_text(encoding='utf-8')
s=s.replace('button.textContent=symbol;', 'button.innerHTML=themeIcons[value];')
themeIcons={k:icon(k) for k in ('system','light','dark')}
s=s.replace('const buttons=entries.map', 'const themeIcons='+json.dumps(themeIcons)+';\n    const buttons=entries.map',1)
s=s.replace("counter.textContent = 'Board '", "counter.textContent = 'View '")
# Theme meta follows actual appearance even on system preference changes.
s=s.replace("  applyTheme(theme);","  applyTheme(theme);\n  const updateChrome=()=>{const meta=document.querySelector('meta[name=theme-color]');if(meta)meta.content=getComputedStyle(document.documentElement).getPropertyValue('--paper').trim()||'#031E24';};\n  requestAnimationFrame(updateChrome);\n  matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>requestAnimationFrame(updateChrome));",1)
s=s.replace('theme = select.value; applyTheme(theme);','theme = select.value; applyTheme(theme); requestAnimationFrame(updateChrome);')
p.write_text(s,encoding='utf-8')
# Client-focused hero and conversion pathway.
p=d/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('Independent publication design / 2026','KODRYN / Editorial &amp; Publication Design')
s=s.replace('Give ideas <br><em>form.</em>','Publications built <br>to <em>communicate.</em>')
s=s.replace('Editorial and publication design for brands, businesses and organisations. Annual reports, magazines, catalogues and brochures, thoughtfully built in Adobe InDesign.','Turn complex content into clear, confident publications. Kodryn designs annual reports, magazines, catalogues and brochures with purposeful layouts and production-conscious Adobe InDesign workflows.')
s=s.replace('Explore selected work','View selected work')
s=s.replace('Discuss your project','Start a project')
s=s.replace('02 / Explore by discipline','03 / Explore by discipline')
s=s.replace('Not an endless grid. The complete 40-project collection is organised by discipline and available in an editorial index.','Explore the complete collection of 40 design studies by discipline, document type or project name.')
s=s.replace('</figure>\n </div></section>','</figure>\n </div></section>',1)
trust='<div class="shell proof-strip"><div><strong>40</strong><span>Self-initiated design studies</span></div><div><strong>6</strong><span>Publication service categories</span></div><div><strong>InDesign</strong><span>Editable layouts &amp; PDF delivery, by scope</span></div></div>'
s=s.replace('<div class="shell strip"',trust+'<div class="shell strip"',1)
s=s.replace('<section class="cta-section">','<section class="shell commercial-section faq"><div class="section-heading"><div><p class="eyebrow">Before you enquire</p><h2>Good <em>questions.</em></h2></div><p>What to know before commissioning publication design.</p></div><details><summary>What should I prepare?</summary><p>Share draft copy, available imagery, brand guidelines, audience, estimated page count, deadline and intended format. We can discuss what is still missing.</p></details><details><summary>Can I request editable files?</summary><p>InDesign or IDML source, linked assets and PDF exports can be included in the agreed scope. Font and image licences are handled separately.</p></details><details><summary>Can you prepare documents for print?</summary><p>Print specifications, bleed, colour requirements and printer instructions are agreed before production. Screen PDFs can also be scoped.</p></details><details><summary>Are these commissioned projects?</summary><p>The 40 projects shown are self-initiated design studies. Illustrative data and fictional briefs are not client testimonials or commercial results.</p></details></section><section class="cta-section">',1)
p.write_text(s,encoding='utf-8')
# Add direct marketplace link and brief-focused user journey. No invented delivery endpoint.
p=d/'enquire/index.html';s=p.read_text(encoding='utf-8')
s=s.replace('Prepare a brief before contacting Kodryn. Your entries stay in this browser and are not sent automatically.','Tell us what you need, prepare a clear brief and contact Kodryn through the existing Fiverr channel. Nothing is submitted automatically.')
s=s.replace('<div class="enquiry-grid">','<div class="enquiry-route"><a class="button-secondary" href="https://www.fiverr.com/kodryn_tech/" target="_blank" rel="noopener noreferrer">Already have a brief? Contact on Fiverr '+icon('up-right')+'</a><p>Or complete the guided brief below. No payment or account is required to prepare it.</p></div><div class="enquiry-grid">',1)
s=s.replace('Prepare my brief','Prepare project brief')
s=s.replace('Your next step.','Share your brief.')
p.write_text(s,encoding='utf-8')
print('Brand and interaction markup updated')
