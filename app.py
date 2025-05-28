from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from pytz import timezone
import os

app = Flask(__name__)
app.secret_key = 'secret'
IST = timezone('Asia/Kolkata')

# Dummy database
users = {}
transactions = []

def get_time():
    return datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = request.form['uid']
        password = request.form['password']
        if uid in users and users[uid]['password'] == password:
            session['user'] = uid
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uid = request.form['uid']
        name = request.form['name']
        password = request.form['password']
        if uid not in users:
            users[uid] = {
                'name': name,
                'password': password,
                'balance': 1000000,
                'joined': get_time()
            }
            return redirect(url_for('login'))
        return 'User already exists'
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    uid = session['user']
    if request.method == 'POST':
        to = request.form['to']
        amount = int(request.form['amount'])
        if to in users and users[uid]['balance'] >= amount:
            users[uid]['balance'] -= amount
            users[to]['balance'] += amount
            transactions.append({
                'from': uid,
                'to': to,
                'amount': amount,
                'time': get_time()
            })
    return render_template('dashboard.html', user=users[uid], uid=uid)

@app.route('/admin')
def admin():
    code = request.args.get('code')
    if code == '1234567890':
        return render_template('admin.html', users=users, transactions=transactions)
    return redirect(url_for('index'))

@app.route('/conversion')
def conversion():
    return render_template('conversion.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
