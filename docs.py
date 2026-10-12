import json, build
from lib import *
v = json.load(open("validation.json"))
wc = v["wc"]; inb = v["inbound"]; outb = v["outbound"]
f = lambda s: "index.html" if s == "index" else s + ".html"
U = lambda s: SITE + ("/" if s == "index" else f"/{s}.html")

SUP = [("tractor wala game","index","Homepage hub; primary keyword"),("wala game tractor wala game","index","Natural-language variant; consolidated"),
("tractor wala game tractor wala game","index","Repetition variant; consolidated"),("game tractor wala game","index","Word-order variant; consolidated"),
("game tractor wala","index","Word-order variant; consolidated"),("tractor wala game video","tractor-wala-game-video","Video/gameplay intent"),
("tractor trali wala game","tractor-trolley-wala-game","Spelling variant of trolley; consolidated"),
("tractor wala game download apk","tractor-wala-game-apk-guide","APK safety intent"),("tractor wala game download","tractor-wala-game-download","Safe download intent"),
("tractor wala game tractor wala","index","Repetition variant; consolidated"),("tractor wala game dikhaiye","tractor-wala-game-dikhaiye","Discovery methods"),
("tractor wala game chahie","tractor-wala-game-chahie","Needs-based choice"),("tractor wala game dikhao","tractor-wala-game-dikhao","Reading gameplay visuals"),
("tractor ka game","tractor-ka-game","Plain-language orientation"),("real tractor game","real-tractor-game","Realism intent"),
("tractor simulator game","tractor-simulator-game","Genre explainer"),("tractor games 3d","tractor-games-3d","3D graphics/performance"),
("tractor game tractor game","tractor-ka-game","Repetition variant; consolidated into generic tractor-game page"),
("tractor wali game","tractor-wali-game","Mixed-genre tractor involvement"),("truck wala game","truck-wala-game","Adjacent vehicle intent"),
("indian tractor games","indian-tractor-games","Indian-setting intent"),("tractor wale game","tractor-wale-games","Plural/collection browsing")]
km = ["# Keyword Map\n", "All keyword research here is **qualitative**. Search volume, keyword difficulty, ranking position, competitor and backlink metrics are **unverified / not collected**. Validate with Google Search Console and a keyword tool before relying on any priority.\n",
"## 1. Supplied keywords to target URL\n", "| Supplied keyword | Target URL | Handling |", "|---|---|---|"]
km += [f"| {k} | {U(s)} | {n} |" for k, s, n in SUP]
km += ["\nVariants that mean the same thing (repeated phrases, word order, wala/wale/wali spellings, trali/trolley) were **consolidated** rather than given separate near-duplicate pages. Where the brief required separate pages (wali, wale, ka, dikhaiye, chahie, dikhao), each was given a distinct purpose: wali = how central the tractor is in mixed games; wale = genre-by-genre shortlist building; ka = plain-language category map; dikhaiye = discovery methods; chahie = needs-based choice; dikhao = reading screenshots and footage.\n",
"## 2. Page-level mapping\n", "| URL | SEO title | Primary keyword | Secondary keywords | Search intent | Content purpose | Key internal links in |", "|---|---|---|---|---|---|---|"]
km.append(f"| {U('index')} | Tractor Wala Game: Tractor Simulator and 3D Farming Guides | tractor wala game | wala game tractor wala game, game tractor wala, tractor wale game | Navigational / informational hub | Homepage linking to every category and guide | all pages (header/footer) |")
for s in ORDER:
    p = PAGES[s]
    km.append(f"| {U(s)} | {p['title']} | {p['kw']} | {', '.join(p['kws'][1:] or ['-'])} | {p['intent']} | {p['purpose'] or p['summary'][:70]} | {len(inb[f(s)])} pages |")
open("out/keyword-map.md", "w").write("\n".join(km) + "\n")

