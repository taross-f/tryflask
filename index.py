import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

from werkzeug import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'jif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return '''<p>ログインしてください</p>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username == 'admin':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return '''<p>ユーザー名が違います</p>'''
    return '''
        <form action="" method="post">
            <p><input type="text" name="username">
            <p><input type="submit" value="Login">
        </form>
        '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save('./uploads/' + img_file.filename)
            return render_template('index.html')
        else:
            return '''<p>許可されていない拡張子です</p>'''
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('./uploads', filename)

@app.route('/hello/')
def hello():
    return render_template('hello.html', message='Hello world')

if __name__ == '__main__':
    app.debug = True
    app.run()