# Tractor Wala Game (static website)

Production URL: https://tractorwalagame.github.io/
Repository: https://github.com/tractorwalagame/tractorwalagame.github.io

Static HTML, CSS and a small amount of vanilla JavaScript. No build step, backend, database, tracker or external request is needed.

## Structure

- Root: `index.html`, `404.html`, `robots.txt`, `sitemap.xml`, 3 hub pages (`game-guides.html`, `download-guides.html`, `gameplay-guides.html`), 5 trust pages, `README.md`, `FILE-MANIFEST.md`, `VALIDATION-REPORT.md`, `keyword-map.md`, `content-inventory.md`, favicons, `.nojekyll`
- `articles/`: 31 guide pages
- `assets/css`, `assets/js`, `assets/images`

Pages in `articles/` use `../` relative paths; `404.html` uses root-relative paths because GitHub Pages serves it at any broken address. The `.md` files and `.nojekyll` are public once deployed; delete the documents you do not want published.

## Deploy to GitHub Pages

1. Unzip `tractorwalagame-github-pages.zip`. Its contents (not an outer folder) belong at the root of the repository.
2. Copy everything into a clone of `https://github.com/tractorwalagame/tractorwalagame.github.io` (repository name must be exactly `tractorwalagame.github.io`), commit and push to `main`. Or upload through the GitHub web interface.
3. Open **Settings > Pages**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`, save.
4. After a few minutes open https://tractorwalagame.github.io/ and https://tractorwalagame.github.io/missing-page to see the 404 page.

## Before publishing

- Replace the email placeholder in `contact.html`.
- Read every page. No game, developer, price or download link is named on purpose; add verified details only with an official source and a date.
- Add real screenshots or video only if you own them or have permission, with `alt`, `width` and `height`.

## Google Search Console (not yet done)

1. Add a **URL-prefix** property for `https://tractorwalagame.github.io/`.
2. Verify ownership with the HTML tag (paste into `<head>` of `index.html`) or an HTML file in the repository root.
3. Submit `sitemap.xml` under **Sitemaps**.
4. Use **URL Inspection** on the homepage and guides; compare user-declared and Google-selected canonicals.
5. Review **Pages** (indexing reasons), **Performance** (queries, clicks, impressions) and Core Web Vitals once data exists; fix reported errors and use **Validate fix**.

Indexing and rankings are decided by Google. No ranking, indexing speed or traffic is promised.

## Adding a page

Copy an existing page's head and footer, set a unique title, description and canonical, link to it from a hub and two related guides, and add it to `sitemap.xml`.
