# MarkBlog — File-based Markdown Blog Engine

A lightweight blog engine that renders Markdown files as blog posts. Built with **Python** and **Flask**.

## Features

- Write posts in plain Markdown files (`content/*.md`)
- Auto-generates metadata from YAML frontmatter (title, date, tags)
- Tag-based filtering with `/tag/<tagname>` pages
- Automatic RSS feed at `/feed.xml`
- Clean, responsive UI with syntax-highlighted code blocks

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`.

## Usage

1. Create `content/*.md` files with YAML frontmatter:

```markdown
---
title: My First Post
date: 2026-01-15
tags: tech, python
---

# Hello World

This is my blog post content in **Markdown**.
```

2. Restart or append `?reload=1` to any page to rebuild the index.

## Structure

```
markblog/
├── app.py           # Flask application
├── blog.py          # Blog engine (load, parse, render)
├── requirements.txt
├── templates/
│   ├── base.html    # Base layout
│   ├── index.html   # Post list
│   └── post.html    # Single post view
├── content/         # Drop .md files here
└── README.md
```
