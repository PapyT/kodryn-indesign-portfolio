from pathlib import Path
import re
d=Path('dist')
p=d/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('Give ideas<br><em>form.</em>','Give ideas <br><em>form.</em>')
# Lead with a more commercially relevant, image-rich long-form editorial example.
s=s.replace('/assets/approved-2026/northline/showcase.webp','/assets/approved-2026/calloway/showcase.webp',2)
s=s.replace('href="/work/northline/" aria-label="Explore Northline"','href="/work/calloway/" aria-label="Explore Calloway"')
s=s.replace('Northline — approved design study artwork','Calloway — approved annual report design study artwork')
s=s.replace('Featured image / Northline','Featured study / Calloway annual report')
s=s.replace('01 / A collection of forty','48-page publication study')
p.write_text(s,encoding='utf-8')
# Correct dimensions for all new showcase images (leave original board dimensions unchanged).
for p in d.rglob('*.html'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'<img\b[^>]*showcase\.webp[^>]*>',lambda m:re.sub(r'height="810"','height="960"',m.group()),s)
 s=s.replace("Let's make<br><em>it readable.","Let's make <br><em>it readable.")
 p.write_text(s,encoding='utf-8')
p=d/'style.css'
s=p.read_text(encoding='utf-8')+'''
/* Final responsive refinements and editorial signposts */
.hero-left{padding-bottom:0}.hero-bottom{justify-content:flex-start;gap:24px}
.hero-bottom .text-action{margin:0}.hero-bottom .hero-enquire{margin:0}
.hero-art figcaption{flex-wrap:wrap;gap:5px 15px}
.case-grid h3{font-size:15px;letter-spacing:.02em;margin:22px 0 5px}
.case-grid h3+p{margin-top:0}
@media(max-width:580px){.hero-bottom{margin-top:24px;gap:12px}.hero-left{gap:0}.hero-stage-inner{padding-top:32px}.hero-bottom .text-action{min-height:44px}.hero-bottom .hero-enquire{min-height:44px}.hero-art figcaption{font-size:10px}.site-header .site-nav a{min-height:38px;display:flex;align-items:center}}
'''
p.write_text(s,encoding='utf-8')
p=Path('commercial_qa.cjs');s=p.read_text(encoding='utf-8-sig').replace("const p=await b.newPage();","const p=await b.newPage();await p.setCacheEnabled(false);").replace("r.ok()&&!data.overflow","(r.ok()||r.status()===304)&&!data.overflow").replace("data);if(path","{...data,status:r.status()});if(path")
p.write_text(s,encoding='utf-8')
