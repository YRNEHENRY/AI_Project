from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    nb = 4
    size = nb * nb
    return render_template('index.html')