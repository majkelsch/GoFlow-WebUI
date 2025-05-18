from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/profile')
def profile():
    return render_template('index.html')






if __name__ == '__main__':
    app.run(debug=True)