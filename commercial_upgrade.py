from pathlib import Path
import json, zipfile, re, html, os
from PIL import Image, ImageDraw, ImageFilter
import pymupdf as fitz
root=Path(__file__).resolve().parent
d=root/'dist'
projects=json.loads((d/'approved-projects.json').read_text(encoding='utf-8'))
manifest={x['slug']:x for x in json.loads((root/'EDITORIAL-ARTWORK-SOURCE-MANIFEST.json').read_text(encoding='utf-8'))}
delivery=Path.home()/'Downloads/Telegram Desktop/Extracted-Portfolio-Windows/Approved-Portfolio/05-Design-Upgrade-In-Progress/DELIVERY'
archives={}
for p in delivery.rglob('*.zip'):
    if 'SUPERSEDED' not in str(p): archives.setdefault(p.name,[]).append(p)
def esc(s): return html.escape(str(s),quote=True)
def get(p): return p.read_text(encoding='utf-8')
def put(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def render(page, cap=1700):
    pix=page.get_pixmap(matrix=fitz.Matrix(cap/max(page.rect.width,page.rect.height),cap/max(page.rect.width,page.rect.height)),alpha=False)
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
def fit(img,w,h):
    im=img.copy(); im.thumbnail((w,h),Image.Resampling.LANCZOS); return im
def paste_shadow(canvas,img,xy):
    x,y=xy
    shadow=Image.new('RGBA',canvas.size); dr=ImageDraw.Draw(shadow)
    dr.rectangle((x+10,y+16,x+img.width+10,y+img.height+16),fill=(15,20,22,100))
    canvas.paste(shadow.filter(ImageFilter.GaussianBlur(17)),(0,0),shadow.filter(ImageFilter.GaussianBlur(17)))
    canvas.paste(img,(x,y))
source_info={}
for p in projects:
    slug=p['slug']; m=manifest[slug]; candidates=archives.get(m['source_zip'],[])
    if not candidates: raise RuntimeError('Missing '+m['source_zip'])
    zpath=sorted(candidates,key=lambda x: ('Quality-Reassessment' not in str(x),len(str(x))))[0]
    with zipfile.ZipFile(zpath) as z:
        target=m['source_pdf']; names=z.namelist()
        matches=[n for n in names if n.replace('\\','/').endswith(target.replace('\\','/'))]
        if not matches: matches=[n for n in names if Path(n).name==Path(target).name]
        if len(matches)!=1: raise RuntimeError((slug,target,matches))
        doc=fitz.open(stream=z.read(matches[0]),filetype='pdf')
        n=len(doc)
        if n!=m['source_pdf_pages']: raise RuntimeError((slug,n,m['source_pdf_pages']))
        idx=sorted(set([0,min(1,n-1),min(max(2,n//2),n-1)]))
        imgs=[render(doc[i]) for i in idx]
        folder=d/'assets/approved-2026'/slug
        for i,img in zip(idx,imgs): img.save(folder/f'publication-{i+1:02}.webp','WEBP',quality=86,method=4)
        W,H=1440,960
        bg=Image.new('RGB',(W,H),'#dfded6')
        a=fit(imgs[0],650,825); b=fit(imgs[1] if len(imgs)>1 else imgs[0],680,750)
        paste_shadow(bg,b,(W-65-b.width,(H-b.height)//2+30))
        paste_shadow(bg,a,(65,(H-a.height)//2-20))
        bg.save(folder/'showcase.webp','WEBP',quality=86,method=4)
        source_info[slug]={'pages':n,'width_mm':round(doc[0].rect.width*25.4/72,1),'height_mm':round(doc[0].rect.height*25.4/72,1),'preview_pages':[i+1 for i in idx],'source_zip':m['source_zip'],'source_pdf':m['source_pdf']}
        doc.close()
    print('Rendered',slug,n,flush=True)
put(root/'COMMERCIAL-SOURCE-PREVIEWS.json',json.dumps(source_info,indent=2))
# Explicit deliverable groupings based on the approved project descriptions, not invented client work.
groups={
'Reports & research':('reports','Annual reports, research publications and information-rich documents','calloway brightmoor-solar civic clearwater common-ground distributed-work fernloop quarterly-index'),
'Magazines & journals':('magazines','Editorial publications with considered pacing, typography and imagery','material fieldnotes halftone-garden neighbour slowroad-journal structure table silence-quarterly'),
'Catalogues & lookbooks':('catalogues','Product collections, specifications and visual merchandising','datum hearthwell tolvik thread'),
'Brochures & visitor guides':('brochures','Clear introductions, visitor journeys and practical guides','aldous-pike courtyard fieldnote harbor hollow-pine kiln-cup larkfield linden-court northline open-house stillhouse halvorsen-quill'),
'Brand & layout systems':('identity','Identity guides, packaging concepts and consistent document systems','daily-form gridshift orlathread pattern signal wellspring-next'),
'Workbooks & learning':('workbooks','Readable exercises, prompts and instructional publications','clearpath-coaching make-room')}
# Preserve all 40: verify every project appears exactly once.
group_for={slug:(name,route,desc) for name,(route,desc,slugs) in groups.items() for slug in slugs.split()}
assert set(group_for)=={p['slug'] for p in projects}
by={p['slug']:p for p in projects}
def project_name(p): return p['name'].replace('-',' ')
def imgurl(slug,file='showcase.webp'): return f'/assets/approved-2026/{slug}/{file}'
def service_cards():
    return ''.join(f'<a class="service-card" href="/services/{route}/"><span class="tiny-label">0{i+1} / Service</span><img src="{imgurl(slugs.split()[0])}" alt="" width="1440" height="960" loading="lazy"><h3>{esc(name)}</h3><p>{esc(desc)}</p><span class="text-action">Explore examples &#8599;</span></a>' for i,(name,(route,desc,slugs)) in enumerate(groups.items()))
def common(s):
    s=s.replace('Independent design portfolio</span>','Publication design studio</span>')
    s=s.replace('<strong>KODRYN</strong>','<img class="brand-icon" src="/assets/kodryn-mark.png" width="32" height="32" alt=""><strong>KODRYN</strong>')
    s=re.sub(r'<a href="/#chapters">Disciplines</a><a href="/#approach">Approach</a>', '<a href="/#services">Services</a><a href="/#approach">Approach</a>',s)
    s=re.sub(r'<a class="nav-cta" href="https://www.fiverr.com/kodryn_tech/"[^>]*>.*?</a>','<a class="nav-cta" href="/enquire/">Enquire &#8599;</a>',s)
    s=re.sub(r'<a class="cta-button" href="https://www.fiverr.com/kodryn_tech/"[^>]*>.*?</a>','<a class="cta-button" href="/enquire/">Discuss your project &#8599;</a>',s)
    s=s.replace('<a href="/work/">All work</a><a href="/#chapters">Disciplines</a>','<a href="/work/">All work</a><a href="/#services">Services</a><a href="/enquire/">Enquire</a>')
    return s
for f in d.rglob('*.html'):
    s=common(get(f))
    s=re.sub(r'(/assets/approved-2026/[^/" ]+)/artwork\.webp',r'\1/showcase.webp',s)
    put(f,s)
home=d/'index.html'; s=get(home)
s=s.replace('A collection of design studies / 2026','Independent publication design / 2026')
s=s.replace('Give<br>ideas<br><em>form.</em>','Give ideas<br><em>form.</em>')
s=s.replace('Editorial design, visual identities and information systems for the stories, services and objects people care about.','Editorial and publication design for brands, businesses and organisations. Annual reports, magazines, catalogues and brochures, thoughtfully built in Adobe InDesign.')
s=s.replace('Discover the work','Explore selected work')
s=s.replace('<span class="hero-spec">Independent portfolio / 40 reviewed design studies</span>','<a class="hero-enquire" href="/enquire/">Discuss your project &#8599;</a>')
s=s.replace('width="1440" height="810"','width="1440" height="960"')
s=s.replace('A few to <em>start with.</em>','Selected <em>work.</em>')
s=s.replace('Eight different starting points. Each project has a distinct visual language, purpose and way of telling its story.','Eight self-initiated studies, selected to demonstrate the range of publication design, identity and information systems.')
services='<section id="services" class="shell commercial-section"><div class="section-heading"><div><p class="eyebrow">02 / What Kodryn designs</p><h2>Find your <em>format.</em></h2></div><p>Start with the document you need, then explore relevant work and discuss the scope.</p></div><div class="service-grid">'+service_cards()+'</div></section>'
about='''<section id="studio" class="shell commercial-section"><div class="section-heading"><div><p class="eyebrow">The independent practice</p><h2>Care on <em>every page.</em></h2></div><p>Kodryn focuses on publication systems: typography, page hierarchy, visual direction and clear communication. The portfolio is a collection of self-initiated studies, not a list of commissioned clients.</p></div><div class="commercial-columns"><article><h3>Design and production</h3><p>Adobe InDesign layouts, editable source files and PDF delivery can be scoped for print or screen. Final print specifications, linked assets and usage rights are agreed per project.</p></article><article><h3>A clear working process</h3><p>Brief and content review, visual direction, layout development, consolidated feedback and agreed file handover.</p></article><article><h3>Evidence, not promises</h3><p>Explore forty studies with source-derived publication previews, format specifications and original presentation boards.</p><a class="text-action" href="/work/">View all work &#8599;</a></article></div></section>'''
s=s.replace('<div class="shell strip"', '<div class="shell strip"',1)
pos=s.find('<section',s.find('id="selected"')+1)
# Place services immediately after selected section (before next section).
if pos<0: raise RuntimeError('home insertion')
s=s[:pos]+services+s[pos:]
pos=s.find('<section class="cta-section"')
s=s[:pos]+about+s[pos:]
put(home,s)
# Add factual case study context and source publication views. Original boards and viewer remain.
for p in projects:
    slug=p['slug']; name=project_name(p); f=d/'work'/slug/'index.html'; s=get(f); info=source_info[slug]
    group,route,desc=group_for[slug]
    # All context is derived from approved descriptions; differentiate intended outcome from measured impact.
    detail=f'''<section class="shell commercial-section case-context"><p class="eyebrow">The design brief / Self-initiated study</p><div class="case-grid"><article><h2>Purpose.</h2><p>{esc(p['description'])}</p></article><article><h2>Design direction.</h2><p>Explore the original page compositions below: the cover establishes the visual direction, while the selected interior pages demonstrate how the content is organised across the publication.</p><a class="text-action" href="/services/{route}/">More {esc(group.lower())} &#8599;</a></article><article><h2>Source and format.</h2><dl><dt>Source PDF</dt><dd>{info['pages']} pages / {info['width_mm']:g} × {info['height_mm']:g} mm (first page)</dd><dt>Review edition</dt><dd>Revision {p['revision']:02} / 2026</dd><dt>Context</dt><dd>Illustrative design exercise, not commissioned client work.</dd></dl></article></div><div class="section-heading"><div><p class="eyebrow">Source publication</p><h2>Look <em>closer.</em></h2></div><p>Actual pages rendered from the approved local source PDF, not recreated content. Select a page to view its full image.</p></div><div class="source-pages">'''
    for i in info['preview_pages']:
        url=imgurl(slug,f'publication-{i:02}.webp')
        detail+=f'<figure><a href="{url}" target="_blank" rel="noopener"><img src="{url}" alt="{esc(name)} source publication page {i}" loading="lazy"></a><figcaption>Source page {i:02} / {info["pages"]:02}</figcaption></figure>'
    detail+='</div></section>'
    s=s.replace('<section class="shell detail-body"',detail+'<section class="shell detail-body"',1)
    s=s.replace('href="#case-pages"','href="#case-pages"',1)
    s=s.replace('class="cta-button" href="/enquire/"',f'class="cta-button" href="/enquire/?type={route}"')
    put(f,s)
# Reuse actual header/footer and metadata from homepage for new static routes.
header=re.search(r'<body>.*?<main id="main">',s,re.S).group(0)
footer=re.search(r'</main>.*?</html>',s,re.S).group(0)
def page(route,title,desc,body):
    url='https://kodryn-indesign-portfolio.vercel.app/'+route.strip('/')+'/'
    head=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Kodryn</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><meta property="og:title" content="{esc(title)} | Kodryn"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><link rel="icon" href="/assets/kodryn-mark.png"><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head>'
    put(d/route.strip('/')/'index.html',head+header+body+footer)
for name,(route,desc,slugs) in groups.items():
    tiles=''.join(f'<a class="service-card" href="/work/{slug}/"><img src="{imgurl(slug)}" alt="{esc(project_name(by[slug]))} publication preview" width="1440" height="960" loading="lazy"><h3>{esc(project_name(by[slug]))}</h3><p>{esc(by[slug]["description"])}</p><span class="text-action">View study &#8599;</span></a>' for slug in slugs.split())
    page('services/'+route,name,desc,f'<section class="shell commercial-section"><p class="eyebrow"><a href="/#services">Services</a> / Publication design</p><h1 class="commercial-h1">{esc(name)}.</h1><p class="hero-lead">{esc(desc)}. Explore the relevant self-initiated studies below.</p><a class="hero-enquire" href="/enquire/?type={route}">Discuss this project &#8599;</a><div class="service-grid">{tiles}</div></section>')
options=''.join(f'<option value="{route}">{esc(name)}</option>' for name,(route,_,_) in groups.items())
page('enquire','Discuss your publication','Prepare a clear publication design brief for Kodryn.',f'''<section class="shell commercial-section enquiry"><p class="eyebrow">Start a project / No obligation</p><h1 class="commercial-h1">Let's make<br><em>it readable.</em></h1><p class="hero-lead">Prepare a brief before contacting Kodryn. Your entries stay in this browser and are not sent automatically.</p><div class="enquiry-grid"><form id="brief-form"><label>Publication type<select name="type" required><option value="">Choose a format</option>{options}<option value="other">Other / not sure</option></select></label><label>Estimated page count<input name="pages" placeholder="e.g. 24 pages or not sure"></label><label>Deadline<input name="deadline" type="date"></label><label>Budget range<input name="budget" placeholder="Amount and currency (optional)"></label><label>Required deliverables<select name="format"><option>Not decided</option><option>Screen PDF</option><option>Print PDF</option><option>Editable InDesign and PDF</option><option>Print and screen PDF</option></select></label><label>Content and brand assets<select name="assets"><option>Not yet ready</option><option>Draft content available</option><option>Final content and brand assets ready</option></select></label><label>Tell us about the project<textarea name="notes" rows="5" placeholder="Audience, design goals, references and other requirements"></textarea></label><button type="submit" class="hero-enquire">Prepare my brief</button></form><aside class="brief-preview"><h2>Your next step.</h2><p>Prepare your brief, copy or download it, then share it through the existing Kodryn Fiverr contact channel.</p><textarea id="brief-output" rows="12" readonly aria-label="Prepared project brief" placeholder="Your brief will appear here."></textarea><div class="brief-actions"><button id="copy-brief" type="button" disabled>Copy brief</button><button id="download-brief" type="button" disabled>Download brief</button></div><p id="brief-status" role="status"></p><a class="text-action" href="https://www.fiverr.com/kodryn_tech/" target="_blank" rel="noopener noreferrer">Contact Kodryn on Fiverr &#8599;</a><p class="tiny-label">No payment or submission is made on this page.</p></aside></div></section>''')
# Add alternate deliverable navigation to archive, without disrupting the existing filter.
f=d/'work/index.html'; s=get(f)
links=''.join(f'<a href="/services/{route}/">{esc(name)}</a>' for name,(route,_,_) in groups.items())
s=s.replace('<div class="archive-tools">','<nav class="deliverable-links" aria-label="Browse by deliverable"><span class="tiny-label">Browse by format</span>'+links+'</nav><div class="archive-tools">',1)
put(f,s)
# Extend sitemap for new public pages.
f=d/'sitemap.xml'; s=get(f)
urls=['enquire']+['services/'+v[0] for v in groups.values()]
s=s.replace('</urlset>',''.join('<url><loc>https://kodryn-indesign-portfolio.vercel.app/'+u+'/</loc></url>' for u in urls)+'</urlset>')
put(f,s)
print('Commercial pages complete',flush=True)
