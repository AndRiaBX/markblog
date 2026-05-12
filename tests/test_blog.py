"""
MarkBlog test suite — tests blog rendering, RSS generation, 404 handling.
Uses pytest with a temporary content directory.
"""
import os
import sys
import json

# Ensure the project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from blog import load_posts, get_post, parse_frontmatter, CONTENT_DIR, INDEX_FILE


@pytest.fixture(autouse=True)
def patch_index_cache(monkeypatch, tmp_path):
    """Redirect INDEX_FILE to temp dir so cache writes don't collide."""
    monkeypatch.setattr('blog.INDEX_FILE', str(tmp_path / '.index_cache.json'))
    yield tmp_path


def _load_posts(content_dir, force=False):
    """Helper: call load_posts with a specific content directory."""
    return load_posts(force=force, content_dir=str(content_dir))


def create_post(dirpath, filename, title, date, tags, body):
    """Helper: create a markdown post file with frontmatter."""
    tags_str = ', '.join(tags) if isinstance(tags, list) else tags
    content = f"""---
title: {title}
date: {date}
tags: {tags_str}
---
{body}"""
    with open(os.path.join(str(dirpath), filename), 'w', encoding='utf-8') as f:
        f.write(content)


class TestParseFrontmatter:
    def test_parse_full_post(self):
        text = """---
title: Hello World
date: 2026-01-15
tags: tech, python
---
# Hello
Content here."""
        meta, body = parse_frontmatter(text)
        assert meta['title'] == 'Hello World'
        assert meta['date'] == '2026-01-15'
        assert meta['tags'] == ['tech', 'python']
        assert '# Hello' in body
        assert 'Content here.' in body

    def test_parse_no_frontmatter(self):
        text = "Just plain content without frontmatter."
        meta, body = parse_frontmatter(text)
        assert meta == {}
        assert body == text

    def test_parse_empty_tags(self):
        text = """---
title: No Tags
date: 2026-01-01
---
Body text."""
        meta, body = parse_frontmatter(text)
        assert meta['title'] == 'No Tags'
        assert meta.get('tags', []) == []

    def test_parse_extra_whitespace(self):
        text = """---
  title:  Spaced Out  
date: 2026-06-01  
  tags:  a , b , c  
---
Body"""
        meta, body = parse_frontmatter(text)
        assert meta['title'] == 'Spaced Out'
        assert meta['tags'] == ['a', 'b', 'c']


class TestLoadPosts:
    def test_empty_content_dir(self, tmp_path):
        posts = _load_posts(tmp_path)
        assert posts == []

    def test_single_post(self, tmp_path):
        create_post(tmp_path, 'hello-world.md', 'Hello', '2026-01-01', ['test'], 'Hello content')
        posts = _load_posts(tmp_path)
        assert len(posts) == 1
        assert posts[0]['slug'] == 'hello-world'
        assert posts[0]['title'] == 'Hello'
        assert posts[0]['date'] == '2026-01-01'
        assert posts[0]['tags'] == ['test']
        assert posts[0]['body'] == 'Hello content'

    def test_multiple_posts_sorted_by_date(self, tmp_path):
        create_post(tmp_path, 'first.md', 'First', '2026-01-01', [], 'First body')
        create_post(tmp_path, 'second.md', 'Second', '2026-03-15', [], 'Second body')
        create_post(tmp_path, 'third.md', 'Third', '2026-02-10', [], 'Third body')
        posts = _load_posts(tmp_path)
        assert len(posts) == 3
        assert posts[0]['title'] == 'Second'
        assert posts[1]['title'] == 'Third'
        assert posts[2]['title'] == 'First'

    def test_ignores_non_markdown_files(self, tmp_path):
        create_post(tmp_path, 'post.md', 'Post', '2026-01-01', [], 'Body')
        with open(os.path.join(str(tmp_path), 'notes.txt'), 'w') as f:
            f.write('Not a blog post')
        posts = _load_posts(tmp_path)
        assert len(posts) == 1

    def test_cache_usage(self, tmp_path):
        create_post(tmp_path, 'cached.md', 'Cached', '2026-01-01', [], 'Original')
        posts1 = _load_posts(tmp_path)
        assert len(posts1) == 1
        assert posts1[0]['body'] == 'Original'

        # Same content — cache should be used (no re-read)
        posts2 = _load_posts(tmp_path)
        assert posts2[0]['body'] == 'Original'

        # Modify the file
        create_post(tmp_path, 'cached.md', 'Cached', '2026-01-01', [], 'Updated body')

        # Without force, hash mismatch triggers re-read, getting new content
        posts3 = _load_posts(tmp_path)
        assert posts3[0]['body'] == 'Updated body'

        # With force, index is rebuilt from scratch
        create_post(tmp_path, 'cached.md', 'Cached', '2026-01-01', [], 'Force reloaded')
        posts4 = _load_posts(tmp_path, force=True)
        assert posts4[0]['body'] == 'Force reloaded'


class TestGetPost:
    def test_find_existing_post(self, tmp_path):
        create_post(tmp_path, 'my-post.md', 'My Post', '2026-01-01', [], 'Body')
        posts = _load_posts(tmp_path)
        found = get_post('my-post', posts)
        assert found is not None
        assert found['slug'] == 'my-post'

    def test_missing_post_returns_none(self):
        found = get_post('nonexistent', [])
        assert found is None


class TestRendering:
    def test_markdown_to_html(self):
        from app import render_md
        html = render_md('# Hello\n\nThis is **bold** and `code`.')
        # 'extra' extension adds id attributes, so check for partial match
        assert 'Hello' in html
        assert '<strong>bold</strong>' in html
        assert '<code>code</code>' in html

    def test_rss_generation(self):
        from app import app
        with app.test_client() as client:
            resp = client.get('/feed.xml')
            assert resp.status_code == 200
            assert resp.content_type == 'application/rss+xml'
            assert '<?xml version="1.0" encoding="UTF-8"?>' in resp.data.decode('utf-8')

    def test_404_page(self):
        from app import app
        with app.test_client() as client:
            resp = client.get('/nonexistent-post')
            assert resp.status_code == 404

    def test_home_page(self):
        from app import app
        with app.test_client() as client:
            resp = client.get('/')
            assert resp.status_code == 200
