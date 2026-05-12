# MarkBlog — File-based Markdown Blog Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1%2B-lightgrey)](https://flask.palletsprojects.com)
[![GitHub issues](https://img.shields.io/github/issues/AndRiaBX/markblog)](https://github.com/AndRiaBX/markblog/issues)

A lightweight blog engine that renders Markdown files as blog posts. **No database, no CMS** — just drop `.md` files into the `content/` directory.

Built with **Python** and **Flask**.

## Features

- **Write in Markdown** — Create posts as plain `.md` files with YAML frontmatter
- **Zero Database** — Everything is file-based. Your content is plain text.
- **Tag System** — Filter posts by tag with `/tag/<tagname>` routes
- **Auto-generated RSS** — RSS feed at `/feed.xml` for subscribers
- **Syntax Highlighting** — Beautiful code blocks via Pygments
- **Smart Caching** — Content is cached by file hash; append `?reload=1` to rebuild
- **Responsive UI** — Clean, modern design that works on any device

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Server runs on **http://localhost:5000**.

## Usage

### Creating a Post

1. Create a Markdown file in the `content/` directory with YAML frontmatter:

```markdown
---
title: My First Post
date: 2026-01-15
tags: tech, python
---

# Hello World

This is my blog post content in **Markdown**.
```

2. Visit `http://localhost:5000` — your post appears automatically.

> **Need to refresh the index?** Append `?reload=1` to any page URL.

### Frontmatter Fields

| Field   | Required | Description                                      |
|---------|----------|--------------------------------------------------|
| `title` | No       | Post title (defaults to filename)                |
| `date`  | No       | Publication date (`YYYY-MM-DD`), used for sorting |
| `tags`  | No       | Comma or space-separated list of tags            |

### RSS Feed

Subscribe to `/feed.xml` with any RSS reader. Posts are automatically included.

## Project Structure

```
markblog/
├── app.py              # Flask application and routes
├── blog.py             # Blog engine: load, parse, cache
├── requirements.txt    # Python dependencies
├── content/            # Drop .md files here
├── templates/
│   ├── base.html       # Base layout
│   ├── index.html      # Post listing
│   ├── post.html       # Single post view
│   └── 404.html        # Not found page
└── README.md
```

## Dependencies

| Package    | Version | Purpose                    |
|------------|---------|----------------------------|
| Flask      | 3.1+    | Web framework              |
| Markdown   | 3.7+    | Markdown → HTML conversion |
| Pygments   | 2.19+   | Syntax highlighting        |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with Flask and Python.*