ci = ["# Content Inventory\n", f"Generated from the built HTML on {BUILD_DATE}. Counts are unique internal pages linking in/out (header, footer and breadcrumb links included). Word counts cover text inside `<main>`.\n",
"| URL | Type | Words | Inbound | Outbound | Outbound targets |", "|---|---|---|---|---|---|"]
for s in ["index"] + ORDER:
    t = "Home" if s == "index" else PAGES[s]["cat"]
    ci.append(f"| /{'' if s=='index' else s+'.html'} | {t} | {wc[f(s)]} | {len(inb[f(s)])} | {len(outb[f(s)])} | {', '.join(x.replace('.html','') for x in outb[f(s)] if x not in ('index.html','about.html','contact.html','editorial-policy.html','privacy-policy.html','disclaimer.html','game-guides.html','download-guides.html','gameplay-guides.html','tractor-game-faqs.html','tractor-game-glossary.html'))[:300]} |")
ci.append("| /404.html | Error page (noindex) | - | - | - | home, popular guides, hubs |")
ci.append(f"\nTotal words across indexable pages: {sum(wc.values())}. Orphan pages: none (checked by `validate.py`).")
open("out/content-inventory.md", "w").write("\n".join(ci) + "\n")

r = v["res"]
rep = [f"# SEO Validation Report\n", f"Run date: {BUILD_DATE}. All results below come from `validate.py` (Python, standard library only) executed against the files in this repository. Nothing here was measured in a browser or by an external service.\n",
"## A. Tests actually completed (automated, static)\n"] + [f"- PASS: {m}" for m in r["pass"]]
rep += ["\nSummary: **%d passed, %d failed, %d warnings** in the final run.\n" % (len(r["pass"]), len(r["fail"]), len(r["warn"])),
"## B. Issues found\n",
"1. First run reported 39 failures (\"absolute internal link\"). Cause: a bug in the validator, which treated each page's own `<link rel=canonical>` as an internal anchor. The pages themselves were correct.",
"2. Hub page `download-guides.html` is short (about 430 words) because it is a navigation hub; the validator flagged it as thin. It is a link hub, not an article.",
"3. **Content depth limit (not auto-fixable):** the 30 guide articles run roughly 600 to 900 words each (about 26,000 words across the site), below the 1,000 to 1,800 range suggested in the brief. They were written to avoid padding. Expand them where you have real first-hand material (screenshots, tested devices, verified official links).",
"4. **No real screenshots, videos or verified official download links exist yet.** The site deliberately names no specific game, embeds no video and links to no downloads.\n",
"## C. Issues fixed\n",
"- Validator bug in (1) corrected; re-run produced 0 failures.",
"- Hub-page warning in (2) accepted as intended (hub pages excluded from the thin-content threshold).\n",
"## D. Tests that still require a browser or external service (NOT done)\n",
"- Visual rendering on real phones and desktops, including the mobile menu toggle and the guide filter (JavaScript logic was written but not executed in a browser)",
"- Lighthouse / PageSpeed Insights and Core Web Vitals (no score is claimed)",
"- Google Rich Results Test and Schema.org validator for structured data (only JSON syntax and FAQ-text consistency were checked)",
"- Colour-contrast and screen-reader testing (palette chosen for contrast, but not measured)",
"- Live GitHub Pages deployment, HTTPS and 404 behaviour on the real domain",
"- Google Search Console: property, verification, sitemap submission, indexing status (none of this has been done)",
"- External link health (only external link: the GitHub issues URL on the contact page)\n",
"## E. Configuration notes\n",
"- No Google verification file or meta tag is included; add yours after creating the Search Console property.",
"- `contact.html` contains the placeholder **[ADD YOUR CONTACT EMAIL HERE]**. Replace it or delete the line.",
"- Sitemap `lastmod` is the build date, %s, for every page." % BUILD_DATE]
open("out/SEO-validation-report.md", "w").write("\n".join(rep) + "\n")

