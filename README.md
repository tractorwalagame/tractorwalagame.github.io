# Tractor Wala Game (static website)

Production URL: https://tractorwalagame.github.io/
Repository: https://github.com/tractorwalagame/tractorwalagame.github.io

An independent guide site about tractor games: simulators, 3D and Indian tractor games, trolley play, safe downloads and gameplay. Plain HTML, CSS and a small amount of vanilla JavaScript. No build step, backend, database, tracker or external request is needed to run it.

## Contents

- `index.html` plus **38** other indexable pages: 3 hubs, 30 guides, 5 trust pages; and `404.html`
- `assets/css/style.css`, `assets/js/main.js`, `assets/images/` (generic illustration, OG image, icon)
- `robots.txt`, `sitemap.xml` (39 URLs), favicon files, `.nojekyll`
- `keyword-map.md`, `content-inventory.md`, `SEO-validation-report.md`

URL convention: flat, lowercase, hyphenated `.html` files in the repository root (for example `/tractor-simulator-game.html`). This keeps relative links and asset paths reliable on GitHub Pages with no rewrite rules. `404.html` uses root-relative paths because GitHub Pages serves it at any broken URL.

## Deploy to GitHub Pages

1. Unzip the project. Deploy only the contents of the `site/` folder; they must sit at the **root** of the repository (`index.html` next to `robots.txt`), not inside a subfolder. The `generator/` folder is optional tooling and should stay out of the repository.
2. Copy them into a local clone of `https://github.com/tractorwalagame/tractorwalagame.github.io`, or upload them through the GitHub web interface.
3. Commit and push to the default branch (`main`).
4. In the repository, open **Settings > Pages**. Under **Build and deployment**, set **Source: Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
5. Wait a few minutes, then open https://tractorwalagame.github.io/ and https://tractorwalagame.github.io/does-not-exist (to see the 404 page).
6. The repository must be named exactly `tractorwalagame.github.io` for the root URL to work.

The `.nojekyll` file tells GitHub Pages to serve files as they are. The `.md` documents in the root will also be publicly viewable; move them to a private place if you do not want that.

## Before you publish: checklist

- Replace the contact email placeholder in `contact.html`.
- Read every page and correct anything you cannot stand behind. No game is named and no download is linked on purpose; add verified details only with an official source and a date.
- Add real screenshots or video only if you own them or have permission; then add `alt`, `width` and `height`.

## Google Search Console

Nothing has been configured. To do it yourself:

1. Open Search Console and choose **Add property**. A **URL-prefix** property for `https://tractorwalagame.github.io/` is the simplest for a github.io site.
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
