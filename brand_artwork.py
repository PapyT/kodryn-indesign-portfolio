from pathlib import Path
import json,zipfile,io
from PIL import Image,ImageFilter,ImageDraw
import pymupdf as fitz
root=Path(__file__).parent; d=root/'dist'
manifest=json.loads((root/'COMMERCIAL-SOURCE-PREVIEWS.json').read_text(encoding='utf-8'))
delivery=Path.home()/'Downloads/Telegram Desktop/Extracted-Portfolio-Windows/Approved-Portfolio/05-Design-Upgrade-In-Progress/DELIVERY'
zips={}
for z in delivery.rglob('*.zip'):
 if 'SUPERSEDED' not in str(z):zips.setdefault(z.name,[]).append(z)
def render(p,cap=1800):
 m=cap/max(p.rect.width,p.rect.height)
 pix=p.get_pixmap(matrix=fitz.Matrix(m,m),alpha=False)
 return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
def fit(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS);return im
def place(bg,im,x,y):
 sh=Image.new('RGBA',bg.size);ImageDraw.Draw(sh).rectangle((x+10,y+14,x+im.width+10,y+im.height+14),fill=(0,20,25,80));sh=sh.filter(ImageFilter.GaussianBlur(13));bg.paste(sh,(0,0),sh);bg.paste(im,(x,y))
for slug,m in manifest.items():
 candidates=zips[m['source_zip']]
 path=sorted(candidates,key=lambda x:('Quality-Reassessment' not in str(x),len(str(x))))[0]
 with zipfile.ZipFile(path) as z:
  target=m['source_pdf']; names=[n for n in z.namelist() if n.replace('\\','/').endswith(target.replace('\\','/'))]
  if not names:names=[n for n in z.namelist() if Path(n).name==Path(target).name]
  assert len(names)==1
  doc=fitz.open(stream=z.read(names[0]),filetype='pdf')
  n=len(doc);assert n==m['pages']
  # Image area is a selection heuristic, not an artistic quality score.
  def score(i):
   p=doc[i]; area=p.rect.get_area(); images=p.get_image_info()
   coverage=sum(min(area,fitz.Rect(x['bbox']).get_area()) for x in images)/area
   return min(1,coverage)+min(.25,len(p.get_drawings())*.012)
  eligible=list(range(1,n))
  chosen=max(eligible,key=score) if eligible else 0
  pair=[chosen]
  if n>2:
   second=max([i for i in eligible if i!=chosen],key=lambda i:score(i)+(.15 if abs(i-chosen)==1 else 0));pair.append(second)
  folder=d/'assets/approved-2026'/slug
  cover=render(doc[0]); images=[render(doc[i]) for i in pair]
  for i,im in zip(pair,images):im.save(folder/f'publication-{i+1:02}.webp','WEBP',quality=86,method=3)
  # Two-page proof composition, not a claim of a physical print photograph.
  wide=cover.width>cover.height
  bg=Image.new('RGB',(1600,1000), '#e1e8e4' if not wide else '#dce4e2')
  if wide:
   a=fit(cover,760,900);b=fit(images[0],760,900);place(bg,a,30,(1000-a.height)//2-20);place(bg,b,810,(1000-b.height)//2+20)
  else:
   a=fit(cover,675,900);b=fit(images[0],780,875);place(bg,a,45+(675-a.width)//2,(1000-a.height)//2);place(bg,b,755+(780-b.width)//2,(1000-b.height)//2)
  bg.save(folder/'feature.webp','WEBP',quality=86,method=3)
  m['feature_pages']=[i+1 for i in pair]
  m['preview_pages']=sorted(set(m['preview_pages']+m['feature_pages']))
  doc.close()
 print(slug,m['feature_pages'],flush=True)
(root/'COMMERCIAL-SOURCE-PREVIEWS.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('40 feature compositions ready',flush=True)
