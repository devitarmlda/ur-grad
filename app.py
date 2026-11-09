from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import random

app = Flask(__name__, static_folder='.')
CORS(app)

DB_FILE = 'database.json'

def load_data():
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": [
                {"username": "owner", "password": "123", "role": "owner", "name": "Owner Your Graduation"},
                {"username": "admin", "password": "123", "role": "admin", "name": "Admin Operational"},
                {"username": "vendor", "password": "123", "role": "vendor", "name": "Mitra Vendor MUA & Studio"},
                {"username": "customer1", "password": "123", "role": "customer", "name": "Upin Ipin"},
                {"username": "ninuninu", "password": "tyas1234", "role": "customer", "name": "Nirma"}
            ],
            "orders": [
                {
                    "id": "#YG-8821",
                    "username": "customer1",
                    "name": "Upin Ipin",
                    "prodi": "Sastra Inggris",
                    "university": "Universitas Sebelas Maret",
                    "date": "2026-11-06",
                    "time": "08:00",
                    "location": "Gedung Serbaguna Kampus",
                    "branch": "Pekalongan",
                    "status": "Lunas - Slot Terkunci",
                    "total": 749000,
                    "items": ["Paket Ultimate Wisuda"]
                }
            ],
            "chats": []
        }
        with open(DB_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {"users": [], "orders": [], "chats": []}

def save_data(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Gagal menyimpan data:", e)

# Serving Frontend Utama
@app.route('/')
def index():
    return send_from_directory(app.root_path, 'index.html')

# Melayani gambar secara langsung agar tetap dapat diakses setelah deploy ke Vercel.
@app.route('/picture/<path:filename>')
def serve_picture(filename):
    return send_from_directory(os.path.join(app.root_path, 'picture'), filename)

# API GET & POST ORDERS
@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    data = load_data()
    
    if request.method == 'GET':
        return jsonify(data.get('orders', [])), 200

    if request.method == 'POST':
        req_data = request.json
        branch = req_data.get('branch')
        date = req_data.get('date')
        time_slot = req_data.get('time', '08:00')

        # Proteksi Kuota Maksimal 4 Customer
        existing = [o for o in data.get('orders', []) if o.get('branch') == branch and o.get('date') == date and o.get('time') == time_slot]
        if len(existing) >= 4:
            return jsonify({"error": f"KUOTA PENUH! Cabang {branch} pada tanggal {date} jam {time_slot} WIB sudah memenuhi kuota batas (4/4)."}), 409

        new_id = f"#YG-{random.randint(1000, 9999)}"
        new_order = {
            "id": new_id,
            "username": req_data.get('username', 'guest'),
            "name": req_data.get('name'),
            "prodi": req_data.get('prodi'),
            "university": req_data.get('university'),
            "date": date,
            "time": time_slot,
            "location": req_data.get('location'),
            "branch": branch,
            "status": "Lunas - Slot Terkunci",
            "total": req_data.get('total', 0),
            "items": req_data.get('items', [])
        }

        data['orders'].append(new_order)
        save_data(data)
        return jsonify({"status": "success", "id": new_id, "message": "Pesanan tersimpan di Database!"}), 201

# API LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    req = request.json
    data = load_data()
    username = req.get('username')
    password = req.get('password')

    user = next((u for u in data.get('users', []) if u['username'] == username and u['password'] == password), None)
    if user:
        return jsonify({"status": "success", "user": {"username": user['username'], "role": user['role'], "name": user['name']}}), 200
    return jsonify({"status": "error", "message": "Username atau Password salah!"}), 401

# API REGISTER
@app.route('/api/register', methods=['POST'])
def register():
    req = request.json
    data = load_data()
    username = req.get('username')

    if any(u['username'] == username for u in data.get('users', [])):
        return jsonify({"status": "error", "message": "Username sudah terdaftar!"}), 400

    new_user = {
        "username": username,
        "password": req.get('password'),
        "role": "customer",
        "name": req.get('name')
    }
    data['users'].append(new_user)
    save_data(data)
    return jsonify({"status": "success", "user": {"username": new_user['username'], "role": "customer", "name": new_user['name']}}), 201

# API CHATS
@app.route('/api/chats', methods=['GET', 'POST'])
def handle_chats():
    data = load_data()
    if request.method == 'GET':
        return jsonify(data.get('chats', [])), 200

    if request.method == 'POST':
        chat_item = request.json
        data['chats'].append(chat_item)
        save_data(data)
        return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
