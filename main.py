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

@app.route('/singlepost', methods=['POST', 'GET'])
def singlepost():
    
    id = request.args.get('id')

    #use id to query database save to variable

    post = Blog.query.filter_by(id=id).first()
    #blogpost = #query return using id


    #render template with variable 
    return render_template('singlepost.html', post=post)

    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        
        title = str(request.form['title'])
        title_from_form = title
        title_error = ''

        body = str(request.form['body'])
        body_from_form = body
        body_error = ''

        if title_from_form == "" and body_from_form == "":
            title_error = "please enter valid text"
            body_error = "please enter valid text"
            return render_template('newpost.html', title_error = title_error, body_error = body_error)
        if title_from_form == "":
            title_error = "please enter valid text"
            return render_template('newpost.html', title_error = title_error)
        if body_from_form == "":
            body_error = "please enter valid text"  
            return render_template('newpost.html', body_error = body_error)
        
        
        db.session.add(new_post)
        db.session.commit()
        id = new_post.id
        return redirect('/singlepost?id={}'.format(id))

    return render_template('newpost.html')
    

@app.route('/blogposts', methods=['POST', 'GET'])
def blog():
    
    blogs = Blog.query.all()
    return render_template('blogposts.html', blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blogposts.html')

if __name__ == '__main__':
    app.run()