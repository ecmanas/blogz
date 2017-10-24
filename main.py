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
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        
        else:
            return '<h1>Duplicate User</h1>'
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            print(session)
            return redirect('/')
        else:
            flash("User password incorrect or user does not exist", "error")
    
    return render_template(login.html)

@app.route ('/logout', methods=['POST'])
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/singlepost', methods=['POST', 'GET'])
def singlepost():
    id = request.args.get('id')
    post = Blog.query.filter_by(id=id).first()
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