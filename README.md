# MarkBlog — File-based Markdown Blog Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Markdown-3.7-000000?logo=markdown&logoColor=white" alt="Markdown">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/github/actions/workflow/status/AndRiaBX/markblog/ci.yml?branch=master" alt="CI">
  <img src="https://img.shields.io/github/issues/AndRiaBX/markblog" alt="Issues">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs Welcome">
</p>

A lightweight blog engine that renders Markdown files as blog posts. **No database, no CMS** — just drop `.md` files into the `content/` directory and they appear on your blog.

Built with **Python** and **Flask**.

---

## Features

- **✍️ Write in Markdown** — Create posts as plain `.md` files with YAML frontmatter
- **🗄️ Zero Database** — Everything is file-based. Your content is plain text.
- **🏷️ Tag System** — Filter posts by tag with `/tag/<tagname>` routes
- **📡 Auto-generated RSS** — RSS feed at `/feed.xml` for subscribers
- **🎨 Syntax Highlighting** — Beautiful code blocks via Pygments
- **⚡ Smart Caching** — Content is cached by file hash; append `?reload=1` to rebuild
- **📱 Responsive UI** — Clean, modern design that works on any device
- **🐳 Docker Support** — One-command deployment with docker-compose

---

## Screenshots

> _Screenshots coming soon. The UI features a clean, minimal design with responsive typography and syntax-highlighted code blocks._

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Python 3.9+ |
| Framework | Flask 3.1 |
| Markdown | Python-Markdown 3.7 with `extra`, `codehilite`, `toc` extensions |
| Highlighting | Pygments 2.19 |
| Container | Docker (python:3.12-slim) |
| Testing | Pytest 8.3 |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/AndRiaBX/markblog.git
cd markblog

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a sample post
mkdir -p content
cat > content/hello-world.md << 'EOF'
---
title: Hello World
date: 2026-05-12
tags: demo, python
---

# Hello World

Welcome to **MarkBlog**! This post was created by dropping a `.md` file into the `content/` directory.
EOF

# 4. Start server
python app.py
```

Server runs on **http://localhost:5000**.

---

## Usage

### Creating a Post

Create a Markdown file in the `content/` directory with YAML frontmatter:

```markdown
---
title: My First Post
date: 2026-01-15
tags: tech, python
---

# Hello World

This is my blog post content in **Markdown**.
```

Visit `http://localhost:5000` — your post appears automatically.

> **Need to refresh the index?** Append `?reload=1` to any page URL to force a full index rebuild.

### Frontmatter Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `title` | No | Filename (without `.md`) | Post title |
| `date` | No | — | Publication date (`YYYY-MM-DD`), used for sorting |
| `tags` | No | `[]` | Comma or space-separated list of tags |

---

## Routes

| Route | Description |
|-------|-------------|
| `GET /` | Home page — list all posts, newest first |
| `GET /<slug>` | Single post view |
| `GET /tag/<tagname>` | Filter posts by tag |
| `GET /feed.xml` | RSS feed (last 20 posts) |

---

## Project Structure

```
markblog/
├── app.py              # Flask application and routes
├── blog.py             # Blog engine: load, parse, cache posts
├── requirements.txt    # Python dependencies
├── content/            # Drop .md files here (auto-created)
├── templates/
│   ├── base.html       # Base layout with responsive styles
│   ├── index.html      # Post listing page
│   ├── post.html       # Single post view
│   └── 404.html        # Not found page
├── tests/
│   └── test_blog.py    # Pytest test suite
├── .github/
│   ├── workflows/
│   │   └── ci.yml      # GitHub Actions CI
│   └── ISSUE_TEMPLATE/
├── Dockerfile
├── docker-compose.yml
├── .index_cache.json   # Content cache (auto-generated)
├── CONTRIBUTING.md
└── README.md
```

---

## Development Setup

### Prerequisites

- Python 3.9+ (3.12 recommended)
- pip

### Install & run locally

```bash
git clone https://github.com/AndRiaBX/markblog.git
cd markblog
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Running tests

```bash
python -m pytest tests/ -v
```

Tests use `pytest` with temporary content directories — no manual setup needed.

---

## Docker Deployment

### Using Docker directly

```bash
docker build -t markblog .
docker run -d \
  --name markblog \
  -p 5000:5000 \
  -v $(pwd)/content:/app/content \
  markblog
```

### Using Docker Compose (recommended for development)

```bash
docker compose up --build
```

The `docker-compose.yml` mounts `./content` and `./templates` as volumes for hot-reload during development.

### Cloud Deployment

**Fly.io:**
```bash
fly launch
fly deploy
```

**Railway / Render:**
- Connect GitHub repository
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Set environment variable `FLASK_ENV=production`

---

## Performance

- Content is cached in `.index_cache.json` using SHA-256 hashes
- Cache is validated per-file; unchanged files skip re-parsing
- Append `?reload=1` to force a full cache rebuild
- RSS feed is generated on-the-fly from the cached post index

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Development setup
- Code style (PEP 8)
- PR process
- Issue reporting

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with Flask and Python.
</p>
