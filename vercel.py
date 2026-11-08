from flask import Flask, request, jsonify, send_from_directory
import urllib.parse
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    # Auto decode spasi %20 dari browser Vercel
    decoded_filename = urllib.parse.unquote(filename)
    return send_from_directory('.', decoded_filename)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    # logic login tetap sama...
    return jsonify({"message": "Login berhasil!"}), 200

app = app
