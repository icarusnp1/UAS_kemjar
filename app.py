from flask import Flask, render_template, request, redirect, url_for, session
from modules.db import init_db, get_user_by_email, add_user, add_transaction
from modules.crypto_utils import encrypt_aes, decrypt_aes, rsa_decrypt_key
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session key

# Initialize DB once
init_db()

@app.route('/')
def index():
    if 'user' in session:
        return render_template('beli.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        enc_data = request.form['data']
        enc_key = request.form['key']

        aes_key = rsa_decrypt_key(enc_key)
        decrypted = decrypt_aes(enc_data, aes_key)

        email, password = decrypted.split('|')
        user = get_user_by_email(email)

        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('index'))
        return 'Login gagal'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        enc_data = request.form['data']
        enc_key = request.form['key']

        aes_key = rsa_decrypt_key(enc_key)
        decrypted = decrypt_aes(enc_data, aes_key)

        name, email, password = decrypted.split('|')
        if get_user_by_email(email):
            return 'Email sudah terdaftar'
        add_user(name, email, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/beli', methods=['POST'])
def beli():
    if 'user' not in session:
        return redirect(url_for('login'))
    obat = request.form['obat']
    jumlah = request.form['jumlah']
    add_transaction(session['user'], obat, jumlah)
    return 'Pembelian berhasil'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
