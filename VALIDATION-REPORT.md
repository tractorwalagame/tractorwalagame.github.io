# VALIDATION REPORT

Run date: 2026-10-12. Every result below comes from `validate.py` (Python standard library) executed on the files in this archive after restructuring. Nothing here was measured in a browser or by an external service.

## 1. Checks actually completed (static)

- PASS: 41 HTML files exist (40 indexable + 404.html)
- PASS: required file index.html
- PASS: required file 404.html
- PASS: required file robots.txt
- PASS: required file sitemap.xml
- PASS: required file favicon.svg
- PASS: required file favicon.ico
- PASS: required file apple-touch-icon.png
- PASS: required file assets/css/style.css
- PASS: required file assets/js/main.js
- PASS: required file .nojekyll
- PASS: all 40 titles unique
- PASS: all 40 meta descriptions unique
- PASS: all canonicals correct, absolute, on production domain; one H1; lang=en; viewport present; no noindex; no meta keywords; og:url matches canonical
- PASS: 404.html is noindex and has no canonical
- PASS: sitemap lists exactly the 40 indexable canonical URLs, no duplicates, no 404
- PASS: robots.txt references sitemap and blocks nothing
- PASS: every internal link, anchor, stylesheet, script, icon and image path resolves to an existing local file/id
- PASS: no orphan pages (every indexable page has at least one inbound internal link)
- PASS: all pages reachable from the homepage through normal HTML links
- PASS: homepage links directly to 39 of 39 other pages
- PASS: 113 JSON-LD blocks parse as valid JSON
- PASS: FAQ structured data questions all appear in visible page text
- PASS: all <img> elements have alt text, width and height
- PASS: no 'example.com' in output
- PASS: no 'lorem' in output
- PASS: no 'TODO' in output
- PASS: no 'http://localhost' in output
- PASS: no '127.0.0.1' in output
- PASS: no third-party scripts, fonts or external resources are loaded
- PASS: all guides/hubs have >=500 words

Final run: **31 passed, 0 failed, 0 warnings**. 1642 internal link/anchor references on 40 indexable pages were resolved.

Negative test: one internal link was deliberately broken in a copy of an article; the validator reported it as a failure, then the file was restored and the run returned to 0 failures.

## 2. Errors found and fixed

- **Structure:** the earlier build kept all guides in the repository root. Guides were moved to `articles/`, all relative paths, canonicals, breadcrumbs, JSON-LD URLs and sitemap entries were regenerated, and `index.html`, `404.html`, `robots.txt` and `sitemap.xml` stay at the archive root.
- **Missing required topic:** *Tractor Wala Game Gameplay* did not exist as its own page. It was written as a new guide about the play loop and pacing (the video page stays focused on judging footage).
- **Keyword usage:** `game tractor wala` and `wala game tractor wala game` appeared only in metadata. They now appear naturally in homepage copy and FAQ; the Hinglish query pages are linked from the homepage.
- **Validator bug (earlier round):** canonical tags were wrongly counted as internal links. Fixed; validator now also handles nested paths and rejects root-relative links outside the 404 page.
- No broken links, anchors, assets, duplicate titles/descriptions or canonical errors were found in the restructured output.

## 3. Remaining issues

- **Article depth:** 31 articles average 691 words (range 604 to 953; measured), below the 1,000 to 1,800 range you mentioned. They were left at their natural length instead of padded. Expand them with first-hand details.
- **No verified game data:** no specific game, developer, price, download link or APK is named. No real screenshots or videos exist; the only images are a labelled generic illustration, an Open Graph image and icons.
- **Placeholder:** `contact.html` contains `[ADD YOUR CONTACT EMAIL HERE]` on purpose. Replace it or remove the line.
- **URL change:** guide URLs moved from `/slug.html` to `/articles/slug.html`. If the earlier layout was ever published or submitted, add redirects (not possible on GitHub Pages without extra pages) or resubmit the new sitemap.
- Sitemap `lastmod` is the build date for every URL.

## 4. Checks that need a browser, external tools or a live deployment (NOT done)

- Rendering on real phones and desktops, mobile menu and guide filter behaviour (JavaScript written, not executed in a browser)
- Lighthouse / PageSpeed / Core Web Vitals (no score is claimed)
- Google Rich Results Test and Schema.org validator (only JSON syntax and FAQ-text consistency were checked)
- Colour contrast measurement and screen-reader testing
- Live GitHub Pages deployment, HTTPS and the 404 page on the real domain
- Google Search Console setup, verification, sitemap submission and indexing (nothing has been done; Google has not indexed this site as far as this project knows)
- External link health (the only external link is the GitHub issues URL on the contact page)

