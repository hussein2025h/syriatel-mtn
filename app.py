from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(_name_)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
conn = sqlite3.connect('requests.db')
conn.execute('''CREATE TABLE IF NOT EXISTS requests
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              phone TEXT NOT NULL,
              amount TEXT NOT NULL,
              company TEXT NOT NULL)''')
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form['phone']
    amount = request.form['amount']
    company = request.form['company']

    conn = sqlite3.connect('requests.db')
    conn.execute('INSERT INTO requests (phone, amount, company) VALUES (?, ?, ?)',
                 (phone, amount, company))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    rows = cursor.fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)