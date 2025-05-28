# app.py
from flask import Flask, render_template, request, redirect, session, url_for, flash
from modules.user import register_user, login_user
from modules.db import insert_transaction, get_all_obat
from datetime import datetime
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
    
    obats = get_all_obat()

    if request.method == 'POST':
        user_id = session['user_id']
        obat_ids = request.form.getlist('obat_id[]')
        jumlahs = request.form.getlist('jumlah[]')
        total_hargas = request.form.getlist('total_harga[]')
        waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for obat_id, jumlah, total_harga in zip(obat_ids, jumlahs, total_hargas):
            insert_transaction(user_id, obat_id, jumlah, total_harga, waktu)
        flash('Pembelian berhasil!', 'success')
    return render_template('beli.html', username=session.get('username'), obats=obats)

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
