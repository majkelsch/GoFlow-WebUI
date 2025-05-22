from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "secret_key" # Will definitely be replaced (development use only)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # We only have http for now
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_url="/",
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    offline=True,
    reprompt_consent=True,
)
app.register_blueprint(google_bp, url_prefix="/login")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    given_name = db.Column(db.String(120), nullable=False)
    family_name = db.Column(db.String(120), nullable=False)
    picture = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()




@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for('login'))
    return render_template('index.html', userinfo=get_user_info())

@app.route('/tasks')
def tasks():
    if not google.authorized:
        return redirect(url_for('login'))
    return render_template('tasks.html')


@app.route('/team')
def team():
    if not google.authorized:
        return redirect(url_for('login'))
    return render_template('team.html')

@app.route('/profile')
def profile():
    if not google.authorized:
        return redirect(url_for('login'))
    return render_template('profile.html', userinfo=get_user_info())

@app.route('/config')
def config():
    if not google.authorized:
        return redirect(url_for('login'))
    with open(os.path.join("..", "GoFlow", "config.json"), "r") as f:
        data = f.read()
        data = json.loads(data)
    return render_template('config.html', dataKeys=list(data), data=data)


@app.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()

    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info['name'],
            given_name=user_info['given_name'],
            family_name=user_info['family_name'],
            picture=user_info['picture']
        )
        db.session.add(user)
        db.session.commit()



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    

def get_user_info():
    if not google.authorized:
        return None
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return resp.json()







if __name__ == '__main__':
    app.run(debug=True)