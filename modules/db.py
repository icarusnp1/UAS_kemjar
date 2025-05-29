# modules/db.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='kemjar'  # Pastikan nama DB kamu sesuai
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

def insert_transaction(user_id, obat_id, jumlah, total_harga, waktu):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transaksi (user_id, obat_id, jumlah, total_harga, waktu) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (user_id, obat_id, jumlah, total_harga, waktu))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_obat():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nama, harga FROM obat")
    obats = cursor.fetchall()
    cursor.close()
    conn.close()
    return obats

def get_riwayat():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            r.user_id,
            u.username AS user_name,
            r.obat_id,
            o.nama AS obat_name,
            r.jumlah,
            r.total_harga,
            r.waktu
        FROM transaksi r
        JOIN users u ON r.user_id = u.id
        JOIN obat o ON r.obat_id = o.id
    """
    cursor.execute(query)
    riwayat = cursor.fetchall()
    cursor.close()
    conn.close()
    return riwayat