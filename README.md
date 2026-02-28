# Static Site Generator Project

This is a small static site generator I built while learning with Boot.dev. It takes Markdown files, applies an HTML template, copies static files, and builds a website that can be hosted.

## Why I built this
I built this project while learning backend development. It helped me understand how Python works with files and folders, how HTML templates work, and how recursion is used to go through directories.

## What it does
- Converts Markdown files into HTML
- Uses a shared `template.html` for all pages
- Recursively reads everything inside the `content/` folder
- Copies static files from `static/`
- Supports a `basepath` for GitHub Pages
- Outputs the final site into `docs/`

## Project layout
- `content/` — Markdown files
- `static/` — CSS, images, and other static files
- `src/` — Python code for the generator
- `template.html` — HTML layout
- `docs/` — Generated site (ready for GitHub Pages)

## Build

Local build:

```bash
python3 src/main.py
```

Build for GitHub Pages:

```bash
./build.sh
```

This project helped me understand file paths, recursion, and how static sites are generated.