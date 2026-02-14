from flask import Flask, render_template, request, redirect, flash, abort, url_for
import smtplib
from email.message import EmailMessage
from graphdata import graph_data
from olympiadproblems import olympiad_problems
import os
import markdown
from memes import memes

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


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
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Save to file
            with open("subscribers.txt", "a") as file:
                file.write(f"{email}\n")

            # Send your notification email
            try:
                msg = EmailMessage()
                msg['Subject'] = 'New Herd Member Joined!'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = EMAIL_ADDRESS
                msg.set_content(f"Good news! {email} has joined the frictionless herd.")

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)

                flash("You've joined the herd! 🐮", "success")
            except Exception as e:
                flash("The cow tripped! Try again later.", "danger")

            # Stay on the page so they see the success message
            return redirect(url_for('subscribe'))

    # If it's a GET request, just show the page
    return render_template('subscribe.html')


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
