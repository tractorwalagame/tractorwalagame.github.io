import json, re, os, shutil, html
from lib import *
import content.a, content.b, content.c, content.d

OUT = "out"
HUBS = {"game-guides": "guides", "download-guides": "download", "gameplay-guides": "gameplay"}
CAT2HUB = {v: k for k, v in HUBS.items()}
NAV = [("index", "Home"), ("game-guides", "Game Guides"), ("download-guides", "Download Guides"),
       ("gameplay-guides", "Gameplay Guides"), ("tractor-game-faqs", "FAQs"), ("about", "About")]
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="12" fill="#2e7d3c"/><rect x="14" y="26" width="26" height="14" rx="3" fill="#b9e08f"/><rect x="36" y="31" width="16" height="9" rx="2" fill="#b9e08f"/><rect x="18" y="16" width="14" height="14" rx="2" fill="#e0a82e"/><circle cx="21" cy="42" r="10" fill="#fff"/><circle cx="21" cy="42" r="4" fill="#12301d"/><circle cx="46" cy="44" r="6" fill="#fff"/></svg>'

def url(slug): return SITE + "/" if slug == "index" else f"{SITE}/{slug}.html"
def href(slug, base=""): return (base + "./" if base == "" else "/") if slug == "index" else f"{base}{slug}.html"
def A(slug, text, base=""): return f'<a href="{href(slug, base)}">{text}</a>'

def short(p, n=150):
    s = p["summary"].replace('"', "")
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"

def head(title, desc, canon, schema, base="", noindex=False, og_type="article"):
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    canon_tag = "" if noindex else f'<link rel="canonical" href="{canon}">\n'
    ogu = f'<meta property="og:url" content="{canon}">\n' if not noindex else ""
    img = f"{SITE}/assets/images/og-tractor-wala-game.png"
    sch = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in schema)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}{canon_tag}<meta name="theme-color" content="#12301d">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
{ogu}<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Tractor Wala Game logo artwork with a green tractor on a ploughed field">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{base}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<script>document.documentElement.className+=' js';</script>
<link rel="stylesheet" href="{base}assets/css/style.css">
{sch}</head>
'''

def header(cur, base=""):
    items = "".join(f'<li><a href="{href(s, base)}"{" aria-current=\"page\"" if s == cur else ""}>{t}</a></li>' for s, t in NAV)
    return f'''<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="{href("index", base)}" aria-label="{NAME} home">{LOGO}<span>{NAME}</span></a>
<button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav class="nav" id="site-nav" aria-label="Main"><ul>{items}</ul></nav>
</div></header>
'''

def footer(base=""):
    L = lambda s: f"<li>{A(s, PAGES[s]['nav'] if s != 'index' else 'Home', base)}</li>"
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><h2>{NAME}</h2><p>An independent guide to tractor games, safe downloads and gameplay. We do not host or distribute game files.</p></div>
<div><h2>Explore</h2><ul><li>{A("index","Home",base)}</li>{L("game-guides")}{L("download-guides")}{L("gameplay-guides")}{L("tractor-game-glossary")}</ul></div>
<div><h2>Site information</h2><ul>{L("about")}{L("contact")}{L("editorial-policy")}{L("privacy-policy")}{L("disclaimer")}</ul></div>
</div>
<p class="legal">Game and brand names belong to their owners. This site is not affiliated with any game developer. Information is general guidance; verify details on official sources.</p>
</div></footer>
<script src="{base}assets/js/main.js" defer></script>
</body>
</html>
'''

def crumbs(items):
    lis = "".join(f'<li>{A(s, t) if s else t}</li>' if s else f'<li aria-current="page">{t}</li>' for s, t in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def bc_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": url(s)} if s else {"item": None})}
        for i, (s, t) in enumerate(items)]}

def clean_bc(s):
    for el in s["itemListElement"]:
        if el.get("item") is None: el.pop("item", None)
    return s

def card(slug, big=False):
    p = PAGES[slug]
    return (f'<article class="card{" big" if big else ""}" data-guide="{html.escape((p["nav"]+" "+p["summary"]+" "+" ".join(p["kws"])).lower())}">'
            f'<h3>{A(slug, esc(p["nav"]))}</h3><p>{esc(short(p))}</p></article>')

