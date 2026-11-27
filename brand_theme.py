from pathlib import Path
import re
p=Path('dist/style.css');s=p.read_text(encoding='utf-8')
# Replace the former warm accents and background neutrals, not any original publication pixel.
mapping={'#eca08a':'#91C785','#f7c9ae':'#91C785','#efab8b':'#91C785','#f0c2ae':'#91C785','#eba790':'#91C785','#d6a38b':'#91C785','#f8c1a5':'#91C785','#f5bb99':'#91C785','#df6d51':'#008C76','#ab422d':'#006B5C','#f0c7b6':'#D9F1E7','#f08e73':'#71D8BF','#743b32':'#194D46','#151c1c':'#031E24','#f4f2ed':'#F3F7F4','#1d2321':'#031E24','#515b55':'#40575B','#5d675f':'#52656D','#cfcfc7':'#C6D7D3','#e8e7df':'#E4EEEA','#202823':'#102C31','#101615':'#071F24','#f1f0e8':'#F3F7F4','#c4cec6':'#D2E4E1','#a9b7af':'#AEC8C5','#45514c':'#42615F','#25302c':'#17383B','#dfded6':'#E1E8E4'}
s=re.sub(r'#[0-9a-fA-F]{6}\b',lambda m:mapping.get(m[0].lower(),m[0]),s)
s+='''
/* Kodryn masterbrand rollout / semantic tokens, shared spacing and interaction. */
:root,:root[data-theme="light"]{color-scheme:light;--paper:#F3F7F4;--surface:#FFFFFF;--ink:#031E24;--soft-ink:#40575B;--muted:#52656D;--line:#C6D7D3;--card:#E4EEEA;--accent:#006B5C;--accent-light:#D9F1E7;--primary:#006B5C;--primary-hover:#005044;--on-primary:#FFFFFF;--focus:#006B5C;--reverse:#031E24;--reverse-ink:#F3F7F4;--reverse-muted:#C5D8D5;--reverse-accent:#91C785;--reverse-line:#35575B;--logo-ink:#031E24;--lime:#70C507;--mint:#91C785;--teal:#008C76;--gutter:clamp(18px,4vw,72px);--section-space:clamp(50px,7vw,108px);--gap:clamp(16px,2.5vw,36px)}
@media(prefers-color-scheme:dark){:root:not([data-theme]){color-scheme:dark;--paper:#071F24;--surface:#102C31;--ink:#F3F7F4;--soft-ink:#D2E4E1;--muted:#AEC8C5;--line:#42615F;--card:#17383B;--accent:#71D8BF;--accent-light:#194D46;--primary:#91C785;--primary-hover:#B5DDAA;--on-primary:#031E24;--focus:#91C785;--logo-ink:#F3F7F4}}
:root[data-theme="dark"]{color-scheme:dark;--paper:#071F24;--surface:#102C31;--ink:#F3F7F4;--soft-ink:#D2E4E1;--muted:#AEC8C5;--line:#42615F;--card:#17383B;--accent:#71D8BF;--accent-light:#194D46;--primary:#91C785;--primary-hover:#B5DDAA;--on-primary:#031E24;--focus:#91C785;--logo-ink:#F3F7F4}
html{scroll-padding-top:112px}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.6}
.shell{padding-inline:var(--gutter);max-width:1600px}
.site-header{height:auto;min-height:84px;max-width:none;width:100%;background:var(--paper);border-bottom:1px solid var(--line);gap:clamp(12px,2vw,30px)}
.brandmark,.site-footer .footer-brand{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:4px;min-width:0;color:var(--logo-ink)}
.brand-logo{width:clamp(136px,16vw,224px);height:auto;display:block;flex:none}
.brandmark span,.site-footer .footer-brand span{font:600 9px/1.2 var(--sans);letter-spacing:.065em;text-transform:uppercase;color:var(--muted);margin:0;display:block;white-space:nowrap}
.site-header .site-nav{gap:clamp(12px,2vw,30px);margin-left:auto;font-weight:600}
.site-nav a{min-height:44px;display:inline-flex;align-items:center;gap:8px}
.ui-icon{display:inline-block;width:1.15em;height:1.15em;vertical-align:-.18em;flex:none;overflow:visible}
.text-action .ui-icon{font-size:16px;transition:transform .18s ease}
.text-action:hover .ui-icon{transform:translate(3px,-1px)}
.nav-cta,.hero-enquire,.cta-button,.brief-actions button:not(:disabled),.archive-filters button[aria-pressed=true]{background:var(--primary);color:var(--on-primary);border:1px solid var(--primary);min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:10px;font-weight:650;transition:background .15s,color .15s,border-color .15s}
.nav-cta:hover,.hero-enquire:hover,.cta-button:hover,.brief-actions button:not(:disabled):hover,.archive-filters button[aria-pressed=true]:hover{background:var(--primary-hover);border-color:var(--primary-hover);color:var(--on-primary)}
.button-secondary{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:11px 16px;border:1px solid var(--line);font-weight:650;color:var(--ink);background:var(--surface)}
.button-secondary:hover,.archive-filters button:not([aria-pressed=true]):hover{background:var(--accent-light);color:var(--accent);border-color:var(--accent)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--focus);outline-offset:4px}
.theme-switcher{display:flex;gap:3px;padding:3px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.theme-switcher select[hidden],.theme-switcher label[hidden]{display:none}
.theme-switcher button{width:40px;height:40px;min-width:40px;min-height:40px;border-radius:5px;color:var(--muted);padding:0}
.theme-switcher button[aria-pressed=true]{background:var(--accent-light);color:var(--accent);border-color:var(--accent)}
.theme-switcher button:hover{color:var(--accent);border-color:var(--accent)}
.hero-stage{background:var(--paper);color:var(--ink)}
.hero-stage-inner{padding-block:clamp(40px,6vw,100px) 32px;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:var(--gap)}
.hero-title{font-size:clamp(50px,5.7vw,86px);line-height:1.04;margin:18px 0 24px;letter-spacing:-.05em;overflow-wrap:normal}
.hero-title em{color:var(--accent);font-size:1.08em}
.hero-left .eyebrow,.hero-art figcaption span:last-child{color:var(--accent)}
.hero-lead{margin:0 0 24px;color:var(--soft-ink);max-width:42ch}
.hero-bottom{gap:12px;align-items:center;justify-content:flex-start;flex-wrap:wrap}
.hero-bottom .hero-enquire{order:-1}
.hero-art-frame{aspect-ratio:8/5;min-height:0;transform:none;background:#E1E8E4;border:1px solid var(--line)}
.hero-art-frame img{filter:none;object-fit:contain;width:100%;height:100%}
.hero-art figcaption,.hero-stat span{color:var(--muted)}
.hero-stat{border-color:var(--line);margin-top:16px;padding-top:12px}
.proof-strip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--gap);padding-block:24px;border-block:1px solid var(--line)}
.proof-strip div{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;min-width:0}
.proof-strip strong{font:800 clamp(24px,3vw,38px)/1.1 var(--brand);color:var(--accent)}
.proof-strip span{color:var(--muted);font-size:13px}
.strip{overflow-x:visible;flex-wrap:wrap;gap:12px 18px}
.commercial-section{padding-block:var(--section-space)}
.section-heading{gap:var(--gap);margin:var(--section-space) 0 32px}
.section-heading h2,.chapters-heading h2,.interlude h2{font-size:clamp(40px,5.3vw,80px);line-height:1.05;letter-spacing:-.04em}
.section-heading p{color:var(--soft-ink)}
.work-mosaic,.collection-grid{gap:var(--gap)}
.mosaic-card .mosaic-picture,.collection-card .collection-visual,.collection-card:first-child .collection-visual,.detail-hero-art{height:auto;min-height:0;aspect-ratio:8/5;background:#E1E8E4;border:1px solid var(--line)}
.mosaic-card .mosaic-picture img,.collection-card .collection-visual img,.detail-hero-art img{object-fit:contain;max-height:none;width:100%;height:100%;filter:none}
.mosaic-card--full{grid-template-columns:1.1fr .9fr}
.mosaic-card--full .mosaic-picture{min-height:0}
.mosaic-card--full .mosaic-info{padding:clamp(22px,4vw,55px)}
.mosaic-card--full .mosaic-label .category,.mosaic-card--full .mosaic-label .series,.mosaic-card--full .description{color:var(--reverse-muted)}
.mosaic-card--full .text-action,.mosaic-card--full h3 a:hover,.ink-section .eyebrow,.chapter-row:hover .chapter-name,.chapter-row:focus-visible .chapter-name,.chapter-summary .num{color:var(--reverse-accent)}
.mosaic-picture::after{content:"";background-color:#F3F7F4;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23031E24' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 18 18 6M8 6h10v10'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:20px;border:1px solid #C6D7D3}
.mosaic-card .mosaic-picture:hover::after,.mosaic-card .mosaic-picture:focus-visible::after{opacity:1}
.service-card{border-top:1px solid var(--line);padding-top:16px;gap:12px}
.service-card img{aspect-ratio:8/5;object-fit:contain;background:#E1E8E4;border:1px solid var(--line)}
.service-card:hover h3,.mosaic-card:not(.mosaic-card--full) h3 a:hover,.collection-card:hover h3{color:var(--accent)}
.service-card .text-action,.case-grid .text-action{color:var(--accent)}
.ink-section,.mosaic-card--full,.cta-section{background:var(--reverse);color:var(--reverse-ink)}
.ink-section{padding-block:var(--section-space)}
.ink-section .chapters-heading p,.chapter-summary,.chapter-index{color:var(--reverse-muted)}
.chapter-row,.chapter-row:last-child{border-color:var(--reverse-line)}
.chapter-thumb img{object-fit:contain}
.cta-section .tiny-label,.cta-section h2 em{color:var(--reverse-accent)}
.cta-section p{color:var(--reverse-muted)}
.cta-inner{padding-block:var(--section-space);align-items:center;gap:var(--gap)}
.cta-inner h2{font-size:clamp(48px,6.8vw,100px);line-height:1.02}
.cta-section .cta-button{background:#91C785;color:#031E24;border-color:#91C785}
.cta-section .cta-button:hover{background:#B5DDAA;color:#031E24;border-color:#B5DDAA}
.site-footer{gap:var(--gap);align-items:start;padding-block:36px}
.footer-nav{flex-wrap:wrap;gap:8px 18px}
.footer-nav a{min-height:32px;display:inline-flex;align-items:center}
.site-footer .footer-brand .brand-logo{width:180px}
.faq details{padding:18px 0;border-top:1px solid var(--line);max-width:920px}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{font:700 clamp(18px,2vw,23px)/1.4 var(--brand);cursor:pointer;color:var(--ink)}
.faq details p{color:var(--soft-ink);max-width:70ch}
.enquiry-route{margin-top:24px;display:flex;align-items:center;flex-wrap:wrap;gap:14px}
.enquiry-route p{margin:0;color:var(--muted);font-size:14px}
.enquiry input,.enquiry textarea,.enquiry select,.search input{background:var(--surface);color:var(--ink);border:1px solid var(--line);min-height:44px}
.enquiry form{gap:18px}
.brief-preview{background:var(--card);border:1px solid var(--line)}
.brief-actions button{min-height:44px}
.case-nav{display:flex;flex-wrap:wrap;gap:12px 18px;border-block:1px solid var(--line);padding-block:14px;margin-top:24px}
.case-nav a{display:inline-flex;align-items:center;min-height:36px;color:var(--accent);font-weight:600}
.case-grid{gap:var(--gap)}
.case-grid article{min-width:0}
.case-grid h2{font-size:clamp(24px,2.5vw,38px)}
.case-grid h3{font-size:16px;color:var(--accent)}
.source-pages{grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--gap)}
.source-pages button{display:grid;place-items:center;width:100%;padding:12px;border:1px solid var(--line);background:#E1E8E4;min-height:180px}
.source-pages img{height:auto;width:auto;max-width:100%;max-height:660px;object-fit:contain}
.source-pages figcaption{display:flex;justify-content:space-between;gap:12px;align-items:center}
.detail-board button{background:#E1E8E4;border:1px solid var(--line)}
.detail-next a:hover{color:var(--accent)}
.viewer-controls button{min-width:44px;min-height:44px}
.viewer-controls .ui-icon{width:20px;height:20px}
.viewer{max-width:calc(100vw - 24px);max-height:calc(100dvh - 24px)}
.viewer-img{max-height:calc(100dvh - 155px);object-fit:contain}
.case-conversion{margin-block:30px;display:flex;gap:var(--gap);align-items:center;justify-content:space-between;padding:clamp(20px,4vw,42px);background:var(--card);border:1px solid var(--line)}
.case-conversion h2{font-size:clamp(24px,3vw,38px);line-height:1.1;margin:0 0 10px}
.case-conversion p{max-width:58ch;color:var(--soft-ink);margin:0}
.case-conversion a{flex:none}
@media(max-width:1024px){.brand-logo{width:174px}.site-header .site-nav{gap:14px}.theme-switcher button{width:36px;min-width:36px;height:36px;min-height:36px}.hero-title{font-size:clamp(45px,6.3vw,74px)}}
@media(max-width:820px){.site-header{min-height:0;padding-block:12px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px 12px}.site-header .brandmark{grid-column:1;grid-row:1}.site-header .theme-switcher{grid-column:2;grid-row:1}.site-header .site-nav{grid-column:1/-1;grid-row:2;margin:0;justify-content:space-between;gap:10px}.hero-stage-inner{grid-template-columns:1fr;gap:26px}.hero-title{font-size:clamp(48px,9.2vw,76px);max-width:14ch}.proof-strip{gap:14px}.proof-strip div{display:grid;gap:5px}.case-conversion{flex-wrap:wrap}.site-footer{grid-template-columns:1fr 1fr}.site-footer .footer-note{grid-column:1/-1;justify-self:start;text-align:left}}
@media(max-width:580px){:root{--gutter:18px;--section-space:48px}.site-header .site-nav a{font-size:13px;min-height:44px;gap:4px}.site-header .nav-cta{padding:8px 10px}.site-header .brand-logo{width:155px}.brandmark span{font-size:8px}.theme-switcher button{width:34px;min-width:34px;height:36px;min-height:36px}.hero-title{font-size:clamp(39px,11.8vw,58px);margin:14px 0 18px;max-width:16ch}.hero-title em{font-size:1em}.hero-lead{font-size:16px;line-height:1.65}.hero-bottom .text-action{padding:9px 0}.hero-bottom .hero-enquire{min-height:48px}.hero-art figcaption{gap:6px;font-size:10px}.hero-stat{gap:8px}.proof-strip{grid-template-columns:1fr;gap:14px}.proof-strip div{display:flex;align-items:baseline;gap:10px}.strip{display:none}.section-heading{margin-bottom:22px}.section-heading h2,.chapters-heading h2,.interlude h2{font-size:clamp(36px,10vw,54px)}.mosaic-card--full{display:block}.mosaic-card .mosaic-picture,.mosaic-card--full .mosaic-picture{height:auto;aspect-ratio:8/5}.mosaic-label{gap:8px;flex-wrap:wrap}.service-grid,.source-pages,.site-footer{grid-template-columns:1fr}.site-footer .footer-note{grid-column:auto}.site-footer .footer-nav{justify-content:flex-start}.cta-inner{grid-template-columns:1fr}.cta-inner h2{font-size:clamp(42px,12vw,66px)}.case-grid{margin-bottom:35px}.source-pages button{min-height:120px}.case-conversion a{width:100%}.archive-hero h1,.commercial-h1,.collection-title,.detail-h1{overflow-wrap:anywhere}.detail-next{gap:12px}.viewer-controls{gap:6px}.viewer-controls button{min-width:36px;min-height:44px}.brief-preview{padding:15px}.enquiry-route .button-secondary{width:100%}}
@media(max-width:350px){:root{--gutter:14px}.site-header .brand-logo{width:140px}.brandmark span{font-size:7px}.site-header .site-nav{gap:6px}.site-header .site-nav a{font-size:12px}.theme-switcher button{width:30px;min-width:30px}.hero-title{font-size:39px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation-duration:.01ms!important;transition-duration:.01ms!important}}
'''
p.write_text(s,encoding='utf-8')
print('Semantic theme and responsive CSS complete')
