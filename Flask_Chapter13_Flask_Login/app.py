from flask import Flask, request, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin




login_manager = LoginManager()
db = SQLAlchemy()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in first lol!'

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    db.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/profile')
    @login_required
    def profile():
        return f'<h1> You are in the profile, current user: - {current_user.username}{current_user.id}  </h1>'
    
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            user = User.query.filter_by(username=username).first()

            if not user:
                return f'User does not exist'
            
            login_user(user)

            if 'next' in session and session['next']:
                if is_safe_url(session['next']):
                    print('KWIWIWIIWIWI')
                    return redirect(session['next'])
                

            return redirect(url_for('index'))
        
        
        session['next'] = request.args.get('next')
        return render_template('login.html')

    
    @app.route('/logout')
    def logout():
        logout_user()
        return f'Kwik wylogowany!'
    
    @app.route('/')
    def index():
        return render_template('index.html')
        

    return app


