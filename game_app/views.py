from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')
size = 4

@app.route('/')
def index():
    return render_template('index.html', size = size)

@app.route('/game/')
def game():
    return render_template('game.html', size = size)