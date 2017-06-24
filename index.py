from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message='Hello')

@app.route('/hello/')
def hello():
    return render_template('hello.html', message='Hello world')

if __name__ == '__main__':
    app.debug = True
    app.run()