from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from graphdata import graph_data
from olympiadproblems import olympiad_problems
import os
import markdown
import firebase_admin
from firebase_admin import firestore
from memes import memes
from datetime import datetime

app = Flask(__name__)

# if not firebase_admin._apps:
#     firebase_admin.initialize_app()
#
# db = firestore.client()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sitemap.xml')
def sitemap():
    pages = []
    static_urls = [
        {'loc': '/', 'priority': '1.0'},
        {'loc': '/about', 'priority': '0.5'},
        {'loc': '/posts', 'priority': '0.7'},
        {'loc': '/memes', 'priority': '0.3'},
        {'loc': '/olympiad', 'priority': '0.7'},
    ]
    for url in static_urls:
        pages.append(url)
    for category in graph_data.keys():
        pages.append({'loc': f'/posts/{category}', 'priority': '0.6'})
    for cat in graph_data.values():
        for post in cat['posts']:
            pages.append({'loc': post['url'], 'priority': '0.8'})
    for p in olympiad_problems.values():
        pages.append({'loc': f"/{p['url_slug']}", 'priority': '0.8'})
    base_url = "https://assumeafrictionlesscowtheblog.web.app"
    lastmod = datetime.now().strftime("%Y-%m-%d")

    xml_content = render_template('sitemap_template.xml',
                                  pages=pages,
                                  base_url=base_url,
                                  lastmod=lastmod)

    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/posts')
def posts():
    return render_template('posts.html', graph_data=graph_data)


@app.route('/posts/<category>')
def show_graph(category):
    data = graph_data.get(category)
    return render_template('graph_page.html', hub_title=data['title'], hub_color=data['color'], posts=data['posts'])


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    success = False
    if request.method == 'POST':
        email = request.form.get('email')
        # if email:
        #     # Add to Firebase
        #     db.collection('subscribers').add({
        #         'email': email,
        #     })
        #     success = True
        #     # We stay on the page to show the "User added!" message
        #     return render_template('subscribe.html', success=success)

    return render_template('subscribe.html', success=success)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/memes')
def meme():
    return render_template('memes.html', memes=memes)


@app.route('/olympiad')
def olympiad():
    return render_template('olympiad.html', problems=olympiad_problems)


@app.route('/<path:post_slug>')
def individual_post(post_slug):
    # 1. Find the metadata in your graph_data
    target_url = f"/{post_slug}"
    post_metadata = None
    color = "#333"

    for p in olympiad_problems.values():
        if p['url_slug'] == f"{post_slug}":
            post_metadata = p
            break

    for cat in graph_data.values():
        for p in cat['posts']:
            if p['url'] == target_url:
                post_metadata = p
                color = cat['color']
                break

    if not post_metadata:
        abort(404)

    # 2. Look for the corresponding Markdown file
    file_path = os.path.join('posts', f"{post_slug}.md")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            # Convert Markdown to HTML
            html_content = markdown.markdown(text, extensions=['extra', 'codehilite'])
    else:
        html_content = "<p>Content coming soon...</p>"

    return render_template('post_page.html',
                           post=post_metadata,
                           content=html_content,
                           color=color)



if __name__ == '__main__':
    app.run(debug=True)
