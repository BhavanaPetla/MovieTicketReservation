import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Initialize the App
app = Flask(__name__)
app.secret_key = "cinema_secret_key_99"

# 2. Configure Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cinema.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Define Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(50)) 
    price = db.Column(db.Integer)
    img = db.Column(db.String(500))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie_title = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    total_price = db.Column(db.Integer)

# 4. Create Database and Seed Data (THIS MUST BE AFTER 'app' IS DEFINED)
with app.app_context():
    db.create_all()
    if not Movie.query.first():
        sample_movies = [
            Movie(title="Oppenheimer", category="Hollywood", price=350, img="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500"),
            Movie(title="Jawan", category="Bollywood", price=250, img="https://images.unsplash.com/photo-1598899303450-5a4812255750?w=500"),
            Movie(title="RRR", category="Tollywood", price=300, img="https://images.unsplash.com/photo-1533928298208-27ff66555d8d?w=500"),
            Movie(title="Leo", category="Kollywood", price=250, img="https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=500"),
            Movie(title="Manjummel Boys", category="Mollywood", price=200, img="https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=500"),
            Movie(title="KGF 2", category="Sandalwood", price=300, img="https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=500"),
            Movie(title="Suzume", category="Anime", price=350, img="https://images.unsplash.com/photo-1607604276483-4efdd6d43bb6?w=500")
        ]
        db.session.add_all(sample_movies)
        db.session.commit()

# --- 5. Routes ---

@app.route('/')
def index():
    cat = request.args.get('category')
    if cat:
        movies = Movie.query.filter_by(category=cat).all()
    else:
        movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=request.form['username'], password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            flash("Username already exists!")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash("Invalid Credentials")
    return render_template('login.html')

@app.route('/book/<int:mid>', methods=['POST'])
def book(mid):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    movie = Movie.query.get(mid)
    seats = int(request.form.get('seats'))
    new_b = Booking(
        user_id=session['user_id'], 
        movie_title=movie.title, 
        seats=seats,
        total_price=seats * movie.price
    )
    db.session.add(new_b)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    my_bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', bookings=my_bookings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)