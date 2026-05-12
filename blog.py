"""Blog engine: loads, parses, and serves Markdown content with YAML frontmatter."""

import os
import re
import json
import hashlib
from datetime import datetime

CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')
INDEX_FILE = os.path.join(os.path.dirname(__file__), '.index_cache.json')

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n?(.*)', re.DOTALL)
TAG_SPLIT_RE = re.compile(r'[,\s]+')


def parse_frontmatter(text):
    """Extract YAML-like frontmatter and body text."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text

    raw = m.group(1)
    body = m.group(2)
    meta = {}
    for line in raw.strip().split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip().lower()
            val = val.strip()
            if key == 'tags':
                meta[key] = [t.strip() for t in TAG_SPLIT_RE.split(val) if t.strip()]
            else:
                meta[key] = val
    return meta, body


def get_file_hash(filepath):
    """SHA256 of file contents for cache invalidation."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def load_posts(force=False, content_dir=None):
    """Load all markdown posts from content/ directory. Caches via JSON."""
    if content_dir is None:
        content_dir = CONTENT_DIR
    if not os.path.isdir(content_dir):
        os.makedirs(content_dir, exist_ok=True)

    cache = {}
    if os.path.exists(INDEX_FILE) and not force:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)

    posts = []
    current_hashes = {}

    for fname in sorted(os.listdir(content_dir)):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(content_dir, fname)
        fhash = get_file_hash(fpath)
        current_hashes[fname] = fhash

        # Use cache if unchanged
        if fname in cache and cache[fname].get('hash') == fhash:
            posts.append(cache[fname])
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()

        meta, body = parse_frontmatter(text)
        slug = fname[:-3]  # remove .md

        entry = {
            'hash': fhash,
            'slug': slug,
            'title': meta.get('title', slug),
            'date': meta.get('date', ''),
            'tags': meta.get('tags', []),
            'body': body,
        }
        posts.append(entry)
        cache[fname] = entry

    # Sort by date descending, then by slug
    def sort_key(p):
        try:
            return datetime.strptime(p['date'], '%Y-%m-%d').isoformat()
        except (ValueError, TypeError):
            return '0000-00-00'
    posts.sort(key=lambda p: (sort_key(p), p['slug']), reverse=True)

    # Write cache
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

    return posts


def get_post(slug, posts):
    """Find a single post by slug."""
    for p in posts:
        if p['slug'] == slug:
            return p
    return None
