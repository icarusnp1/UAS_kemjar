# modules/user.py
import re
from werkzeug.security import generate_password_hash, check_password_hash
from modules.db import insert_user, check_user

def register_user(username, email, password):
    # Validasi regex password
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s])(?=.{8,})(?!.*[*\'=]).*$'
    )
    if not pattern.match(password):
        return {
            'success': False,
            'message': 'Password minimal 8 karakter, mengandung huruf besar, huruf kecil, angka, simbol, dan tidak boleh mengandung *, \' atau ='
        }

    if check_user(email):
        return {'success': False, 'message': 'Email sudah terdaftar'}

    password_hash = generate_password_hash(password)
    insert_user(username, email, password_hash)
    return {'success': True, 'message': 'Registrasi berhasil'}

def login_user(email, password):
    user = check_user(email)
    if user and check_password_hash(user['password'], password):
        return {'success': True, 'user_id': user['id'], 'username': user['username']}
    return {'success': False, 'message': 'Email atau password salah'}
