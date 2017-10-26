from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz1@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dfndsosnfsdnsiiii'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(256))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['index', 'blog', 'login', 'signup', 'singlepost']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = str(request.form['username'])
        username_error = ""

        if len(username) < 3:
            username_error = "username must be longer than 3 characters"
        if len(username) > 20:
            username_error = "username cannot be longer than 20 characters"

        password = str(request.form['password'])
        verify = str(request.form['verify'])
        password_error = ""

        if len(password) < 3:
            password_error = "password must be longer than 3 characters"
        if len(password) > 20:
            password_error = "password cannot be longer than 20 characters"
        if password != verify:
            password_error = "passwords do not match"
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            username_error = "this username already exists"
        if not existing_user and not username_error and not password_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        
        else:
            return render_template('signup.html', username_error=username_error, password_error=password_error, username=username)
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/newpost')
        else:
            flash("username or password incorrect, or user does not exist", "error")
    
    return render_template('login.html')

@app.route ('/logout')
def logout():
    del session['username']
    flash("Logged out")
    return redirect('/')

@app.route('/singlepost', methods=['POST', 'GET'])
def singlepost():
    id = request.args.get('id')
    post = Blog.query.filter_by(id=id).first()
    return render_template('singlepost.html', post=post)

@app.route('/singleuser', methods=['POST','GET'])
def singleuser():
    user_id = request.args.get('user')
    user_query = User.query.get(user_id)
    all_posts = Blog.query.filter_by(owner=user_query).all()
    return render_template('singleuser.html', all_posts=all_posts)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body, owner)

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

@app.route('/index', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users, title='title')

if __name__ == '__main__':
    app.run()