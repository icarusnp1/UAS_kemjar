# app.py
from flask import Flask, render_template, request, redirect, session, url_for, flash
from modules.user import register_user, login_user
from modules.db import insert_transaction
import os

app = Flask(__name__)
app.secret_key = 'rahasia_super_aman'  # Ganti jadi key rahasia kamu

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/beli')
    return redirect('/login')

# 🔐 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = register_user(
            request.form['username'],
            request.form['email'],
            request.form['password']
        )
        if result['success']:
            flash('Registrasi berhasil, silakan login', 'success')
            return redirect('/login')
        flash(result['message'], 'error')
    return render_template('register.html')

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = login_user(request.form['email'], request.form['password'])
        if result['success']:
            session['user_id'] = result['user_id']
            session['username'] = result['username']
            return redirect('/beli')
        flash(result['message'], 'error')
    return render_template('login.html')

# 🛒 Beli Obat
@app.route('/beli', methods=['GET', 'POST'])
def beli():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        user_id = session['user_id']
        obat_id = request.form['obat_id']
        jumlah = request.form['jumlah']
        insert_transaction(user_id, obat_id, jumlah)
        flash('Pembelian berhasil!', 'success')
    return render_template('beli.html', username=session.get('username'))

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
