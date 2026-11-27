from pathlib import Path
import urllib.request
from fontTools.ttLib import TTFont
p=Path('dist/fonts')
sources={'inter':'https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2','manrope':'https://fonts.gstatic.com/s/manrope/v23/xn7gYHE41ni1AdIRggexSg.woff2'}
for name,url in sources.items():
 f=p/(name+'-latin.woff2'); f.write_bytes(urllib.request.urlopen(url,timeout=20).read())
 font=TTFont(f); print(name,[(a.axisTag,a.minValue,a.maxValue) for a in font['fvar'].axes])
 assert any(a.axisTag=='wght' and a.minValue<=400 and a.maxValue>=700 for a in font['fvar'].axes)
for name in ['inter','manrope','instrumentserif']:
 (p/(name+'-OFL.txt')).write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/google/fonts/main/ofl/'+name+'/OFL.txt',timeout=20).read())
f=Path('dist/style.css'); css=f.read_text(encoding='utf-8')
css+='''
/* Kodryn approved brand typography v1.1 */
@font-face{font-family:Manrope;src:url('/fonts/manrope-latin.woff2') format('woff2');font-weight:200 800;font-style:normal;font-display:swap}
@font-face{font-family:Inter;src:url('/fonts/inter-latin.woff2') format('woff2');font-weight:100 900;font-style:normal;font-display:swap}
:root{--sans:Inter,'Segoe UI',Arial,sans-serif;--brand:Manrope,Inter,'Segoe UI',Arial,sans-serif;--serif:Instrument,Georgia,serif}
body{font-family:var(--sans)}
h1,h2,h3,h4,.brandmark strong,.footer-brand,.hero-title,.commercial-h1,.commercial-subhead{font-family:var(--brand);font-weight:700;letter-spacing:-.035em}
.hero-title{font-weight:800;font-size:clamp(56px,6.5vw,96px);line-height:1.03;letter-spacing:-.045em}
h1 em,h2 em,h3 em,.hero-title em,.commercial-h1 em{font-family:var(--serif);font-weight:400;font-style:italic;letter-spacing:-.015em}
.detail-h1,.collection-title,.archive-hero h1,.commercial-h1{font-weight:800}
.site-nav,.theme-switcher,button,input,textarea,select,.text-action,.hero-enquire,.cta-button{font-family:var(--sans)}
.eyebrow,.tiny-label{font-family:var(--sans);font-weight:600}
.mosaic-info h3,.service-card h3,.commercial-columns h3,.case-grid h2,.brief-preview h2{font-family:var(--brand);font-weight:700;font-size:clamp(25px,2.8vw,38px);line-height:1.15}
.chapter-name{font-family:var(--serif);font-weight:400}
@media(max-width:820px){.hero-title{font-size:clamp(54px,10vw,88px)}}
@media(max-width:580px){.hero-title{font-size:clamp(48px,12vw,68px)}.site-nav{gap:8px}.brandmark strong{font-size:21px}.section-heading h2,.chapters-heading h2,.interlude h2{font-size:clamp(36px,10vw,58px)}.commercial-h1,.detail-h1,.collection-title,.archive-hero h1{font-size:clamp(38px,11vw,65px);overflow-wrap:anywhere}}
'''
f.write_text(css,encoding='utf-8')
print('Typography CSS and fonts ready')
