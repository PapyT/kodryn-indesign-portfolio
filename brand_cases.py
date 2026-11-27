from pathlib import Path
from PIL import Image
import json,html,re
d=Path('dist')
manifest=json.loads(Path('COMMERCIAL-SOURCE-PREVIEWS.json').read_text(encoding='utf-8'))
projects=json.loads((d/'approved-projects.json').read_text(encoding='utf-8'))
by={p['slug']:p for p in projects}
def esc(s):return html.escape(str(s),quote=True)
def name(slug):return by[slug]['name'].replace('-',' ')
def url(slug,file):return f'/assets/approved-2026/{slug}/{file}'
arrow='<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 18 18 6M8 6h10v10"/></svg>'
for p in d.rglob('*.html'):
 s=p.read_text(encoding='utf-8').replace('/showcase.webp','/feature.webp')
 # The feature compositions are 1600 x 1000; preserve actual layout aspect ratio.
 s=re.sub(r'<img\b[^>]*feature\.webp[^>]*>',lambda m: re.sub(r'width="1440" height="960"','width="1600" height="1000"',m[0]),s)
 p.write_text(s,encoding='utf-8')
for slug,m in manifest.items():
 p=d/'work'/slug/'index.html';s=p.read_text(encoding='utf-8')
 n=name(slug); count=m['pages']
 route=re.search(r'href="/enquire/\?type=([^"]+)"',s).group(1)
 # Existing cover opens the first original board; set the hero to enlarge the actual visible image.
 s=s.replace(f'data-board-src="{url(slug,"board-01.webp")}"',f'data-board-src="{url(slug,"feature.webp")}"',1)
 s=re.sub(r'data-board-alt="[^"]*"(?= data-project-name="[^"]*" aria-label="Enlarge the first)',f'data-board-alt="{esc(n)} cover and interior composition"',s, count=1)
 s=re.sub(r'aria-label="Enlarge the first [^"]+ presentation board"',f'aria-label="Enlarge {esc(n)} feature artwork"',s,count=1)
 s=s.replace('class="shell commercial-section case-context"','class="shell commercial-section case-context" id="case-brief"',1)
 nav='<nav class="case-nav" aria-label="Case study sections"><a href="#case-brief">The brief</a><a href="#source-publication">Publication pages</a><a href="#case-pages">Design boards</a><a href="#case-enquire">Similar project?</a></nav>'
 s=s.replace('</dl></div></section>','</dl>'+nav+'</div></section>',1)
 s=s.replace('<p class="eyebrow">Source publication</p>','<p class="eyebrow" id="source-publication">Source publication</p>',1)
 s=s.replace('Select a page to view its full image.','Select any page to enlarge it. The page numbers refer to the original approved PDF.')
 figures=[]
 # Present selected feature pages first after cover, then any other source pages, without duplicating page numbers.
 order=list(dict.fromkeys([1]+m['feature_pages']+m['preview_pages']))
 for i in order:
  f=f'publication-{i:02}.webp'; u=url(slug,f)
  im=Image.open(d/u.lstrip('/'));w,h=im.size
  figures.append(f'<figure><button type="button" data-board-src="{u}" data-board-alt="{esc(n)} original source page {i}" data-project-name="{esc(n)}" aria-label="Enlarge source page {i}"><img src="{u}" alt="{esc(n)} original source publication page {i}" width="{w}" height="{h}" loading="lazy"></button><figcaption><span>Source page {i:02} / {count:02}</span><span>Enlarge {arrow}</span></figcaption></figure>')
 s=re.sub(r'<div class="source-pages">.*?</div></section>',lambda _:'<div class="source-pages">'+''.join(figures)+'</div></section>',s,count=1,flags=re.S)
 # Restore the original cover board as a third board following the selected source views.
 board1=url(slug,'board-01.webp')
 b=f'<figure class="detail-board"><div class="detail-board-head"><span>01 / 03</span><span>Cover and overview</span></div><button data-board-src="{board1}" data-board-alt="{esc(n)} presentation board 1" data-project-name="{esc(n)}" type="button" aria-label="Enlarge presentation board 1"><img loading="lazy" src="{board1}" alt="{esc(n)} original presentation board 1" width="1440" height="810"></button></figure>'
 s=s.replace('<div class="detail-spreads">','<div class="detail-spreads">'+b,1)
 cta=f'<div class="shell"><section class="case-conversion" id="case-enquire"><div><p class="eyebrow">Plan your own publication</p><h2>Need something like {esc(n)}?</h2><p>Share your document type, audience, page count and delivery requirements. We can discuss the layout scope and editable files before agreeing a project.</p></div><a class="hero-enquire" href="/enquire/?type={route}&amp;reference={slug}">Prepare a brief {arrow}</a></section></div>'
 s=s.replace('<div class="shell detail-next">',cta+'<div class="shell detail-next">',1)
 s=s.replace('aria-label="Enlarged presentation board"','aria-label="Enlarged publication artwork"')
 s=re.sub(r'(<small data-viewer-counter>).*?(</small>)',r'\g<1>View 1\2',s)
 p.write_text(s,encoding='utf-8')
