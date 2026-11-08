from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Database Sederhana di Memori (Dapat dihubungkan ke Database Eksternal)
users_db = {
    "customer": {"username": "customer", "password": "123", "name": "Anisa Rahma", "role": "customer"},
    "vendor": {"username": "vendor", "password": "123", "name": "Glamour MUA", "role": "vendor", "category": "Make Up Artist (MUA)"},
    "admin": {"username": "admin", "password": "123", "name": "Admin Support", "role": "admin"},
    "owner": {"username": "owner", "password": "123", "name": "Owner YourGraduation", "role": "owner"}
}

# --- ROUTING STATIC FILES (HTML & GAMBAR) ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# --- ROUTING API ENDPOINTS ---
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
    
    return jsonify({"message": "Username atau password salah!"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    if not username or not password or not name:
        return jsonify({"message": "Mohon lengkapi data pendaftaran!"}), 400

    if username in users_db:
        return jsonify({"message": "Username sudah terdaftar!"}), 400

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

# Entry point untuk Vercel Serverless Function
app = app
