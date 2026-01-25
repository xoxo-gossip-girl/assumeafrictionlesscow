from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.message import EmailMessage
from graphdata import graph_data
import os

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


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/memes')
def memes():
    return render_template('memes.html')


@app.route('/olympiad')
def olympiad():
    return render_template('olympiad.html')


# This bit is for the contact page if they want to contact us...
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']
#
#         msg = EmailMessage()
#         msg['Subject'] = 'New Contact Form Submission'
#         msg['From'] = EMAIL_ADDRESS
#         msg['To'] = EMAIL_ADDRESS
#         msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#         try:
#             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#                 smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#                 smtp.send_message(msg)
#             flash("Message sent successfully!", "success")
#         except Exception as e:
#             flash("Failed to send message.", "danger")
#     return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