PUB = {"@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/images/icon-512.png", "width": 512, "height": 512}}
def pub_ref(): return {"@id": SITE + "/#org"}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs, title="Frequently asked questions"):
    if not faqs: return ""
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">{title}</h2>' + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faqs) + "</section>"

def page_file(slug): return "index.html" if slug == "index" else slug + ".html"

def write(name, txt):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(txt)

# ---------- generic page ----------
def build_page(slug):
    p = PAGES[slug]; cat = p["cat"]
    body, toc = render_body(p["body"])
    if cat == "hub":
        trail = [("index", "Home"), (None, p["nav"])]
        kids = [s for s in ORDER if PAGES[s]["cat"] == HUBS[slug]]
        body += f'<h2 id="all-guides">All {esc(p["nav"].lower())}</h2><div class="grid">' + "".join(card(s) for s in kids) + "</div>"
        toc.append(("all-guides", f"All {p['nav'].lower()}"))
        schema_type = "CollectionPage"
    elif cat == "trust":
        trail = [("index", "Home"), (None, p["nav"])]; schema_type = {"about": "AboutPage", "contact": "ContactPage"}.get(slug, "WebPage")
    else:
        hub = CAT2HUB[cat]; trail = [("index", "Home"), (hub, PAGES[hub]["nav"]), (None, p["nav"])]; schema_type = "Article"
    c = url(slug)
    page = {"@context": "https://schema.org", "@type": schema_type, "@id": c + "#page", "url": c,
            "name": p["h1"], "description": p["desc"], "inLanguage": "en", "isPartOf": {"@id": SITE + "/#website"}}
    if schema_type == "Article":
        page.update({"headline": p["h1"], "mainEntityOfPage": c, "publisher": pub_ref(), "author": pub_ref()})
        page.pop("name")
    schemas = [page, clean_bc(bc_schema(trail))]
    if p["faqs"] and cat not in ("trust",): schemas.append(faq_schema(p["faqs"]))
    h = head(p["title"], p["desc"], c, schemas)
    related = [r for r in p["related"] if r != slug]
    rel_html = ""
    if related:
        rel_html = '<section aria-labelledby="rel-h"><h2 id="rel-h">Related guides</h2><div class="grid">' + "".join(card(r) for r in related) + "</div></section>"
    tochtml = ""
    if len(toc) > 1:
        tochtml = '<nav class="toc" aria-labelledby="toc-h"><h2 id="toc-h">On this page</h2><ul>' + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ul></nav>"
    parent = ""
    if cat in CAT2HUB:
        hub = CAT2HUB[cat]
        parent = f'<div class="box"><h2>More in this section</h2><p>{A(hub, esc(PAGES[hub]["nav"]))} lists every guide in this group. Or return to the {A("index", "homepage")}.</p></div>'
    side = f'<aside class="side" aria-label="Page extras"><div class="sticky">{tochtml}{parent}</div></aside>'
    layout = f'<div class="layout"><div><div class="prose">{body}</div>{faq_html(p["faqs"])}{rel_html}</div>{side}</div>'
    doc = (h + header(slug if slug in dict(NAV) else (CAT2HUB.get(cat) if cat in CAT2HUB else None)) +
           f'<main id="main"><div class="wrap">{crumbs(trail)}<h1>{esc(p["h1"])}</h1><p class="lede">{esc(p["summary"])}</p>{layout}</div></main>' + footer())
    write(page_file(slug), doc)

