from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        msg = request.form['msg']
        return render_template('index.html', message=msg)
    else:
        return redirect(url_for('index'))
@app.route('/hello/')
def hello():
    return render_template('hello.html', message='Hello world')

if __name__ == '__main__':
    app.debug = True
    app.run()