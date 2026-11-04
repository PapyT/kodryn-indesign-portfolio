# Kodryn — Editorial & Publication Design Portfolio

A curated, responsive portfolio for **40 approved self-initiated design studies**, with a clear emphasis on art direction, publication craft, image scale and editorial hierarchy.

## Information architecture

| Route | Purpose |
| --- | --- |
| `/` | Original editorial landing page with a featured project, eight mixed-size selected works, six discipline chapters, design approach and contact |
| `/disciplines/{slug}/` | Six carefully sectioned collections with distinct introductions and varied-scale project previews |
| `/work/` | Searchable and filterable typographic index of all 40 projects with hover/focus previews |
| `/work/{slug}/` | Forty case-study pages using publication artwork, in-depth board images and category-aware navigation |
| `/downloads/form-and-function-40-projects-2026.pdf` | The verified 132-page master portfolio PDF |

The project has **40 art-directed publication mockups** rendered from approved final source PDFs, with originals and provenance recorded in `EDITORIAL-ARTWORK-SOURCE-MANIFEST.json`. All 120 existing three-board presentation images are retained for detailed viewing.

## Local preview and tests

The site is static, without build dependencies:

```bash
python -m http.server 8877 --directory dist
```

Open http://localhost:8877.

Quality gates include verified internal links, source-image references, responsive layouts at 390 / 768 / 1450 px, project filtering, keyboard gallery navigation, dark-mode handling, and all 40 project URLs. Automated QA reports and local screenshots are maintained on PAPY-T.

## Deployment

Repository: `PapyT/kodryn-indesign-portfolio`. Hosting: Vercel, static output directory `dist`, framework Other. Non-production branches create preview builds; changes are merged into main only after QA.

## Creative references and originality

Design research covered DAC Studios (curated work), Actual Source (typographic archive), Studio Feixen (discipline grouping), and Pentagram's editorial design practice (large artwork and discipline-led narratives). The implementation, markup, styling, content structure, and presentation treatment are original; no reference site's source code or portfolio artwork was copied.

## Content and licensing boundaries

Every featured project is a **self-initiated or illustrative design study**. Project review and file portability do not constitute physical printer signoff, external client approval, real-world financial/research results, or independent commercial rights clearance for every source photograph.

Contact CTA retains the previously configured Kodryn Fiverr profile.