# ---------- homepage ----------
HOME_FAQS = [
 ("What is a tractor wala game?", "It is an informal way to describe a game where you drive or operate a tractor. It can be a simple driving game, a farming mission game, a trolley hauling game or a more realistic simulator."),
 ("Does this website offer tractor game downloads?", "No. Tractor Wala Game is an information site. It does not host game files or link to specific downloads, and it does not claim any game is free or available. Use your device's official app store."),
 ("How do I download a tractor game safely?", "Search from inside your device's official app store, check the developer and permissions, compare the game's size with your free storage and read recent comments before you install."),
 ("Is it safe to use an APK file for a tractor game?", "Files from outside an official store carry extra risk because they can be altered. We cannot verify any specific file, so read our APK guide before considering that route."),
 ("Which type of tractor game is best for a beginner?", "Simple driving games and light farming missions with adjustable controls and a tutorial are usually the easiest to start with."),
]
def build_home():
    c = url("index")
    title = "Tractor Wala Game: Tractor Simulator and 3D Farming Guides"
    desc = "Tractor wala game guides: tractor simulators, 3D and Indian tractor games, trolley play, safe download advice, gameplay tips and comparisons."
    schemas = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "inLanguage": "en", "publisher": pub_ref()},
        {"@context": "https://schema.org", **PUB},
        {"@context": "https://schema.org", "@type": "WebPage", "@id": c + "#page", "url": c, "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#website"}},
        faq_schema(HOME_FAQS)]
    cats = [("tractor-simulator-game", "Tractor simulator games", "Work-based driving games, from simple to detailed."),
            ("tractor-games-3d", "3D tractor games", "Cameras, graphics and keeping play smooth."),
            ("indian-tractor-games", "Indian tractor games", "Village roads, trolleys and field settings."),
            ("tractor-trolley-wala-game", "Tractor trolley games", "Towing loads and reversing with a trailer."),
            ("tractor-wala-game-download", "Download and install guides", "Official sources, permissions and APK risks."),
            ("tractor-wala-game-for-beginners", "Beginner tutorials", "A first-hour plan for new players."),
            ("tractor-game-comparisons", "Comparisons", "Compare games fairly with the same criteria.")]
    cards = "".join(f'<article class="card big"><h3>{A(s, t)}</h3><p>{d}</p></article>' for s, t, d in cats)
    def group(hub):
        return "".join(card(s) for s in ORDER if PAGES[s]["cat"] == HUBS[hub])
    allcards = len([s for s in ORDER if PAGES[s]["cat"] in CAT2HUB])
    feat = ["best-tractor-games-for-beginners", "tractor-wala-game-video", "how-to-choose-tractor-wala-game", "tractor-wala-game-apk-guide"]
    hero = f'''<section class="hero"><div class="wrap hero-grid"><div>
<h1>Tractor Wala Game: Guides to Tractor Simulators, 3D Farming and Indian Tractor Games</h1>
<p>Looking for a tractor wala game? This independent guide explains the kinds of tractor games, how to find and compare them, how to download them from safe sources, and how to play them well. Everything is written to help you decide, and nothing here promises a game is free or available.</p>
<div class="btns"><a class="btn" href="#find">Find a guide</a><a class="btn alt" href="{href("tractor-wala-game-for-beginners")}">Start as a beginner</a></div>
</div><figure><img src="assets/images/tractor-illustration-generic.svg" width="640" height="360" alt="Flat illustration of a green tractor on a ploughed field. Generic artwork, not a game screenshot.">
<figcaption>Generic illustration, not a screenshot of any game.</figcaption></figure></div></section>'''
    sec = lambda i, t, intro, inner: f'<section aria-labelledby="{i}"><h2 id="{i}">{t}</h2><p class="section-intro">{intro}</p>{inner}</section>'
    main = f'''<main id="main"><div class="wrap">
{sec("intro", "What you will find on this website", "Tractor Wala Game is a static guide site built around the questions people ask when they look for tractor games. In India the phrase tractor wala game is widely used for anything from a quick driving game to a detailed farming simulator, so the guides here separate those styles and explain each one in plain language. You will also find practical advice for mobile players: what a game needs from your phone, which permissions are reasonable, and why files from unofficial websites deserve caution. Read about our standards in the " + A("editorial-policy", "editorial policy") + " or learn more " + A("about", "about the site") + ".", '<div class="grid">' + cards + '</div>')}
{sec("featured", "Featured guides", "If you only read a few pages, start with these.", '<div class="grid">' + "".join(card(s) for s in feat) + '</div>')}
{sec("simulators", "Tractor simulator, 3D and Indian tractor games", "Simulators try to imitate machine behaviour, 3D games add depth and camera control, and Indian-themed games draw on village roads and farm scenes. Each guide explains what to expect and what to verify before you install. For the full set, open the " + A("game-guides", "Game Guides hub") + ".", '<div class="grid">' + "".join(card(s) for s in ["tractor-simulator-game", "tractor-games-3d", "indian-tractor-games", "tractor-trolley-wala-game", "real-tractor-game", "tractor-driving-farming-missions"]) + '</div>')}
{sec("downloads", "Download and installation guides", "A safe download starts at an official source. These guides cover store checks, permissions, device requirements and fixes for common errors. See all of them in the " + A("download-guides", "Download Guides hub") + ".", '<div class="grid">' + group("download-guides") + '</div>')}
{sec("gameplay", "Gameplay, tips and tutorials", "Learn how to watch gameplay, choose between options, handle a trolley and fix problems. The " + A("gameplay-guides", "Gameplay Guides hub") + " collects everything.", '<div class="grid">' + "".join(card(s) for s in ["tractor-wala-game-video", "tractor-wala-game-for-beginners", "tractor-trolley-driving-tips", "tractor-simulator-controls-tips", "tractor-game-troubleshooting", "tractor-games-vs-truck-games"]) + '</div>')}
<section id="find" aria-labelledby="find-h"><h2 id="find-h">Find a guide</h2>
<p class="section-intro">Type a word such as trolley, apk, beginners or controls. The list below is complete HTML, so every guide is reachable even without JavaScript.</p>
<div class="finder"><label for="guide-filter">Search guides</label><input id="guide-filter" type="search" autocomplete="off" placeholder="For example: trolley, apk, controls"><span class="count" id="filter-count" aria-live="polite">{allcards} guides</span></div>
<h3>Game guides</h3><div class="grid">{group("game-guides")}</div>
<h3>Download guides</h3><div class="grid">{group("download-guides")}</div>
<h3>Gameplay guides</h3><div class="grid">{group("gameplay-guides")}</div></section>
{faq_html(HOME_FAQS, "Frequently asked questions about tractor wala games")}
<section class="steps" aria-labelledby="next-h"><h2 id="next-h">Not sure where to begin?</h2><p>New to tractor games? Read {A("best-tractor-games-for-beginners", "best tractor games for beginners")}, then follow {A("tractor-wala-game-for-beginners", "your first hour")}. Need terms explained? Visit the {A("tractor-game-glossary", "glossary")}. Questions or corrections are welcome on the {A("contact", "contact page")}.</p></section>
</div></main>'''
    write("index.html", head(title, desc, c, schemas, og_type="website") + header("index") + hero + main + footer())

