
from flask import Flask, request, jsonify, send_from_directory
import os

# Inisialisasi Flask
app = Flask(__name__, static_folder='.', static_url_path='')

# Lokasi folder project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database sederhana di memori
users_db = {
    "customer": {
        "username": "customer",
        "password": "123",
        "name": "Anisa Rahma",
        "role": "customer"
    },
    "vendor": {
        "username": "vendor",
        "password": "123",
        "name": "Glamour MUA",
        "role": "vendor",
        "category": "Make Up Artist (MUA)"
    },
    "admin": {
        "username": "admin",
        "password": "123",
        "name": "Admin Support",
        "role": "admin"
    },
    "owner": {
        "username": "owner",
        "password": "123",
        "name": "Owner YourGraduation",
        "role": "owner"
    }
}


# ==========================================
# ROUTING HALAMAN UTAMA
# ==========================================

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


# ==========================================
# ROUTING FOLDER PICTURE
# ==========================================

@app.route('/picture/<path:filename>')
def serve_picture(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, 'picture'),
        filename
    )


# ==========================================
# ROUTING FILE STATIC LAINNYA
# ==========================================

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)


# ==========================================
# API LOGIN
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)

    if user and user['password'] == password:
        return jsonify({
            "message": "Login berhasil!",
            "user": {
                "username": user['username'],
                "name": user['name'],
                "role": user['role'],
                "category": user.get('category', '')
            }
        }), 200

    return jsonify({
        "message": "Username atau password salah!"
    }), 401


# ==========================================
# API REGISTER
# ==========================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    if not username or not password or not name:
        return jsonify({
            "message": "Mohon lengkapi data pendaftaran!"
        }), 400

    if username in users_db:
        return jsonify({
            "message": "Username sudah terdaftar!"
        }), 400

    users_db[username] = {
        "username": username,
        "password": password,
        "name": name,
        "role": "customer"
    }

    return jsonify({
        "message": "Pendaftaran berhasil!",
        "user": {
            "username": username,
            "name": name,
            "role": "customer"
        }
    }), 201


# ==========================================
# VERCEL HANDLER
# ==========================================

app = app