# Project reference captured in enquiry brief when selected from a study.
p=d/'enquire/index.html';s=p.read_text(encoding='utf-8')
s=s.replace('<form id="brief-form">','<form id="brief-form"><label>Portfolio reference (optional)<input name="reference" placeholder="A study you like"></label>',1)
p.write_text(s,encoding='utf-8')
p=d/'app.js';s=p.read_text(encoding='utf-8')
s=s.replace("  if(initial && [...type.options].some(o=>o.value===initial))type.value=initial;","  if(initial && [...type.options].some(o=>o.value===initial))type.value=initial;\n  const reference=new URLSearchParams(location.search).get('reference');if(reference && form.elements.reference)form.elements.reference.value=reference.replace(/-/g,' ').slice(0,120);")
s=s.replace("'Estimated pages: '+val('pages')","'Portfolio reference: '+val('reference'),'Estimated pages: '+val('pages')")
p.write_text(s,encoding='utf-8')
# Six service-specific scope and preparation sections, no unverified delivery promises.
details={
'reports':('Clear reporting, from narrative to numbers.','Annual, impact and research reports; financial and performance summaries.','Document architecture, consistent table and chart layouts, clear data hierarchy and repeatable page systems.','Draft content, data tables, required report sections, brand assets and format specifications.'),
'magazines':('A distinctive editorial voice.','Magazines, journals, feature publications and cultural editorials.','Cover direction, contents, features, captions, folios and typographic styles.','Editorial plan, copy, image assets, audience and publishing format.'),
'catalogues':('Make product information easy to compare.','Product catalogues, specification sheets, furniture collections and lookbooks.','Product hierarchy, specification layouts, reference codes, imagery and reusable templates.','Product list, images, model codes, specifications, dimensions and format.'),
'brochures':('A clearer introduction to what you offer.','Company profiles, service guides, visitor publications and brochures.','Reading sequence, key messages, visual hierarchy and practical information layouts.','Copy, audience, visual references, brand assets, dimensions and production requirements.'),
'identity':('Consistency built into the system.','Brand guidelines, document templates and visual identity applications.','Typography, colour, composition and repeatable rules, scoped to your use cases.','Existing brand assets, target applications, design references and constraints.'),
'workbooks':('Make learning practical on the page.','Planning workbooks, coaching guides and guided exercises.','Instruction hierarchy, response space, repeatable activity templates and fillable PDF requirements when agreed.','Exercise copy, learning goals, audience, page count and intended print or digital use.')}
for r,(head,types,scope,inputs) in details.items():
 p=d/'services'/r/'index.html';s=p.read_text(encoding='utf-8')
 block=f'<section class="shell commercial-section"><p class="eyebrow">Scope your project</p><h2 class="commercial-subhead">{esc(head)}</h2><div class="commercial-columns"><article><h3>Suitable projects</h3><p>{esc(types)}</p></article><article><h3>Design scope</h3><p>{esc(scope)}</p></article><article><h3>What to prepare</h3><p>{esc(inputs)}</p></article></div><a class="hero-enquire" href="/enquire/?type={r}">Prepare a project brief {arrow}</a></section>'
 s=s.replace('</main>',block+'</main>',1)
 p.write_text(s,encoding='utf-8')
print('40 enhanced case studies and six service scope sections ready')
