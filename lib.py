import html, re, json

SITE = "https://tractorwalagame.github.io"
NAME = "Tractor Wala Game"
REPO = "https://github.com/tractorwalagame/tractorwalagame.github.io"
BUILD_DATE = "2026-10-12"

PAGES = {}   # slug -> dict
ORDER = []

def P(slug, nav, title, desc, h1, cat, kw, kws, intent, summary, body, faqs=(), related=(), steps="", purpose=""):
    assert slug not in PAGES, slug
    PAGES[slug] = dict(slug=slug, nav=nav, title=title, desc=desc, h1=h1, cat=cat, kw=kw,
                       kws=kws, intent=intent, summary=summary, body=body, faqs=list(faqs),
                       related=list(related), steps=steps, purpose=purpose)
    ORDER.append(slug)

def esc(s): return html.escape(s, quote=False)

def inline(s):
    s = esc(s)
    def link(m):
        slug, _, text = m.group(1).partition("|")
        if slug not in PAGES and slug != "index":
            raise KeyError("bad link: " + slug)
        href = "./" if slug == "index" else slug + ".html"
        label = text or (PAGES[slug]["nav"] if slug in PAGES else "Home")
        return f'<a href="{href}">{label}</a>'
    s = re.sub(r"\[\[([^\]]+)\]\]", link, s)
    s = re.sub(r"\[([^\]\[]+)\]\((https://[^)\s]+)\)", r'<a href="\2" rel="noopener" target="_blank">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def render_body(text):
    """mini-markup -> (html, [(id, h2 text)])"""
    out, toc = [], []
    for block in re.split(r"\n\s*\n", text.strip()):
        b = block.strip("\n")
        if b.startswith("## "):
            t = b[3:].strip(); i = slugify(t); toc.append((i, t))
            out.append(f'<h2 id="{i}">{inline(t)}</h2>')
        elif b.startswith("### "):
            out.append(f"<h3>{inline(b[4:].strip())}</h3>")
        elif b.startswith("> "):
            out.append('<aside class="note"><p>' + inline(" ".join(l[2:] for l in b.split("\n"))) + "</p></aside>")
        elif b.startswith("- "):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:].strip())}</li>" for l in b.split("\n") if l.startswith("- ")) + "</ul>")
        elif re.match(r"1\. ", b):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l).strip())}</li>" for l in b.split("\n")) + "</ol>")
        elif b.startswith("|"):
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in b.split("\n")]
            rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
            h = "<tr>" + "".join(f'<th scope="col">{inline(c)}</th>' for c in rows[0]) + "</tr>"
            bd = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table-wrap" tabindex="0" role="region" aria-label="Comparison table"><table><thead>{h}</thead><tbody>{bd}</tbody></table></div>')
        else:
            out.append(f"<p>{inline(b.replace(chr(10), ' '))}</p>")
    return "\n".join(out), toc
