from flask import Flask, render_template, request, redirect, abort, url_for
from graphdata import graph_data
from olympiadproblems import olympiad_problems
import os
import markdown
import firebase_admin
from firebase_admin import firestore, credentials
from memes import memes

app = Flask(__name__)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sitemaps')
def sitemaps():
    return render_template('sitemaps.xml')


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
        if email:
            # Add to Firebase
            db.collection('subscribers').add({
                'email': email,
            })
            success = True
            # We stay on the page to show the "User added!" message
            return render_template('subscribe.html', success=success)

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
