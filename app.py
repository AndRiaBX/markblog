"""MarkBlog — Flask application serving file-based Markdown blog."""

from flask import Flask, render_template, request, make_response
import markdown
from xml.sax.saxutils import escape as xml_escape
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
        return render_template('404.html', title='Not Found'), 404
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
        # XML-escape title and description to prevent injection
        safe_title = xml_escape(p['title'])
        items.append(f"""
    <item>
      <title>{safe_title}</title>
      <link>{xml_escape(url)}</link>
      <guid>{xml_escape(url)}</guid>
      <pubDate>{xml_escape(pub_date)}</pubDate>
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>MarkBlog</title>
    <link>{xml_escape(domain)}</link>
    <description>A file-based Markdown blog engine</description>
    {''.join(items)}
  </channel>
</rss>"""
    resp = make_response(rss_xml)
    resp.content_type = 'application/rss+xml'
    return resp


if __name__ == '__main__':
    # Ensure content directory exists
    import os
    content_path = os.path.join(os.path.dirname(__file__), 'content')
    os.makedirs(content_path, exist_ok=True)
    print(f'[markblog] Content directory: {content_path}')
    print('[markblog] Starting server at http://0.0.0.0:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
