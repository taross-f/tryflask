import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)

@app.route('/')
def show_entries():
    con = sqlite3.connect('todo.db')
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS message(data_id, msg, data_time)''')
    result = con.execute('''select * from message order by data_id desc''')
    return render_template('index.html', result=result)

@app.route('/send/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        msg = request.form['msg']
        if not msg:
            alert = '入力してください'
            return render_template('index.html', alert=alert)
        else:
            date_time = datetime.datetime.today()
            data_id = date_time.strftime("%Y%m%d%H%M%S")
            con = sqlite3.connect('todo.db')
            c = con.cursor()
            c.execute('INSERT INTO message VALUES(?,?,?)', (data_id, msg, date_time))
            con.commit()
            result = con.execute('''select * from message order by data_id desc''')
            return render_template('index.html', result=result)

@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
    if request.method == 'POST':
        data_ids = request.form['action']
        con = sqlite3.connect('todo.db')
        c = con.cursor()
        query = "DELETE FROM message WHERE data_id=?"
        c.execute(query, (data_ids,))
        con.commit()
        result = con.execute('''select * from message order by data_id desc''')
        return render_template('index.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()