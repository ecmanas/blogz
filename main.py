from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:dothedamnthing@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/singlepost')

    title_error = ''
    body_error = ''

    return render_template('newpost.html')

@app.route('/blogposts', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blogposts.html', blogs=blogs)

@app.route('/singlepost')
def singlepost():
    blog_id = request.args.get('id')
    return render_template('singlepost.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blogposts.html')

if __name__ == '__main__':
    app.run()