"""MarkBlog — Flask application serving file-based Markdown blog."""

from flask import Flask, render_template, request, make_response
import markdown
from blog import load_posts, get_post

app = Flask(__name__)

MD_EXTENSIONS = [
    'extra',
    'codehilite',
    'toc',
]


def render_md(text):
    """Render Markdown to HTML with extensions."""
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def get_reload_flag():
    """Check if ?reload=1 is in the query string to force index rebuild."""
    return request.args.get('reload') == '1'


def load_and_check():
    """Load posts, force reindex if reload flag is set."""
    force = get_reload_flag()
    return load_posts(force=force)


@app.route('/')
def index():
    posts = load_and_check()
    return render_template('index.html', posts=posts)


@app.route('/<slug>')
def post(slug):
    posts = load_and_check()
    entry = get_post(slug, posts)
    if not entry:
        return render_template('base.html', title='Not Found', content='<h1>404</h1><p>Post not found.</p>'), 404
    html = render_md(entry['body'])
    return render_template('post.html', post=entry, content=html)


@app.route('/tag/<tagname>')
def tag(tagname):
    posts = load_and_check()
    filtered = [p for p in posts if tagname in p.get('tags', [])]
    return render_template('index.html', posts=filtered, tag=tagname)


@app.route('/feed.xml')
def rss():
    posts = load_and_check()
    domain = request.host_url.rstrip('/')
    items = []
    for p in posts[:20]:
        url = f"{domain}/{p['slug']}"
        pub_date = p.get('date', '')
        items.append(f"""
    <item>
      <title>{p['title']}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{pub_date}</pubDate>
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>MarkBlog</title>
    <link>{domain}</link>
    <description>File-based Markdown blog</description>
    {''.join(items)}
  </channel>
</rss>"""
    resp = make_response(rss_xml)
    resp.content_type = 'application/rss+xml'
    return resp


if __name__ == '__main__':
    # Ensure content directory exists
    import os
    os.makedirs(os.path.join(os.path.dirname(__file__), 'content'), exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