n = len(ORDER) + 1
rd = f'''# Tractor Wala Game (static website)

Production URL: {SITE}/
Repository: {REPO}

An independent guide site about tractor games: simulators, 3D and Indian tractor games, trolley play, safe downloads and gameplay. Plain HTML, CSS and a small amount of vanilla JavaScript. No build step, backend, database, tracker or external request is needed to run it.

## Contents

- `index.html` plus **{n-1}** other indexable pages: 3 hubs, 30 guides, 5 trust pages; and `404.html`
- `assets/css/style.css`, `assets/js/main.js`, `assets/images/` (generic illustration, OG image, icon)
- `robots.txt`, `sitemap.xml` ({n} URLs), favicon files, `.nojekyll`
- `keyword-map.md`, `content-inventory.md`, `SEO-validation-report.md`

URL convention: flat, lowercase, hyphenated `.html` files in the repository root (for example `/tractor-simulator-game.html`). This keeps relative links and asset paths reliable on GitHub Pages with no rewrite rules. `404.html` uses root-relative paths because GitHub Pages serves it at any broken URL.

## Deploy to GitHub Pages

1. Unzip the project. Deploy only the contents of the `site/` folder; they must sit at the **root** of the repository (`index.html` next to `robots.txt`), not inside a subfolder. The `generator/` folder is optional tooling and should stay out of the repository.
2. Copy them into a local clone of `{REPO}`, or upload them through the GitHub web interface.
3. Commit and push to the default branch (`main`).
4. In the repository, open **Settings > Pages**. Under **Build and deployment**, set **Source: Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
5. Wait a few minutes, then open {SITE}/ and {SITE}/does-not-exist (to see the 404 page).
6. The repository must be named exactly `tractorwalagame.github.io` for the root URL to work.

The `.nojekyll` file tells GitHub Pages to serve files as they are. The `.md` documents in the root will also be publicly viewable; move them to a private place if you do not want that.

## Before you publish: checklist

- Replace the contact email placeholder in `contact.html`.
- Read every page and correct anything you cannot stand behind. No game is named and no download is linked on purpose; add verified details only with an official source and a date.
- Add real screenshots or video only if you own them or have permission; then add `alt`, `width` and `height`.

## Google Search Console

Nothing has been configured. To do it yourself:

1. Open Search Console and choose **Add property**. A **URL-prefix** property for `{SITE}/` is the simplest for a github.io site.
2. Verify ownership. For GitHub Pages the easiest options are the **HTML tag** (paste the meta tag into the `<head>` of `index.html`) or **HTML file** (upload the file to the repo root).
3. Open **Sitemaps** and submit `sitemap.xml`.
4. Use **URL Inspection** on the homepage and a few guides; look at the indexing status and the user-declared versus Google-selected canonical.
5. Use **Request indexing** sparingly; it does not guarantee inclusion.
6. Monitor **Pages** (indexing report) for reasons pages are excluded, **Performance** for queries, clicks and impressions, and **Core Web Vitals** and **Page experience** once data exists.
7. Fix crawl or rendering problems that Search Console reports, then use **Validate fix**.

Indexing and ranking are decided by Google. This project makes no promise of rankings, speed of indexing or traffic.

## Maintaining the content

Page content is generated from the Python source in the ZIP's `generator/` folder (`content/*.py`, `build.py`; run `python3 build.py && python3 validate.py && python3 docs.py`). If you only edit HTML directly, remember to update `sitemap.xml`, canonical tags and `content-inventory.md` together. To add a page: create the HTML file, copy an existing page's head and footer, set a unique title, description and canonical, link to it from a hub and from at least two related guides, and add it to `sitemap.xml`.

## Honest limits

- Articles are original but modest in length (roughly 600 to 900 words each).
- No keyword volume, difficulty or ranking data was collected.
- Performance, accessibility and structured-data tests in browsers or external tools have not been run; see `SEO-validation-report.md`.
'''
open("out/README.md", "w").write(rd)
print("docs ok", n)
