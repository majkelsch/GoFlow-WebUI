from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
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
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
)
app.register_blueprint(google_bp, url_prefix="/login")




@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]
    return render_template('index.html', email=email)

@app.route('/tasks')
def tasks():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template('tasks.html')


@app.route('/team')
def team():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template('team.html')

@app.route('/profile')
def profile():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template('profile.html')

@app.route('/config')
def config():
    if not google.authorized:
        return redirect(url_for("google.login"))
    with open(os.path.join("..", "GoFlow", "config.json"), "r") as f:
        data = f.read()
        data = json.loads(data)
    return render_template('config.html', dataKeys=list(data), data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))







if __name__ == '__main__':
    app.run(debug=True)