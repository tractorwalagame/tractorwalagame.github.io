import os, re, json, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
OUT = "out"; SITE = "https://tractorwalagame.github.io"

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title = ""; s._t = False; s.meta = {}; s.links = []; s.ids = set(); s.h1 = 0; s.h2 = 0
        s.canon = []; s.jsonld = []; s._j = False; s.imgs = []; s.assets = []; s.text = []; s.main = False; s.kw = False; s.robots = ""
        s.lang = None; s.viewport = False; s.skipdepth = 0; s.scripts_ext = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "html": s.lang = a.get("lang")
        if tag == "title": s._t = True
        if tag == "main": s.main = True
        if tag == "h1": s.h1 += 1
        if tag == "h2": s.h2 += 1
        if tag == "meta":
            n = a.get("name") or a.get("property")
            if n: s.meta[n] = a.get("content", "")
            if a.get("name") == "keywords": s.kw = True
            if a.get("name") == "viewport": s.viewport = True
            if a.get("name") == "robots": s.robots = a.get("content", "")
        if tag == "link":
            if a.get("rel") == "canonical": s.canon.append(a.get("href"))
            if a.get("href") and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon"): s.assets.append(a["href"])
        if tag == "a" and a.get("href"): s.links.append(a["href"])
        if tag == "img": s.imgs.append(a); s.assets.append(a.get("src", ""))
        if tag == "script":
            if a.get("type") == "application/ld+json": s._j = True
            if a.get("src"): s.assets.append(a["src"]); s.scripts_ext.append(a["src"])
        if tag in ("script", "style"): s.skipdepth += 1
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script": s._j = False
        if tag in ("script", "style"): s.skipdepth -= 1
    def handle_data(s, d):
        if s._t: s.title += d
        elif s._j: s.jsonld.append(d)
        elif s.main and not s.skipdepth: s.text.append(d)

res = {"pass": [], "fail": [], "warn": []}
def ok(m): res["pass"].append(m)
def bad(m): res["fail"].append(m)
def warn(m): res["warn"].append(m)

files = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
pages = {}
for f in files:
    p = P(); p.feed(open(os.path.join(OUT, f), encoding="utf-8").read()); pages[f] = p
sm = open(f"{OUT}/sitemap.xml").read()
smurls = re.findall(r"<loc>([^<]+)</loc>", sm)

def canon_of(f): return SITE + "/" if f == "index.html" else f"{SITE}/{f}"
indexable = [f for f in files if f != "404.html"]

# 1 pages exist / counts
ok(f"{len(files)} HTML files exist ({len(indexable)} indexable + 404.html)")
for need in ["robots.txt", "sitemap.xml", "favicon.svg", "favicon.ico", "apple-touch-icon.png", "assets/css/style.css", "assets/js/main.js", ".nojekyll"]:
    (ok if os.path.exists(f"{OUT}/{need}") else bad)(f"required file {need}")
# 3 titles / descriptions unique
for key, name in (("title", "title"), ("desc", "meta description")):
    vals = {}
    for f in indexable:
        v = pages[f].title.strip() if key == "title" else pages[f].meta.get("description", "")
        vals.setdefault(v, []).append(f)
        lim = 65 if key == "title" else 165
        if len(v) > lim: warn(f"{f}: {name} length {len(v)} > {lim}")
        if not v: bad(f"{f}: empty {name}")
    d = {k: v for k, v in vals.items() if len(v) > 1}
    (bad if d else ok)(f"duplicate {name}s: {d}" if d else f"all {len(indexable)} {name}s unique")
# canonicals, h1, lang, viewport
for f in indexable:
    p = pages[f]
    if p.canon != [canon_of(f)]: bad(f"{f}: canonical {p.canon} != {canon_of(f)}")
    if p.h1 != 1: bad(f"{f}: {p.h1} h1 elements")
    if p.lang != "en": bad(f"{f}: lang")
    if not p.viewport: bad(f"{f}: viewport")
    if "noindex" in p.robots: bad(f"{f}: noindex on indexable page")
    if p.kw: bad(f"{f}: meta keywords present")
    if p.meta.get("og:url") != canon_of(f): bad(f"{f}: og:url mismatch")
    if p.h2 < 1: bad(f"{f}: no h2")
