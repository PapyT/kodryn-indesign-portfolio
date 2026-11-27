from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
d=Path('dist')
class Audit(HTMLParser):
 def __init__(self): super().__init__(); self.refs=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1': self.h1+=1
  if 'id' in a: self.ids.append(a['id'])
  for k in ['href','src','data-board-src','data-image']:
   if k in a: self.refs.append(a[k])
pages=list(d.rglob('*.html')); broken=[]; dup=[]; headings=[]; total=0
for f in pages:
 a=Audit();a.feed(f.read_text(encoding='utf-8'))
 if len(a.ids)!=len(set(a.ids)): dup.append(str(f))
 if a.h1!=1:headings.append((str(f),a.h1))
 for ref in a.refs:
  if not ref.startswith('/') or ref.startswith('//'):continue
  u=urlsplit(ref); p=d/unquote(u.path).lstrip('/')
  if p.is_dir():p=p/'index.html'
  total+=1
  if not p.is_file():broken.append((str(f),ref))
  elif u.fragment and p.suffix=='.html':
   b=Audit();b.feed(p.read_text(encoding='utf-8'))
   if u.fragment not in b.ids:broken.append((str(f),ref))
report={'pages':len(pages),'internal_references':total,'broken':broken,'duplicate_ids':dup,'unexpected_h1':headings,'source_projects':len(json.loads(Path('COMMERCIAL-SOURCE-PREVIEWS.json').read_text(encoding='utf-8')))}
Path('COMMERCIAL-STATIC-QA.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2));assert not broken and not dup and not headings