def build_404():
    b = "/"
    links = ["tractor-simulator-game", "tractor-wala-game-download", "tractor-wala-game-for-beginners", "indian-tractor-games", "tractor-game-faqs"]
    lis = "".join(f'<li><a href="/{s}.html">{PAGES[s]["nav"]}</a></li>' for s in links)
    doc = (head("Page not found | Tractor Wala Game", "The page you requested could not be found. Use these links to return to Tractor Wala Game guides.", "", [], base=b, noindex=True, og_type="website")
           + header(None, b) + f'''<main id="main"><div class="wrap"><h1>Page not found</h1>
<p class="lede">That page is not here, or the address has changed. These routes will get you back on track.</p>
<div class="prose"><p><a class="btn" href="/">Go to the homepage</a></p><h2>Popular guides</h2><ul>{lis}</ul>
<p>Or browse the <a href="/game-guides.html">Game Guides</a>, <a href="/download-guides.html">Download Guides</a> and <a href="/gameplay-guides.html">Gameplay Guides</a>.</p></div></div></main>''' + footer(b))
    write("404.html", doc)

if __name__ == "__main__":
    # validate links
    for s in ORDER:
        for r in PAGES[s]["related"]:
            assert r in PAGES, (s, r)
    for s in ORDER: build_page(s)
    build_home(); build_404()
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write(".nojekyll", "")
    urls = ["index"] + ORDER
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{url(s)}</loc><lastmod>{BUILD_DATE}</lastmod></url>\n" for s in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    print("pages:", len(urls) + 1)