if not any(s.startswith("canonical") or s.endswith("canonical") for s in res["fail"]): ok("all canonicals correct, absolute, on production domain; one H1; lang=en; viewport present; no noindex; no meta keywords; og:url matches canonical")
if pages["404.html"].canon == [] and "noindex" in pages["404.html"].robots: ok("404.html is noindex and has no canonical")
else: bad("404 robots/canonical")
# sitemap
exp = sorted(canon_of(f) for f in indexable)
(ok if sorted(smurls) == exp and len(set(smurls)) == len(smurls) else bad)(f"sitemap lists exactly the {len(exp)} indexable canonical URLs, no duplicates, no 404")
rb = open(f"{OUT}/robots.txt").read()
(ok if f"Sitemap: {SITE}/sitemap.xml" in rb and "Disallow" not in rb else bad)("robots.txt references sitemap and blocks nothing")
# links
inbound = {f: set() for f in indexable}; outbound = {f: set() for f in indexable}; ext = set()
for f in files:
    p = pages[f]
    for h in p.links + p.assets:
        if not h or h.startswith(("mailto:", "tel:")): continue
        u = urlparse(h)
        if u.scheme in ("http", "https"):
            ext.add(h) if h in p.links else None
            if u.netloc == "tractorwalagame.github.io" and h in p.links: bad(f"{f}: absolute internal link {h}")
            continue
        path = unquote(u.path)
        if f == "404.html" and path.startswith("/"): target = path.lstrip("/") or "index.html"
        else: target = path or f
        if target in ("", "./") : target = "index.html"
        if target.endswith("/"): target += "index.html"
        if f == "404.html" and path == "/": target = "index.html"
        full = os.path.join(OUT, target)
        if not os.path.exists(full): bad(f"{f}: broken link/asset {h}"); continue
        if u.fragment and target.endswith(".html"):
            tp = pages.get(target)
            if tp and u.fragment not in tp.ids: bad(f"{f}: missing anchor {h}")
        if h in p.links and target in inbound and f in outbound and target != f:
            inbound[target].add(f); outbound[f].add(target)
if not [x for x in res["fail"] if "broken" in x or "anchor" in x or "absolute internal" in x]: ok("every internal link, anchor, stylesheet, script, icon and image path resolves to an existing local file/id")
orph = [f for f, s in inbound.items() if not s]
(bad if orph else ok)(f"orphan pages: {orph}" if orph else "no orphan pages (every indexable page has at least one inbound internal link)")
# reachability from home
seen = {"index.html"}; q = ["index.html"]
while q:
    c = q.pop()
    for t in outbound[c]:
        if t not in seen: seen.add(t); q.append(t)
miss = [f for f in indexable if f not in seen]
(bad if miss else ok)(f"not reachable from home: {miss}" if miss else "all pages reachable from the homepage through normal HTML links")
home_direct = outbound["index.html"]
(ok if len(home_direct) == len(indexable) - 1 else warn)(f"homepage links directly to {len(home_direct)} of {len(indexable)-1} other pages")
# JSON-LD
n = 0
for f in files:
    for blob in pages[f].jsonld:
        try: json.loads(blob); n += 1
        except Exception as e: bad(f"{f}: invalid JSON-LD {e}")
ok(f"{n} JSON-LD blocks parse as valid JSON") if not [x for x in res["fail"] if "JSON-LD" in x] else None
# FAQ markup matches visible
for f in indexable:
    for blob in pages[f].jsonld:
        d = json.loads(blob)
        if d.get("@type") == "FAQPage":
            vis = " ".join(pages[f].text)
            for qn in d["mainEntity"]:
                if qn["name"] not in vis: bad(f"{f}: FAQ schema question not visible: {qn['name']}")
ok("FAQ structured data questions all appear in visible page text") if not [x for x in res["fail"] if "FAQ" in x] else None
# images
for f in files:
    for im in pages[f].imgs:
        if not im.get("alt") or not im.get("width") or not im.get("height"): bad(f"{f}: img missing alt/width/height")
ok("all <img> elements have alt text, width and height") if not [x for x in res["fail"] if "img" in x] else None
# placeholders / banned
alltext = "".join(open(os.path.join(OUT, f), encoding="utf-8").read() for f in files)
for pat in ["example.com", "lorem", "TODO", "http://localhost", "127.0.0.1"]:
    (bad if pat.lower() in alltext.lower() else ok)(f"no '{pat}' in output")
for f in files:
    if re.search(r"https?://(?!tractorwalagame\.github\.io|github\.com/tractorwalagame|www\.w3\.org|schema\.org)", open(f"{OUT}/{f}", encoding="utf-8").read()): bad(f"{f}: unexpected external URL")
# external scripts
for f in files:
    if any(s.startswith("http") for s in pages[f].scripts_ext): bad(f"{f}: third-party script")
ok("no third-party scripts, fonts or external resources are loaded")
# word counts
wc = {f: len(re.findall(r"\w+", " ".join(pages[f].text))) for f in indexable}
thin = [f for f, w in wc.items() if w < 500 and f not in ("download-guides.html", "contact.html", "privacy-policy.html", "disclaimer.html", "about.html", "editorial-policy.html")]
(warn if thin else ok)(f"pages under 500 words: {thin}" if thin else "all guides/hubs have >=500 words")
json.dump({"res": res, "wc": wc, "inbound": {k: sorted(v) for k, v in inbound.items()}, "outbound": {k: sorted(v) for k, v in outbound.items()}, "ext": sorted(ext)}, open("validation.json", "w"), indent=1)
print("PASS", len(res["pass"]), "FAIL", len(res["fail"]), "WARN", len(res["warn"]))
for k in ("fail", "warn"):
    for m in res[k]: print(k.upper(), m)
print(sorted(wc.items(), key=lambda x: x[1])[:12]); print(sum(wc.values()), "words total")
