# modules/db.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='obat_store'  # Pastikan nama DB kamu sesuai
    )

def insert_user(username, email, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

def check_user(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def insert_transaction(user_id, obat_id, jumlah):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transaksi (user_id, obat_id, jumlah) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, obat_id, jumlah))
    conn.commit()
    cursor.close()
    conn.close()
