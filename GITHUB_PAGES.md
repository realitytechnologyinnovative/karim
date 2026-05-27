# GitHub Pages deployment

This project is a Django site, so GitHub Pages cannot run it directly.  
Use the exporter below to generate a static version into `docs/`.

## 1) Build static export

From the project root:

```bash
python export_github_pages.py
```

This generates:

- `docs/index.html`
- `docs/about/index.html`
- `docs/services/index.html`
- `docs/projects/index.html`
- `docs/projects/<slug>/index.html` for every published project
- `docs/static/...` copied assets
- `docs/media/...` copied uploads (if present)
- `docs/.nojekyll`

## 2) Commit and push

```bash
git add docs export_github_pages.py GITHUB_PAGES.md
git commit -m "Add GitHub Pages static export pipeline"
git push
```

## 3) Enable Pages in GitHub

In your repository settings:

- Go to **Pages**
- Set **Source** to `Deploy from a branch`
- Select your branch (usually `main`)
- Select folder: `/docs`
- Save

After a minute or two, your site should be live.
